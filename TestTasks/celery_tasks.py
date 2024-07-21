from ApiTestEngine.core2.cases import run_test
from TestScenes.serializer import SceneToCaseListSerializer
from TestTasks.models import TestTaskModel, TestRecordModel, TestReport
from Testproject.models import TestEnv
from django.shortcuts import get_object_or_404
from apiTestPlaform.celery import celery_app

@celery_app.task
def run_taskcase_celry(env_id,task_id,tester):
    '''
    运行测试计划的方法，调用装饰celery_app注册到任务服务
    :param env_id: 环境id
    :param task_id: 计划id
    :param tester: 测试人
    :return:
    '''
    # 获取env数据，,如果没有找到返回404
    env = get_object_or_404(TestEnv, id=env_id)
    # 拼装env_config参数
    env_config = {
        'ENV': {
            'host': env.host,
            'headers': env.headers,
            **env.global_variable,

        },
        'DB': '',
        'global_func': env.global_func
    }
    # 获取task对象,如果没有找到返回404
    task = get_object_or_404(TestTaskModel, id=task_id)
    # 获取与该任务关联的所有场景
    scens_list = task.scenes.all()
    task_case_data = []
    for scene in scens_list:
        # 返回与当前 scene 相关的所有 SceneToCase 对象
        cases = scene.scenetocase_set.all()
        res = SceneToCaseListSerializer(cases, many=True).data
        sorted_res = sorted(res, key=lambda k: k['sort'])
        scene_case_list = [item["case"] for item in sorted_res]
        task_case_data.append(
            {
                "name": scene.name,
                "Cases": scene_case_list
            }
        )
    # 初始化创建TestRecordModel测试记录对象
    record_obj = TestRecordModel.objects.create(task=task, env=env, tester=tester, status="执行中")

    result = run_test(case_data=task_case_data, env_config=env_config, debug=False)
    # 执行完任务运行后，更新TestRecordModel实例对应的属性
    record_obj.all = result["all"]
    record_obj.success = result["success"]
    record_obj.error = result["error"]
    record_obj.fail = result["fail"]
    record_obj.pass_rate = "{:.2f}".format(result["success"] / result["all"])
    record_obj.status = "执行完成"
    record_obj.save()
    # c初始化TestReport实例，保存测试报告数据到info
    report_obj = TestReport.objects.create(record=record_obj, info=result)
    report_obj.save()
    # print(result)
"""
URL configuration for apiTestPlaform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from TestTasks.views import TestTaskViewSet, TestRecordView, TestReportView
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from TestScenes.views import UpdateSceneCaseOrderView,ScenesViewSet
from TestInterface.views import TestInterfaceCaseViewSet

from users.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    # 登录接口的访问路径
    path('api/users/login/', LoginView.as_view(), name='login'),
    # 请求刷新token路径
    path('api/users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 校验token路径
    path('api/users/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    #注册修改业务流用例顺序的接口路由
    path('api/testFlow/update_scenes_case_order/', UpdateSceneCaseOrderView.as_view(), name='update_scenes_case_order'),
    #注册接口用例运行的接口路由，指定post请求api/TestInterface/case_run/时候，映射TestInterfaceCaseViewSet中的run_case方法
    path("api/TestInterface/case_run/",TestInterfaceCaseViewSet.as_view({
        "post":"run_case"
    }),name="run_case"),
    # 注册测试场景运行的接口路由，指定post请求api/testFlow/scenes_run/时候，映射UpdateSceneCaseOrderView中的scenes_run方法
    path("api/testFlow/scenes_run/",ScenesViewSet.as_view({
        "post":"scenes_run"
    }),name="scenes_run"),

]

# 导入drf的router和自定义的视图集
from Testproject.views import TestProjectView,TestEnvView,TestFileView
from TestInterface.views import TestInterfaceView,TestInterfaceCaseViewSet
from TestScenes.views import  ScenesViewSet,SceneToCaseViewSet
from rest_framework import routers

# 实例化louters
routers = routers.SimpleRouter()
# 注册测试项目接口路由
routers.register("api/testPro/projects", TestProjectView)
#注册测试环境接口路由
routers.register("api/testPro/envs", TestEnvView)
#注册上传文件接口路由
routers.register("api/testPro/files", TestFileView)
#z注册测试接口增删改查接口路由
routers.register('api/TestInterface/interface',TestInterfaceView)
#注册接口测试用例管理的路由
routers.register('api/TestInterface/case',TestInterfaceCaseViewSet)
#注册接口业务流管理路由
routers.register('api/testFlow/scenes',ScenesViewSet)
#注册业务流用例管理路由
routers.register('api/testFlow/cases',SceneToCaseViewSet)
#注册测试任务管理模块的路由
routers.register("api/testTask/task",TestTaskViewSet)
#注册测试记录接口的路由
routers.register("api/testTask/records",TestRecordView)
#注册测试报告接口的路由
routers.register("api/testTask/records/reports",TestReportView)








urlpatterns += routers.urls

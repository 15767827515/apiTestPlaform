
# 创建一个celery的应用，并且加载settings的celery配置
import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE','apiTestPlaform.settings')
# 创建celery的应用
celery_app = Celery('apiTestPlaform')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
# 自动加载Django每个应用下的tasks.py文件，获取celery的注册任务
celery_app.autodiscover_tasks()
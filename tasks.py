from celery import Celery
from celery.schedules import crontab
from webapp import create_app
from webapp.parser import get_python_news

flask_app = create_app()
celery_app = Celery('tasks', broker='redis://localhost:6379/0')


@celery_app.task
def parse():
    with flask_app.app_context():
        get_python_news('http://python.org/blog')


@celery_app.on_after_configure.connect
def setup_shedule(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/1'), parse.s())





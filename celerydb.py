import imp
import logging
import ssl 
import sys 

from celery import Celery
from celery.signals import after_setup_logger 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# CELERY_TASK_LIST = [
#     'app.tasks'
# ]

def create_celery_app(_app=None):
    """ Create a new Celery object with Celery config
        Wrap tasks in context of Flask
    """
    from model import db

    celery = Celery(_app.import_name, backend=_app.config["CELERY_BACKEND"], broker=_app.config["CELERY_BROKER_URL"] )
    celery.conf.update(_app.config)
    class ContextTask(celery.Task): 
        def __call__(self, *args: any, **kwargs):
            with _app.app_context(): 
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
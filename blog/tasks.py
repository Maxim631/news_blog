import time

from celery import shared_task

@shared_task
def some_funk():
    time.sleep(10)

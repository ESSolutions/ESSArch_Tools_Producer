from __future__ import absolute_import

from celery import Celery

app = Celery('workflow',
             broker='amqp://guest:guest@localhost:5672//',
             backend='amqp://',
             include=['workflow.tasks'])

#app.autodiscover_tasks(['workflow.stuff.prepareip'])

if __name__ == '__main__':
    app.start()

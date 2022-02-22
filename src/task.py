import logging
import os
from time import sleep

from celery import Celery, bootsteps
from kombu import Consumer, Exchange, Queue

from db import connect, save_data
from firebasemessaging import sendNotification

# from notification.repositories import save_notification

logger = logging.getLogger(__name__)

exchange = Exchange('cb_notification', type='direct')
offer_queue = Queue(name='offer-queue', exchange=exchange,
                    routing_key='offer-queue')
announcement_queue = Queue(name='announcement_queue',
                           exchange=exchange, routing_key='announcement_queue')

celery_app = Celery(
    'consumer',
    broker=os.environ.get('CELERY_BROKER_URL'),
    backend=os.environ.get('CELERY_BROKER_URL')
)


class OfferConsumer(bootsteps.ConsumerStep):
    def get_consumers(self, channel):
        return [Consumer(channel,
                         queues=[offer_queue],
                         callbacks=[self.handle_message],
                         accept=['json'])]

    def handle_message(self, body, message):
        print(body)
        save_data(connect(), body)
        sendNotification(body)
        message.ack()


class AnnouncementConsumer(bootsteps.ConsumerStep):
    def get_consumers(self, channel):
        return [Consumer(channel,
                         queues=[announcement_queue],
                         callbacks=[self.handle_message],
                         accept=['json'])]

    def handle_message(self, body, message):
        print(body)
        save_data(connect(), body)
        sendNotification(body)
        message.ack()


celery_app.steps['consumer'].add(OfferConsumer)
celery_app.steps['consumer'].add(AnnouncementConsumer)


if __name__ == '__main__':
    celery_app.start()

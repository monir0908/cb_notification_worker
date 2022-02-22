import json
import logging
import os

from pyfcm import FCMNotification

push_service = FCMNotification(api_key=os.environ.get('FCM_SERVER_KEY'))


def sendNotification(data):
    try:
        # data = json.loads(body)
        if data['topic']:
            extra_notification_kwargs = {
                'image': data.get('image')
            }
            result = push_service.notify_topic_subscribers(
                topic_name=data['topic'], message_title=data['title'], message_body=data['body'], data_message=data, extra_notification_kwargs=extra_notification_kwargs)
            logging.info(result)
    except ValueError as e:
        print(e)

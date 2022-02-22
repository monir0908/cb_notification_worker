import datetime
import json
import os
from typing import Dict

from dateutil import parser
from pymongo import MongoClient


def connect() -> MongoClient:
    client = MongoClient(os.environ.get('MONGO_URL'))
    print(client.database_names())
    return client


def save_data(client: MongoClient, body: Dict):
    db = client['pusher']
    collection = db['notification']
    # body = json.loads(body)
    data = {
        'title': body.get('title'),
        'body': body.get('body'),
        'topic': body.get('topic'),
        'type': body.get('type'),
        'resource_info': body.get('resource_info'),
        'image': body.get('image'),
        'origin': body.get('origin'),
        'platform': body.get('platform'),
        'country_code': body.get('country_code'),
        'expired_at': parser.parse(body.get('expired_at')),
        'created_at': datetime.datetime.now()
    }
    collection.insert_one(data)

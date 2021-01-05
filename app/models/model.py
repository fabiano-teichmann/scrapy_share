from datetime import datetime

from mongoengine import Document, StringField, FloatField, \
    DateTimeField, ReferenceField


class Company(Document):
    name = StringField(required=True)
    description = StringField(required=False, default='')
    updated_at = DateTimeField(required=False)
    country = StringField()
    currency = StringField()

    meta = {
        'collection': 'company',
        'indexes': [
            'name', 'country', 'currency'
        ]
    }


class Share(Document):
    name = StringField(required=True)
    date = DateTimeField(required=True)
    open = FloatField(required=True)
    low = FloatField(required=True)
    high = FloatField(required=True)
    close = FloatField(required=True)

    meta = {
        'collection': 'share',
        'indexes': [
            'name', 'date'
        ]
    }

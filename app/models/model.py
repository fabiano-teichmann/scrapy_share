from mongoengine import Document, StringField, ListField, FloatField, \
    EmbeddedDocument, DateTimeField, BooleanField, DateField, EmbeddedDocumentField


class Share(EmbeddedDocument):
    date = DateTimeField(required=True)
    open = FloatField(required=True)
    low = FloatField(required=True)
    high = FloatField(required=True)
    close = FloatField(required=True)


class Company(Document):
    name = StringField(required=True)
    description = StringField(required=False, default='')
    updated_at = DateTimeField(required=True)
    country = StringField()
    currency = StringField()
    share = ListField(EmbeddedDocumentField(Share))

    meta = {
        'collection': 'share',
        'indexes': [
            'name', 'country'
        ]
    }


class Stock(Document):
    symbol = StringField(required=True)
    country = StringField(required=True)
    get_share = BooleanField(required=True, default=False)

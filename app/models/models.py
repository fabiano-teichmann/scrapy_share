from mongoengine import Document, StringField, FloatField, DateField, queryset_manager


class CompanyModel(Document):
    name = StringField(required=True, unique=True)
    description = StringField(required=False, default='')
    description_pt = StringField(required=False, default='')
    updated_at = DateField(required=False)
    initial_date = DateField(required=False)
    country = StringField()
    currency = StringField()

    @queryset_manager
    def get_company(doc_cls, queryset, name):
        return queryset(name=name).first()

    def save(self, *args, **kwargs):
        return super(CompanyModel, self).save()

    meta = {
        'collection': 'company',
        'indexes': [
            'name', 'country', 'currency'
        ]
    }


def update_date(model, updated_at, first_date):
    model.update_at = updated_at
    model.initial_date = first_date
    return model.save()


class ShareModel(Document):
    name = StringField(required=True)
    date = DateField(required=True)
    open = FloatField(required=True)
    low = FloatField(required=True)
    high = FloatField(required=True)
    close = FloatField(required=True)
    average = FloatField(required=True)

    meta = {
        'collection': 'share',
        'indexes': [
            'name', 'date'
        ]
    }

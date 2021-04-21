import peewee as pee

db = pee.SqliteDatabase('invest.db')


class BaseModel(pee.Model):
    class Meta:
        database = db


class CompanyModel(BaseModel):
    name = pee.CharField(unique=True, primary_key=True)
    description = pee.CharField(default="")
    updated_at = pee.DateField(null=True)
    initial_date = pee.DateField(null=True)
    country = pee.CharField()
    currency = pee.CharField()


class ShareModel(BaseModel):
    name = pee.ForeignKeyField(CompanyModel, backref='shares')
    date = pee.DateField(null=False)
    open = pee.FloatField()
    low = pee.FloatField()
    high = pee.FloatField()
    close = pee.FloatField()
    average = pee.FloatField()

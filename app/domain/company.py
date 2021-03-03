from logger import logger
from pydantic import ValidationError

from app.models.models import CompanyModel, update_date
from app.models.validator import CompanyValidator


class Company:
    def __init__(self, name):
        self.model = CompanyModel
        self.name = name
        self.company = self._get_company()

    def save(self, data: dict):
        data.update({'name': self.name})
        payload = self._validator_data(data)
        if payload:
            try:
                return self.model(**data).save()
            except Exception as e:
                logger.error(f'Something unexpected happened in try save bd {e.args}')
                raise e
        else:
            return False

    @staticmethod
    def update_company(model: CompanyModel, last_date, first_date):
        return update_date(model, last_date, first_date)

    @staticmethod
    def _validator_data(data: dict) -> dict:
        try:
            validator = CompanyValidator(**data)
            return validator.dict()
        except ValidationError:
            logger.error(f'Data is not valid - {data}')
            return {}

    def _get_company(self):
        return self.model.get_company(self.name)

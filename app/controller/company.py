from logger import logger
from pydantic import ValidationError

from app.models.models import CompanyModel, update_date
from app.models.validator import CompanyValidator


class Company:
    def __init__(self):
        self.model = CompanyModel

    def save(self, data: dict):
        payload = self._validator_data(data)
        if payload:
            try:
                return self.model(**data).save
            except Exception as e:
                logger.error(f'Something unexpected happened in try save bd {e.args}')
                raise e
        else:
            return False

    @staticmethod
    def update_company(model: CompanyModel, last_date):
        return update_date(model, last_date)

    @staticmethod
    def _validator_data(data: dict) -> dict:
        try:
            validator = CompanyValidator(**data)
            return validator.dict()
        except ValidationError:
            logger.error(f'Data is not valid - {data}')
            return {}

    def get_company(self, name: str):
        return self.model.get_company(name)

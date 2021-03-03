from datetime import date
from datetime import timedelta

from googletrans import Translator
from logger import logger

from app.domain.company import Company
from app.domain.get_shares import GetShares
from app.models.connect_db import connect_mongodb
from app.models.models import ShareModel


class CompanyShare:
    def __init__(self, symbol: str, country: str, date_start: str = '01/01/2010'):
        connect_mongodb()
        self.symbol = symbol
        self.country = country
        self.date_start = date_start
        self.share = GetShares(self.country)
        self.today = date.today()
        self.translator = Translator()

    def _translate_description(self, text: str, language='pt'):
        try:
            if text:
                return self.translator.translate(text=text, dest=language).text
            return ''
        except Exception as e:
            logger.error(f"Something unexpected happened in translate ERROR: {e}")
            return ''

    def get_share(self):
        try:
            company = Company(self.symbol)

            if company.company is None:
                profile = self.share.company_profile(self.symbol)
                if profile:
                    last_date, currency = self.add_share(self.date_start)
                    first_date = ShareModel.objects(name=self.symbol).first()
                    if last_date:
                        company.save({'description':  profile, 'updated_at': last_date, 'country': self.country,
                                      'description_pt': self._translate_description(profile), 'currency': currency,
                                      'initial_date': first_date.date})
                        logger.info(f"New Company {self.symbol} add")
                return 1
            else:
                date = company.company.updated_at + timedelta(days=1)
                last_date, currency = self.update_share(date)
                first_date = ShareModel.objects(name=self.symbol).first()
                company.update_company(company.company, last_date, first_date.date)
                return 1 if currency else 0
        except Exception as e:
            logger.error(f"Something unexpected happened  - {e.args}")
            raise e

    def update_share(self, date: date):

        if date < self.today:
            date = date.strftime("%d/%m/%Y")
            try:
                df = self.share.get_historical_data(self.symbol, date)
            except Exception as e:
                logger.error(f"Something unexpected happened : {e}")
                return False, False
            return self.save_share(df, len(df.index))
        else:
            logger.info(f'Share company {self.symbol} Already updated')
            return False, False

    def save_share(self, df, total_row):
        try:
            for r in range(0, total_row):
                ShareModel(**{
                    'name': self.symbol,
                    'open': df['Open'][r],
                    'low': df['Low'][r],
                    'high': df['High'][r],
                    'average': round((df['Low'][r] + df['High'][r]) / 2, 2),
                    'close': df['Close'][r],
                    'date': df.index[r].date()
                }).save()
                last_date = df.index[r].date()
                currency = df['Currency'][r]
            logger.info(f"Add share for company {self.symbol} total register insert {total_row}")
            return last_date, currency
        except Exception as e:
            logger.error(f"Something unexpected happened in save share company {self.symbol} \n  error {e.args}")
            return False, False

    def add_share(self, date: str):
        try:
            df = self.share.get_historical_data(self.symbol, date)
            total_row = len(df.index)
            if total_row > 60:
                last_date, currency = self.save_share(df, total_row)
                return last_date, currency
            return False, False
        except Exception as e:
            logger.error(f"Something unexpected happened in get share company {self.symbol} \n  error {e.args}")
            return False, False

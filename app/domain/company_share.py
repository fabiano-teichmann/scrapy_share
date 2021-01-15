from datetime import date
from datetime import timedelta

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

    def get_share(self):
        try:
            company = Company(self.symbol)

            if company.company is None:
                profile = self.share.company_profile(self.symbol)
                if profile:
                    last_date, currency = self.add_share(self.date_start)
                    if last_date:
                        company.save({'description':  profile, 'updated_at': last_date,
                                      'country': self.country, 'currency': currency})
                        logger.info(f"New Company {self.symbol} add")
                return 1
            else:
                date = company.company.updated_at + timedelta(days=1)
                if date < self.today:
                    date = date.strftime("%d/%m/%Y")
                    last_date, currency = self.add_share(date)
                    company.update_company(company.company, last_date)
                    logger.info(f"Share company {self.symbol} updated")
                    return 1
                else:
                    logger.info(f'Share company {self.symbol} Already updated')
                    return 0
        except Exception as e:
            logger.error(f"Something unexpected happened  - {e.args}")
            raise e

    def add_share(self, date: str):
        try:
            last_date = ''
            currency = ''
            df = self.share.get_historical_data(self.symbol, date)
            rows = len(df.index)
            for r in range(0, rows):
                ShareModel(**{
                    'name': self.symbol,
                    'open': df['Open'][r],
                    'low': df['Low'][r],
                    'high': df['High'][r],
                    'close': df['Close'][r],
                    'date': df.index[r].date()
                }).save()
                last_date = df.index[r].date()
                currency = df['Currency'][r]

            logger.info(f"Add share for company {self.symbol} total register insert {rows}")
            return last_date, currency
        except Exception as e:
            logger.error(f"Something unexpected happened in get share company {self.symbol} \n  error {e.args}")
            return False, False

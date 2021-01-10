from datetime import timedelta
from datetime import date
from time import sleep

from logger import logger

from app.models.connect_db import connect_mongodb
from app.models.model import Company, Share
from app.worker import GetShares


class CompanyShare:
    def __init__(self, symbol: str, country: str):
        self.symbol = symbol
        self.country = country
        self.share = GetShares(self.country)
        self.today = date.today()

    def get_share(self):
        company = Company.objects(name=self.symbol).first()
        if company is None:
            profile = self.share.company_profile(self.symbol)
            last_date, currency = self.add_share('01/01/2000')
            Company(name=self.symbol, description=profile,
                    updated_at=last_date,
                    country=self.country,
                    currency=currency).save()
            logger.info(f"New Company {self.symbol} add")
        else:
            date = company.updated_at + timedelta(days=1)
            if date > self.today:
                date = date.strftime("%d/%m/%Y")
                last_date, currency = self.add_share(date)
                company.updated_at = last_date
                company.save()
                logger.info(f"Share company {self.symbol} updated")
            else:
                logger.info(f'Share company {self.symbol} Already updated ')

    def add_share(self, date: str):

        last_date = ''
        currency = ''
        df = self.share.get_historical_data(self.symbol, date)
        rows = len(df.index)
        for r in range(0, rows):
            Share(**{
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


if __name__ == '__main__':
    stop = 10
    count = 0
    connect_mongodb()
    shares = GetShares('brazil').get_list_shares()
    for share in shares:
        company = CompanyShare(share, 'brazil')
        company.get_share()
        count += 1
        if count >= stop:
            logger.info(f"Stop consumer API for 30 seg total register inserted: {count} total break {int(stop/10)}")
            stop = stop + 10 if stop == count else stop
            sleep(30)

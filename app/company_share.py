from datetime import timedelta
from datetime import date
from time import sleep, time

from logger import logger

from app.controller.company import Company
from app.models.connect_db import connect_mongodb
from app.models.models import Share
from app.worker import GetShares


class CompanyShare:
    def __init__(self, symbol: str, country: str):
        self.symbol = symbol
        self.country = country
        self.share = GetShares(self.country)
        self.today = date.today()

    def get_share(self):
        try:
            controller = Company()
            company = controller.get_company(self.symbol)
            if company is None:
                profile = self.share.company_profile(self.symbol)
                if profile:
                    last_date, currency = self.add_share('01/01/2000')
                    if last_date:
                        controller.save({'name': self.symbol, 'description':
                            profile, 'updated_at': last_date, 'country': self.country, 'currency': currency})
                        logger.info(f"New Company {self.symbol} add")
                return 1
            else:
                date = company.updated_at + timedelta(days=1)
                if date > self.today:
                    date = date.strftime("%d/%m/%Y")
                    last_date, currency = self.add_share(date)
                    controller.update_company(company, last_date)
                    logger.info(f"Share company {self.symbol} updated")
                    return 1
                else:
                    logger.info(f'Share company {self.symbol} Already updated ')
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
        except Exception as e:
            logger.error(f"Something unexpected happened in get share company {self.symbol} \n  error {e.args}")
            return False, False


def import_shares(country='brazil'):
    start = time()
    stop = 20
    count = 0
    connect_mongodb()
    shares = GetShares(country).get_list_shares()
    for share in shares:
        company = CompanyShare(share, 'brazil')
        get_company = company.get_share()
        count = count + get_company
        if count >= stop:
            logger.info(f"Stop consumer API for 10 seg total register inserted: {count} total break {int(stop / 20)}")
            stop = stop + 20 if stop == count else stop
            sleep(10)
    logger.info(f"Finished import shares in {round(time() - start, 2)} seg")


if __name__ == '__main__':
    import_shares('brazil')

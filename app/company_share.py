from datetime import datetime, timedelta
import pendulum
from app.models.model import Company, Share
from app.worker import GetShares


class CompanyShare:
    def __init__(self, symbol: str, country: str):
        self.symbol = symbol
        self.country = country
        self.share = GetShares(self.country)
        self.profile = self.share.company_profile(self.symbol)

    def get_share(self):
        company = Company.objects(name=self.symbol).first()
        if company is None:
            last_date = self.add_share('01/01/2000')
            company.updated_at = last_date
            company.save()

        else:
            date = company.updated_at + timedelta(days=1)
            date = date.strftime("%d/%m/%Y")
            last_date = self.add_share(date)
            company.updated_at = last_date
            company.save()

    def add_share(self, date: str):
        last_date = ''
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
        return last_date


if __name__ == '__main__':
    share = GetShares('brazil').get_list_shares()
    company = CompanyShare(share[1], 'brazil')
    company.get_share()


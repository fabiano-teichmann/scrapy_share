from datetime import datetime, timedelta
import pendulum
from app.models.model import Company
from app.worker import GetShares


class CompanyShare:
    def __init__(self, symbol: str, country: str):
        self.symbol = symbol
        self.country = country
        self.share = GetShares(self.country)
        self.profile = self.share.company_profile(self.symbol)

    def share(self):
        company = Company.objects(name=self.symbol).first()
        if company:
            date = company.updated_at + timedelta(days=1)
            date = f'{date.days}/{date.month}/{date.year}'
            historical_share = self.add_share(date)
            data = {'name': self.symbol, 'description': self.profile,
                    'share': historical_share, 'updated_at': historical_share[-1]['date']}
            return Company(**data).save()
        else:
            data = self.add_share('01/01/2000')
            company.update(add_to_set__share=data)

    def add_share(self, date: str):
        historical_share = []
        df = self.share.get_historical_data(self.symbol, date)
        rows = len(df.index)
        for r in range(0, rows):
            historical_share.append({
                'open': df['Open'][r],
                'low': df['Low'][r],
                'high': df['High'][r],
                'close': df['Close'][r],
                'date': df.index[r].date()
            })

        return historical_share


if __name__ == '__main__':
    share = GetShares('brazil').get_list_shares()

    company = CompanyShare(share[1], 'brazil')
    company.add_share()
    # shares = share.get_list_shares()
    # profile = share.company_profile(shares[3])
    # historical_data = share.get_historical_data(shares[3])
    # recent_historical = share.get_recent_historical(shares[3])

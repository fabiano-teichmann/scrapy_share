import investpy
import pendulum

from app.models.connect_db import connect_mongodb


class GetShares:
    def __init__(self, country: str = 'brazil'):
        connect_mongodb()
        self.country = country
        self.now = pendulum.now('UTC').format('DD/MM/YYYY')

    def get_list_shares(self):
        shares_list = investpy.get_stocks_list(country=self.country)
        return shares_list

    def get_historical_data(self, share: str):
        df = investpy.get_stock_historical_data(stock=share, country=self.country, from_date='01/01/2020',
                                                to_date=self.now, as_json=False, order='ascending')

        return df

    def get_recent_historical(self, share: str):
        df = investpy.get_stock_recent_data(stock=share, country=self.country, as_json=False, order='ascending')
        return df

    def company_profile(self, share):
        profile = investpy.get_stock_company_profile(stock=share, country=self.country, language='english')
        if profile.get('desc'):
            return profile['desc']
        else:
            return ""


if __name__ == '__main__':
    share = GetShares('brazil')
    shares = share.get_list_shares()
    print(shares)
    profile = share.company_profile(shares[3])
    recent_historical = share.get_recent_historical(shares[3])
    historical_data = share.get_historical_data(shares[3])

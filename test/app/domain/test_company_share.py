import pendulum

from app.domain.company_share import CompanyShare


def test_add_company_share(resource):
    date_start = pendulum.now()
    date_start = date_start.subtract(days=10)
    date_start = date_start.strftime("%d/%m/%Y")
    symbol = 'ABEV3'
    assert CompanyShare(symbol=symbol, country='brazil', date_start=date_start).get_share()
    msg = f"New Company {symbol} add"
    # resource.check_present(('root', 'INFO', msg), order_matters=False)


def test_update_share_already_update(resource):
    symbol = 'ABEV3'
    date_start = pendulum.now()
    date_start = date_start.subtract(days=10)
    date_start = date_start.strftime("%d/%m/%Y")
    assert CompanyShare(symbol=symbol, country='brazil', date_start=date_start).get_share() == 1
    msg = f"Share company {symbol} Already updated"
    # resource.check_present(('root', 'INFO', msg), order_matters=False)


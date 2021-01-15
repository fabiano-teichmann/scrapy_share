from datetime import time
from time import sleep
from logger import logger

from app.domain.company_share import CompanyShare
from app.domain.get_shares import GetShares
from app.models.connect_db import connect_mongodb


def import_shares(country='brazil'):
    start = time()
    stop = 20
    count = 0
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
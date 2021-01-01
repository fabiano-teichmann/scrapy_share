import logger
import mongoengine

from app.settings import Settings


def connect_mongodb():
    try:
        setup = Settings()
        logger.info('Connecting to Mongo')
        mongoengine.connect(host=setup.MONGODB_URI, serverSelectionTimeoutMS=5000)
        logger.info('Connected to Mongo')
    except Exception as e:
        logger.error(f'Something unexpected happened {e}')
        raise e

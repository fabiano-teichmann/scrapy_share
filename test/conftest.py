import pytest
from mongoengine import disconnect
import os
from testfixtures import LogCapture


@pytest.fixture(scope='module')
def resource():
    log = LogCapture()
    os.environ['MONGODB_URI'] = 'mongomock://localhost'
    yield log
    disconnect()
    log.uninstall()

# coding=utf-8
import pytest


def pytest_addoption(parser):
    parser.addoption('--wsdl_url', action='store',  default='http://test.rkdoo.loc/epgu/service-rkdoo/soap-server?wsdl')
    parser.addoption('--pghost', action='store',  default='10.150.250.14')
    parser.addoption('--pgdb', action='store',  default='test_rkdoo')
    parser.addoption('--pguser', action='store',  default='test_rkdoo')
    parser.addoption('--pgpassword', action='store',  default='96xmZRVC')


@pytest.yield_fixture(scope='function')
def config(request):
    yield request.config

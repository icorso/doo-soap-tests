# coding=utf-8
import pytest
from hamcrest import assert_that, equal_to
from suds import WebFault
from suds.client import Client


@pytest.mark.usefixtures('config')
def test_get_order_current_queue_pos_no_guid(config):
    try:
        client = Client(config.option.wsdl_url)
        client.service.getOrderCurrentQueuePosStr()
    except WebFault as err:
        assert_that(err.fault.faultstring, equal_to("Value: guid must not be empty, and it is an string"))


@pytest.mark.usefixtures('config')
def test_get_order_current_queue_pos_int_guid(config):
    guid = "abc"
    try:
        client = Client(config.option.wsdl_url)
        client.service.getOrderCurrentQueuePosStr(guid=guid)
    except WebFault as err:
        assert_that(err.fault.faultstring, equal_to("Заявление с указанным guid: \"%s\" не существует" % guid))

# coding=utf-8
import random

import pytest
from hamcrest import assert_that, has_length
from suds.client import Client

from db.dao import StatusOrder
from db.db import DbConnect
from matchers import has_attributes, compares_attributes
from response import Response


@pytest.mark.usefixtures('config')
def test_get_status_order_success(config):
    # <rkdoo>
    # <statusorder>
    #   <id>1</id>
    #   <name>Очередник - не подтвержден</name>
    #   <description>Заявление создано, но отсутствует дата регистрации в очереди
    # ( требуется подтверждение личности заявителя)</description>
    # </statusorder>
    # <statusorder>...</statusorder>
    # </rkdoo>

    db = DbConnect(config)
    client = Client(config.option.wsdl_url)

    status_orders = db.query_all(StatusOrder, StatusOrder.is_deleted == False)
    expected_status_order = random.choice(status_orders)

    response = Response(client.service.getStatusOrderSpr())
    actual_status_order = list(filter(lambda e: e.id == expected_status_order.id, response.statusorder))[0]
    expected_attributes = ['id', 'name', 'description']
    assert_that(actual_status_order, has_attributes(expected_attributes),
                u'Ошибка при проверки атрибутов метода getStatusOrderSpr()'),
    assert_that(actual_status_order, compares_attributes(expected_status_order),
                u'Ошибка при проверки значений атрибутов метода getStatusOrderSpr()'),
    assert_that(actual_status_order, has_length(len(status_orders)),
                u'Не верное ожидаемое количество элементов rkdoo.statusorder')

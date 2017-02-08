# coding=utf-8
import random

import pytest
from hamcrest import assert_that, has_length
from sqlalchemy import and_
from suds.client import Client

from db.dao import Doo
from db.db import DbConnect
from matchers import has_attributes, compares_attributes
from response import Response


@pytest.mark.usefixtures('config')
def test_get_gardens_single(config):
    # <doo>
    #   <id>60</id>
    #   <district_id>5</district_id>
    #   <city_id>76</city_id>
    #   <type_id>1</type_id>
    #   <type_founders_id>1</type_founders_id>
    #   <type_active_id>1</type_active_id>
    #   <type_ovz_id>1</type_ovz_id>
    #   <name>Лютик №4</name>
    #   <email>duz4_lytik@mail.ru</email>
    #   <site/>
    #   <address>297407, Республика Крым, г.Евпатория, ул.Советская,9</address>
    #   <supervisor>Любашина Виктория Владимировна</supervisor>
    #   <phones>79788305930</phones>
    #   <mode>Пн-Пт с 7.30 до 18.00</mode>
    #   <doo_features/>
    #   <more_activities_type/>
    # </doo>

    db = DbConnect(config)
    doos = db.query_all(Doo, and_(Doo.is_deleted == False))
    expected_doo = random.choice(doos)

    client = Client(config.option.wsdl_url)
    response = Response(client.service.getGardensSpr())

    actual_doo = list(filter(lambda e: e.id == expected_doo.id, response.doo))[0]

    expected_attributes = ['id', 'district_id', 'city_id', 'type_id', 'id', 'type_active_id', 'type_ovz_id', 'name',
                           'email', 'site', 'address', 'supervisor', 'phones', 'mode', 'doo_features',
                           'more_activities_type']

    assert_that(actual_doo, has_attributes(expected_attributes), u'Ошибка при проверки атрибутов метода getGardensSpr()')
    assert_that(actual_doo, compares_attributes(expected_doo),
                u'Ошибка при проверки значений атрибутов метода getGardensSpr()')
    assert_that(actual_doo, has_length(len(doos)), u"Количество детских садов в ответе не соответствует ожидаемому")

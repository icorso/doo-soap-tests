# coding=utf-8
import random

import pytest
from hamcrest import assert_that, equal_to, has_length
from sqlalchemy import and_
from suds import WebFault
from suds.client import Client

from db.dao import District, City
from db.db import DbConnect
from matchers import compares_attributes, has_attributes
from response import Response


@pytest.mark.usefixtures('config')
def test_get_city_no_district(config):
        try:
            client = Client(config.option.wsdl_url)
            client.service.getCitySpr()
        except WebFault as err:
            assert_that(err.fault.faultstring, equal_to("Value: district must not be empty, and it is an integer"))


@pytest.mark.usefixtures('config')
def test_get_city_empty_district(config):
        try:
            client = Client(config.option.wsdl_url)
            client.service.getCitySpr(district="")
        except WebFault as err:
            assert_that(err.fault.faultstring, equal_to("Value: district must not be empty, and it is an integer"))


@pytest.mark.usefixtures('config')
def test_get_city_only_id(config):
        try:
            client = Client(config.option.wsdl_url)
            client.service.getCitySpr(id=103)
        except WebFault as err:
            assert_that(err.fault.faultstring, equal_to("Value: district must not be empty, and it is an integer"))


@pytest.mark.usefixtures('config')
def test_get_city_success(config):
        # <rkdoo>
        #   <city>
        #       <id>76</id>
        #       <district_id>5</district_id>
        #       <name>Евпатория</name>
        #       <socr>г</socr>
        #   </city>
        #   <city>...</city>
        # </rkdoo>

        db = DbConnect(config)
        client = Client(config.option.wsdl_url)

        districts = db.query_all(District, District.is_deleted == False)
        district = random.choice(districts)

        cities = db.query_all(City, and_(City.is_deleted == False, City.district_id == district.id))
        expected_city = random.choice(cities)

        response = Response(client.service.getCitySpr(district=district.id))
        actual_city = list(filter(lambda e: e.id == expected_city.id, response.city))[0]
        expected_attributes = ['id', 'district_id', 'name', 'socr']

        assert_that(actual_city, has_attributes(expected_attributes),
                    u'Ошибка при проверки атрибутов метода getCitySpr()')
        assert_that(actual_city, compares_attributes(expected_city),
                    u'Ошибка при проверки значений атрибутов метода getCitySpr()')
        assert_that(actual_city, has_length(len(cities)), u"Количество городов в ответе не соответствует ожидаемому")

# coding=utf-8
import random

import pytest
from hamcrest import assert_that, equal_to, none
from suds import WebFault
from suds.client import Client

from db.dao import Benefit, TypeBenefit
from db.db import DbConnect
from matchers import has_attributes, compares_attributes
from response import Response

reason = "Метод с несуществующим %s, не должен возвращать значения"


@pytest.mark.usefixtures('config')
def test_get_benefit_nonexistent_id(config):
    try:
        client = Client(config.option.wsdl_url)
        r = Response(client.service.getBenefitSpr(id='99999'))
        assert_that(len(r.benefit), equal_to(none), reason % 'id')
    except WebFault as err:
        assert_that(err.fault.faultstring, equal_to("Data not available"))


@pytest.mark.usefixtures('config')
def test_get_benefit_nonexistent_district(config):
    try:
        client = Client(config.option.wsdl_url)
        r = Response(client.service.getBenefitSpr(district='1'))
        assert_that(len(r.benefit), equal_to(none), reason % 'district')
    except WebFault as err:
        assert_that(err.fault.faultstring, equal_to("Data not available"))


@pytest.mark.usefixtures('config')
def test_get_benefit_empty_district(config):
    try:
        client = Client(config.option.wsdl_url)
        r = Response(client.service.getBenefitSpr(district=""))
        assert_that(len(r.benefit), equal_to(none), reason % 'district')
    except WebFault as err:
        assert_that(err.fault.faultstring, equal_to("Value: district must not be empty, and it is an integer"))


@pytest.mark.usefixtures('config')
def test_get_benefit_success(config):
    db = DbConnect(config)
    benefits = db.query_all(Benefit, Benefit.is_deleted == False)
    expected_benefit = random.choice(benefits)
    benefit_name = db.query_first(TypeBenefit, TypeBenefit.id == expected_benefit.type_id).name
    expected_benefit.name = benefit_name

    client = Client(config.option.wsdl_url)
    response = Response(client.service.getBenefitSpr(id=expected_benefit.id))
    actual_benefit = list(filter(lambda e: e.id == expected_benefit.id, response.benefit))[0]

    expected_attributes = ['id', 'name', 'description', 'district_id', 'confirm_doc', 'updated_at']

    assert_that(actual_benefit, has_attributes(expected_attributes),
                u'Ошибка при проверки атрибутов метода getBenefitSpr()')
    assert_that(actual_benefit, compares_attributes(expected_benefit),
                u'Ошибка при проверки значений атрибутов метода getBenefitSpr()')

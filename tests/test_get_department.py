# coding=utf-8
import random

import pytest
from hamcrest import assert_that, has_length
from suds.client import Client

from db.dao import Department
from db.db import DbConnect
from matchers import has_attributes, compares_attributes
from response import Response

reason = u'Значение поля %s не соответствует ожидаемому'


@pytest.mark.usefixtures('config')
def test_get_department_success(config):
        # <rkdoo>
        #   <department>
        #     <id>1</id>
        #     <name>Министерство образования, науки и молодежи Республики Крым</name>
        #     <district_id>1</district_id>
        #     <city_id>29</city_id>
        #     <address>295000, Республика Крым, г. Симферополь, пер. Совнаркомовский, 3</address>
        #     <phones>тел.007-3652-27-52-32, факс 007-3652-27-61-33</phones>
        #     <email>info.crimea@edu.ru</email>
        #     <site>monm.rk.gov.ru</site>
        #   </department>
        #   <department>...</department>
        # </rkdoo>

        db = DbConnect(config)
        departments = db.query_all(Department, Department.is_deleted == False)
        expected_department = random.choice(departments)

        client = Client(config.option.wsdl_url)
        response = Response(client.service.getDepartmentSpr())
        actual_department = list(filter(lambda d: d.id == expected_department.id, response.department))[0]

        expected_attributes = ['email', 'city_id', 'name', 'phones', 'site', 'id', 'district_id', 'address']

        assert_that(actual_department, has_attributes(expected_attributes),
                    u'Ошибка при проверки атрибутов метода getDepartmentSpr()')
        assert_that(actual_department, compares_attributes(expected_department),
                    u'Ошибка при проверки значений атрибутов метода getDepartmentSpr()')
        assert_that(actual_department, has_length(len(departments)),
                    u"Количество департаментов в ответе не соответствует ожидаемому")

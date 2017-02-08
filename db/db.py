# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DbConnect(object):
    def __init__(self, config):
        self.host = config.option.pghost
        self.user = config.option.pguser
        self.password = config.option.pgpassword
        self.db = config.option.pgdb
        self.engine = create_engine('postgres://' + self.user + ':' + self.password + '@' + self.host + '/' +
                                    self.db, echo=False)

    def query_first(self, table, filter_):
        """
        Выборка первой записи по указанному фильтру из таблицы
        :param table: класс sqlalchemy, описывающий таблицу базы данных
        :param filter_: фильтр данных из таблицы
        :return: первый результат запроса (заполненный 'table' инстанс) или None если резутат не содержит записей.
        Example: user.query_first(History, History.mobile_phone == '3456774')
        """
        s = sessionmaker(bind=self.engine, expire_on_commit=False)()
        result = s.query(table).filter(filter_).first()
        s.close()
        return result

    def query_all(self, table, filter_):
        """
        Выборка всех записей по указанному фильтру из таблицы
        :param table: класс sqlalchemy, описывающий таблицу базы данных
        :param filter_: фильтр данных из таблицы
        :return:
        Example: user.query_all(Advance, Advance.advance_time.like('2015-10-08%'))
        """
        s = sessionmaker(bind=self.engine, expire_on_commit=False)()
        results = s.query(table).filter(filter_).all()
        s.close()
        return results

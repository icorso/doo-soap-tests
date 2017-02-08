from sqlalchemy import Column, Integer, String, Boolean, true, DateTime, false
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import Null

Base = declarative_base()


class StatusOrder(Base):
    __tablename__ = 'status_order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(String(512))
    created_at = Column(Integer)
    updated_at = Column(Integer)
    is_deleted = Column(Boolean)

    def __repr__(self):
        return "<StatusOrder(id='%s', name='%s', description='%s')>" % (self.id, self.name, self.description)

    def __str__(self):
        return self.__repr__()


class District(Base):
    __tablename__ = 'district'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    description = Column(String())
    oktmo = Column(Integer)
    is_deleted = Column(Boolean)

    def __repr__(self):
        return "<District(id='%s', name='%s', oktmo='%s')>" % (self.id, self.name, self.oktmo)

    def __str__(self):
        return self.__repr__()


class Doo(Base):
    __tablename__ = 'doo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer)
    district_id = Column(Integer)
    type_id = Column(Integer)
    type_founders_id = Column(Integer)
    type_active_id = Column(Integer)
    type_ovz_id = Column(Integer, default=1)
    code = Column(String(32))
    name = Column(String(255))
    email = Column(String(50))
    site = Column(String(255), default='')
    address = Column(String(512))
    supervisor = Column(String(150))
    founders = Column(String(512))
    phones = Column(String(255))
    mode = Column(String(255))
    inn = Column(String(10))
    kpp = Column(String(9))
    is_active = Column(Boolean, default=true)
    doo_features = Column(String(255))
    commission_at = Column(DateTime)
    created_at = Column(Integer)
    updated_at = Column(Integer)
    is_deleted = Column(Boolean, default=false)
    meal_serving_type_id = Column(Integer, default=1)
    more_activities_type = Column(String(255), default=Null)
    fias = Column(String(255), default=Null)

    def __repr__(self):
        return "<Doo(id='%s', name='%s')>" % (self.id, self.name)

    def __str__(self):
        return self.__repr__()


class Department(Base):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    district_id = Column(Integer)
    city_id = Column(Integer)
    address = Column(String(512))
    phones = Column(String(255))
    email = Column(String(50))
    site = Column(String(255), default='')
    description = Column(String(512), default='')
    created_at = Column(Integer)
    updated_at = Column(Integer)
    is_deleted = Column(Boolean, default=false)

    def __repr__(self):
        return "<Department(id='%s', name='%s')>" % (self.id, self.name)

    def __str__(self):
        return self.__repr__()


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True, autoincrement=True)
    district_id = Column(Integer)
    name = Column(String(40))
    socr = Column(String(10))
    is_deleted = Column(Boolean)

    def __repr__(self):
        return "<City(id='%s', name='%s')>" % (self.id, self.name)

    def __str__(self):
        return self.__repr__()


class TypeFounders(Base):
    __tablename__ = 'type_founders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    description = Column(String(512))
    created_at = Column(Integer)
    updated_at = Column(Integer)
    is_deleted = Column(Boolean, default=false)

    def __repr__(self):
        return "<TypeFounders(id='%s', name='%s')>" % (self.id, self.name)

    def __str__(self):
        return self.__repr__()


class Benefit(Base):
    __tablename__ = 'benefit'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_id = Column(Integer)
    description = Column(String(1024), nullable=False)
    confirm_doc = Column(String(1024))
    created_at = Column(Integer)
    updated_at = Column(Integer)
    is_deleted = Column(Boolean, default=false)
    district_id = Column(Integer, default=1)

    def __repr__(self):
        return "<Benefit(id='%s', description='%s')>" % (self.id, self.description)

    def __str__(self):
        return self.__repr__()


class TypeBenefit(Base):
    __tablename__ = 'type_benefit'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1024))
    created_at = Column(Integer)
    updated_at = Column(Integer)
    is_deleted = Column(Boolean, default=false)

    def __repr__(self):
        return "<TypeBenefit(id='%s', name='%s')>" % (self.id, self.name)

    def __str__(self):
        return self.__repr__()

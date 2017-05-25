from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
# from mysql.connector import MySQLConnection, Error

# engine = create_engine('sqlite:///mydatabase.db', echo=True)
# engine = create_engine('mysql://wdp:kajhzbn7vceW@localhost')
# engine = create_engine('mysql+mysqlconnector://wdp:kajhzbn7vceW@localhost/todo')

engine = create_engine('sqlite:///base_mjsqla.db', echo=True)

Base = declarative_base()

class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    title = Column(String)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
       return "<Company('%s')>" % (self.title)  # old style!!!


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    salary = Column(Integer)
    company_id = Column(Integer, ForeignKey('company.id'))

    def __init__(self, company_id, name, salary=2500):
        self.name = name
        self.salary = salary
        self.company_id = company_id

    def __repr__(self):
       return "<Employee('%s','%s')>" % (self.name, self.salary)


company_table = Company.__table__
employee_table = Employee.__table__
metadata = Base.metadata


if __name__ == "__main__":
    metadata.create_all(engine)
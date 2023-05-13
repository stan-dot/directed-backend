from typing import Any
from .database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric, event
from sqlalchemy.sql.expression import text
from .seeding import init_table


class Schools(Base):
    __tablename__ = 'schools'
    name = Column(String, nullable=False, primary_key=True)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    gender_school = Column(String, nullable=False)



class Cohorts(Base):
    __tablename__ = 'cohorts'
    name = Column(String, nullable=False, primary_key=True)
    description = Column(Text)


class Students(Base):
    __tablename__ = 'students'
    personal_id = Column(String, nullable=False, primary_key=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String)
    last_name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    pseudonym = Column(String, nullable=False, unique=True)
    github_link = Column(String, unique=True)
    cohort = Column(String, ForeignKey(Cohorts.name, ondelete="SET NULL", onupdate="CASCADE"))
    school = Column(String, ForeignKey(Schools.name, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    phone_number = Column(String)
    cardano_wallet = Column(String, unique=True)
    atala_prism_did = Column(String, unique=True)
    milestones_achieved = Column(Integer, server_default=text('0'))
    pschool_token = Column(String, unique=True)
    pAcceptance_token = Column(String, unique=True)
    grant_received = Column(Numeric, server_default=text('0'))
    total_grant = Column(Numeric, server_default = text('0'))


class Milesones(Base):
    __tablename__ = 'milestones'
    description = Column(Text)
    step_nbr = Column(Integer, nullable=False, primary_key=True)
    cohort_name = Column(String, ForeignKey(Cohorts.name, ondelete="CASCADE", onupdate="CASCADE"), nullable=False, primary_key=True)


# set up event listener for table creation to seed the tables after creation
# event.listen(Schools.__table__, 'after_create', init_table)
# event.listen(Cohorts.__table__, 'after_create', init_table)
# event.listen(Students.__table__, 'after_create', init_table)
# event.listen(Milesones.__table__, 'after_create', init_table)

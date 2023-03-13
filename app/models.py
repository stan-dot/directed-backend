from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, Enum, Numeric, event
from sqlalchemy.sql.expression import text


class Schools(Base):
    school_gender_enum = Enum('Female', 'Male', 'Mixed', name='gender_school')

    __tablename__ = 'schools'
    name = Column(String, nullable=False, primary_key=True)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    gender_school = Column(school_gender_enum, nullable=False)

class Cohorts(Base):
    __tablename__ = 'cohorts'
    name = Column(String, nullable=False, primary_key=True)
    description = Column(Text)

class Students(Base):
    gender_enum = Enum('Female', 'Male', name='gender')
    __tablename__ = 'students'
    personal_id = Column(String, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    gender = Column(gender_enum, nullable=False)
    email = Column(String, nullable=False, unique=True)
    pseudonym = Column(String, nullable=False, unique=True)
    cohort = Column(String, ForeignKey(Cohorts.name, ondelete="SET NULL"))
    school = Column(String, ForeignKey(Schools.name), nullable=False)
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
    cohort_name = Column(String, ForeignKey(Cohorts.name), nullable=False, primary_key=True)


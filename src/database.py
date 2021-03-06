#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# pylint: disable=C0111

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, backref
from sqlalchemy import create_engine

Base = declarative_base()

'''
*   "Service" represents a particular service. This is a particular medication, surgical procedure, voice training, therapy, or anything else that gets added later.
*   "Service type" classifies groups of services and is most relevant for actually reading a medical plan. These are 'other', 'surgery', and 'medication'
'''

def connect (db_path):
    engine = create_engine('sqlite:///%s' % db_path)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


# TODO: refactor significantly
# company_by_name, plan_by_company_name, and create_plan have a very poor logic flow. But we
# are out of time and trying to make sure that this feature exists.
def company_by_name(session, name):
    company = session.query(Company).filter(Company.name == name).all()
    return company[0] if len(company) > 0 else None


def plan_by_company_name(session, company_name, plan_name, state):
    company = company_by_name(session, company_name)
    if company is None:
        return None

    plans = [p for p in company.plans
             if p.state == state and p.name == plan_name]
    return plans[0] if plans else None


def create_plan(session, company_name, plan_name, state):
    company = company_by_name(session, company_name)
    if company is None:
        c = Company(name=company_name)
        session.add(c)
        session.commit()
    company = company_by_name(session, company_name)
    assert company is not None

    plan = Plan(company=company,
                name=plan_name,
                state=state,
                color_code=None,
                medicaid=False)
    session.add(plan)
    session.commit()
    return plan_by_company_name(session, company_name, plan_name, state)


class Company (Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Plan (Base):
    __tablename__ = 'plan'
    id = Column(Integer, primary_key=True)

    company_id = Column(Integer, ForeignKey('company.id'), nullable=False)
    company = relationship(Company, backref=backref('plans', uselist=True))

    name = Column(String(250), nullable=False)
    state = Column(String(20), nullable=False)
    color_code = Column(Enum('bronze', 'silver', 'gold', 'platinum', 'catastrophic', 'not-present'),
                        nullable=True)
    medicaid = Column(Boolean, nullable=False)

    def to_dict(self):
        if self.color_code != 'not-present':
            plan_type = self.color_code
        elif self.medicaid:
            plan_type = 'medicaid'
        else:
            plan_type = 'private'

        return {'state': self.state,
                'company': self.company.name,
                'plan-name': self.name,
                'type': plan_type
                }


class Experience (Base):
    ''' Experience represents a particular instance of attempting to acquire insurance coverage for a specific Service. '''
    __tablename__ = 'experience'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    age = Column(Integer, nullable=True)

    plan_id = Column(Integer, ForeignKey('plan.id'), nullable=False)
    plan = relationship(Plan, backref=backref('experiences', uselist=True))

    service = Column(String(250), nullable=False)
    documented_gender = Column(Enum('M', 'F', 'U'), nullable=False)
    success = Column(Boolean, nullable=False)


class CoverageStatement (Base):
    ''' A coverage statement is a report, from a user, of whether they believe that a type of service (medication, surgery, or other) will be covered by the insurance plan based on information published by the insurance company. '''
    __tablename__ = 'coverage_statement'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)

    plan_id = Column(Integer, ForeignKey('plan.id'), nullable=False)
    plan = relationship(Plan, backref=backref('coverage_statements', uselist=True))

    service_type = Column(Enum('medication', 'surgery', 'other'), nullable=False)
    covered = Column(Enum('yes', 'no', 'unknown'), nullable=False)


class Documents (Base):
    ''' A Document is a link to a product brochure, statement of coverage, or some other useful information. It should be associated with a Coverage Statement as a way of supporting "this is what *I* was reading when I submitted my report".

    Due to time and UI design constraints, this database is not actually being used at this time.
    '''
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)

    plan_id = Column(Integer, ForeignKey('plan.id'), nullable=False)
    plan = relationship(Plan, backref=backref('documents', uselist=True))

    coverage_statement_id = Column(Integer, ForeignKey('coverage_statement.id'), nullable=False)
    coverage_statement = relationship(CoverageStatement, backref=backref('documents', uselist=True))

    date = Column(Date, nullable=False)

#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# pylint: disable=C0111

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, backref
from sqlalchemy import create_engine

Base = declarative_base()


def connect (db_path):
    engine = create_engine('sqlite:///%s' % db_path)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


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


class Incident (Base):
    __tablename__ = 'incident'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)

    plan_id = Column(Integer, ForeignKey('plan.id'), nullable=False)
    plan = relationship(Plan, backref=backref('incidents', uselist=True))

    procedure = Column(String(250), nullable=False)
    stated_gender = Column(Enum('M', 'F', 'U'), nullable=False)
    success = Column(Boolean, nullable=False)


class CoverageStatement (Base):
    __tablename__ = 'coverage_statement'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)

    plan_id = Column(Integer, ForeignKey('plan.id'), nullable=False)
    plan = relationship(Plan, backref=backref('coverage_statements', uselist=True))

    procedure = Column(String(250), nullable=False)
    covered = Column(Enum('true', 'false', 'unknown'), nullable=False)


class Documents (Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)

    plan_id = Column(Integer, ForeignKey('plan.id'), nullable=False)
    plan = relationship(Plan, backref=backref('documents', uselist=True))

    coverage_statement_id = Column(Integer, ForeignKey('coverage_statement.id'), nullable=False)
    coverage_statement = relationship(CoverageStatement, backref=backref('documents', uselist=True))

    date = Column(Date, nullable=False)

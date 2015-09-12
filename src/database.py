#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# pylint: disable=C0111

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
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
    name = Column(String(250), nullable=False)
    state = Column(String(20), nullable=False)
    color_code = Column(Enum('bronze', 'silver', 'gold', 'platinum', 'catastrophic', 'not-present'),
                        nullable=True)
    medicaid = Column(Boolean, nullable=False)


class Incident (Base):
    __tablename__ = 'incident'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    plan_id = Column(Integer, ForeignKey('plan.id'), nullable=False)
    procedure = Column(String(250), nullable=False)
    stated_gender = Column(Enum('M', 'F', 'U'), nullable=False)
    success = Column(Boolean, nullable=False)


class CoverageStatement (Base):
    __tablename__ = 'coverage_statement'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    plan_id = Column(Integer, ForeignKey('plan.id'), nullable=False)
    procedure = Column(String(250), nullable=False)
    covered = Column(Enum('true', 'false', 'unknown'), nullable=False)


class Documents (Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    plan_id = Column(Integer, ForeignKey('plan.id'), nullable=False)
    coverage_statement_id = Column(Integer, ForeignKey('coverage_statement.id'), nullable=False)
    date = Column(Date, nullable=False)

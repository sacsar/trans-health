#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# pylint: disable=C0111

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Company (Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Plan (Base):
    __tablename__ = 'plan'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('company.id'))
    name = Column(String(250), nullable=False)
    state = Column(String(20), nullable=False)
    color_code = Column(String(30), nullable=True)
    medicaid = Column(Boolean, nullable=False)

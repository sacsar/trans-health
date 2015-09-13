#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# pylint: disable=C0111

import datetime

import src.database as database

def build ():
    s = database.connect('trans-health.db')

    humana = database.Company(name='Humana')
    bcbs = database.Company(name='Blue Cross and Blue Shield')
    cigna = database.Company(name='Cigna')
    amerigroup = database.Company(name='Amerigroup')

    s.add(humana)
    s.add(bcbs)
    s.add(cigna)
    s.add(amerigroup)

    cigna = database.Plan(company=cigna,
                          name='myCigna Health Savings',
                          state='TX',
                          color_code='bronze',
                          medicaid=False)

    s.add(cigna)
    s.add(database.Plan(company=humana,
                        name='Humana Basic 6600',
                        state='TX',
                        color_code='catastrophic',
                        medicaid=False))
    s.add(database.Plan(company=humana,
                        name='blue Advantage Bronze HMO',
                        state='TX',
                        color_code='bronze',
                        medicaid=False))
    s.add(database.Plan(company=humana,
                        name='Humana Bronze 6300',
                        state='TX',
                        color_code='bronze',
                        medicaid=False))
    s.add(database.Plan(company=bcbs,
                        name='Blue Advantage Gold HMO 002',
                        state='TX',
                        color_code='gold',
                        medicaid=False))
    s.add(database.Plan(company=amerigroup,
                        name='STAR Medicaid',
                        state='TX',
                        color_code='not-present',
                        medicaid=True))

    s.add(database.CoverageStatement(date=datetime.date(2015, 8, 1),
                                     plan=cigna,
                                     service_type="medication",
                                     covered='yes'))
    s.add(database.CoverageStatement(date=datetime.date(2015, 8, 3),
                                     plan=cigna,
                                     service_type="medication",
                                     covered='yes'))
    s.add(database.CoverageStatement(date=datetime.date(2015, 8, 5),
                                     plan=cigna,
                                     service_type="medication",
                                     covered='unknown'))
    s.add(database.CoverageStatement(date=datetime.date(2014, 1, 10),
                                     plan=cigna,
                                     service_type="medication",
                                     covered='no'))

    s.add(database.Experience(date=datetime.date(2014, 12, 1),
                              age=36,
                              plan=cigna,
                              documented_gender='M',
                              service='Estradiol',
                              success=True))
    s.add(database.Experience(date=datetime.date(2015, 3, 1),
                              age=36,
                              plan=cigna,
                              documented_gender='M',
                              service='Estradiol',
                              success=True))
    s.add(database.Experience(date=datetime.date(2015, 6, 1),
                              age=36,
                              plan=cigna,
                              documented_gender='M',
                              service='Estradiol',
                              success=True))
    s.add(database.Experience(date=datetime.date(2015, 9, 1),
                              age=36,
                              plan=cigna,
                              documented_gender='M',
                              service='Estradiol',
                              success=True))
    s.add(database.Experience(date=datetime.date(2015, 12, 1),
                              age=37,
                              plan=cigna,
                              documented_gender='F',
                              service='Estradiol',
                              success=True))

    s.add(database.Experience(date=datetime.date(2014, 12, 1),
                              age=36,
                              plan=cigna,
                              documented_gender='M',
                              service='Spironolactone',
                              success=True))
    s.add(database.Experience(date=datetime.date(2015, 3, 1),
                              age=36,
                              plan=cigna,
                              documented_gender='M',
                              service='Spironolactone',
                              success=True))
    s.add(database.Experience(date=datetime.date(2015, 6, 1),
                              age=36,
                              plan=cigna,
                              documented_gender='M',
                              service='Spironolactone',
                              success=True))
    s.add(database.Experience(date=datetime.date(2015, 9, 1),
                              age=36,
                              plan=cigna,
                              documented_gender='M',
                              service='Spironolactone',
                              success=False))
    s.add(database.Experience(date=datetime.date(2015, 12, 1),
                              age=37,
                              plan=cigna,
                              documented_gender='F',
                              service='Spironolactone',
                              success=True))

    s.add(database.Experience(date=datetime.date(2015, 12, 1),
                              age=31,
                              plan=cigna,
                              documented_gender='F',
                              service='Facial Feminization',
                              success=True))

    s.commit()

build()

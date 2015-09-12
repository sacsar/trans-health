#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# pylint: disable=C0111

import database

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

    s.add(database.Plan(company=cigna,
                        name='myCigna Health Savings',
                        state='TX',
                        color_code='bronze',
                        medicaid=False))
    s.add(database.Plan(company=humana,
                        name='Humana Basic 6600',
                        state='TX',
                        color_code='catastrophic',
                        medicaid=False))
    s.add(database.Plan(company=humana,
                        name='blue Advantage Bronze',
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

    s.commit()

build()

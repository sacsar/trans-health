#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# pylint: disable=C0111
# pylint: disable=R0201
# pylint: disable=E0602

import spec
import unittest
import json
import requests

server_uri = 'http://127.0.0.1:5000'

class BasicCheck (spec.Spec, unittest.TestCase):
    def test_can_run (self):
        r = requests.get('%s/' % (server_uri,))
        self.assertEqual(r.status_code, requests.codes.ok)

    def test_get_companies (self):
        r = requests.get('%s/api/v1/companies' % (server_uri,))
        self.assertEqual(r.status_code, requests.codes.ok)
        self.assertEqual(r.json(), {"companies": ["Humana", "Blue Cross and Blue Shield", "Cigna", "Amerigroup"]})

    def test_get_plans (self):
        r = requests.get('%s/api/v1/search' % (server_uri,),
                         params={'state': 'TX'})
        self.assertEqual(r.status_code, requests.codes.ok)
        self.assertEqual(len(r.json()), 6)

        self.maxDiff = None
        target = [p for p in r.json() if p['company'] == 'Cigna' and
                                         p['plan'] == 'myCigna Health Savings' and
                                         p['state'] == 'TX'][0]

        self.assertEqual(cigna_plan, target)

    def test_get_by_exchange (self):
        r = requests.get('%s/api/v1/search' % (server_uri,),
                         params={'state': 'TX', 'exchange_code': 'bronze'})
        self.assertEqual(r.status_code, requests.codes.ok)
        self.assertEqual(len(r.json()), 3)
        self.assertIn(cigna_plan, r.json())

    # We actually have to continue skipping this one, and anything else that modifies the database, until we can build infrastructure for destroying and recreating the database. Would be nice. Must be hand tested. Much sadness.
    @unittest.skip
    def test_add_experience (self):
        payload = {'date': '2015-08-22',
                   'gender': 'M',
                   'age': 36,
                   'plan': 'blue Advantage Bronze HMO',
                   'company': 'Humana',
                   'state': 'TX',
                   'procedures': [
                        {'name': 'estradiol',
                         'success': True
                        },
                        {'name': 'spironolactone',
                         'success': True
                        }]
                  }
        r = requests.post('%s/api/v1/experience' % (server_uri,),
                          headers={'Content-Type': 'application/json'},
                          data=json.dumps(payload))
        self.assertEqual(r.status_code, requests.codes.ok)

    def test_service_list (self):
        r = requests.get('%s/api/v1/services' % (server_uri,))
        print(r.text)
        self.assertEqual(r.json().get('Estradiol'), 'medication')
        self.assertEqual(r.json().get('Facial Feminization'), 'surgery')

cigna_plan = {
    'company': 'Cigna',
    'plan': 'myCigna Health Savings',
    'state': 'TX',
    'exchange': 'bronze',
    'medicaid': False,
    'coverage': {
        'medication': {
            'yes': 2,
            'no': 1,
            'unknown': 1
        },
        'surgery': {
            'yes': 0,
            'no': 1,
            'unknown': 3
        }
    },
    'claims': {
        'medication': [
            {'name': 'Estradiol', 'yes': 5, 'no': 0, 'count': 5},
            {'name': 'Spironolactone', 'yes': 4, 'no': 1, 'count': 5}
        ],
        'surgery': [
            {'name': 'Facial Feminization', 'yes': 1, 'no': 0, 'count': 1}
        ],
        'other': []
    }
}

# [
#     {
#         "state": "TX",
#         "company": "Insurance A",
#         "plan": "Bronze Plan",
#         "exchange": null,
#         "medicaid": true,
#         "coverage": {
#             "medication": {
#                 "yes": 3,
#                 "no": 2,
#                 "unknown": 50
#             },
#             "surgery": {
#                 "yes": 3,
#                 "no": 2,
#                 "unknown": 50
#             }
#         },
#         "claims": {
#             "medication": [{
#                 "name": "hormone 1",
#                 "yes": 5,
#                 "no": 10,
#                 "count": 15
#             }],
#             "surgery": [{
#                 "name": "surgery 1",
#                 "yes": 5,
#                 "no": 10
#                 "count": 15
#             }]
#         }
#     },
#     {
#         "state": "IL",
#         "company": "Insurance B",
#         "plan": "Basic Plan",
#         "exchange": "Catastrophic",
#         "medicaid": false,
#         "coverage": {
#             "medication": {
#                 "yes": 3,
#                 "no": 2,
#                 "unknown": 50
#             },
#             "surgery": {
#                 "yes": 3,
#                 "no": 2,
#                 "unknown": 50
#             }
#         },
#         "claims": {
#             "medication": [{
#                 "name": "hormone 1",
#                 "yes": 5,
#                 "no": 10
#             }],
#             "surgery": [{
#                 "name": "surgery 1",
#                 "yes": 5,
#                 "no": 10
#             }]
#         }
#     }
# ]
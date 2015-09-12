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
        self.assertEqual(r.status_code, requests.codes.not_found)

    def test_get_companies (self):
        r = requests.get('%s/api/v1/companies' % (server_uri,))
        self.assertEqual(r.status_code, requests.codes.ok)
        self.assertEqual(r.json(), {"companies": ["Humana", "Blue Cross and Blue Shield", "Cigna", "Amerigroup"]})

    def test_get_plans (self):
        # r = requests.get('%s/api/v1/search/%s' % (server_uri, json.dumps({'state': 'TX'})))
        r = requests.get('%s/api/v1/search' % (server_uri,),
                         params={'state': 'TX'})
        self.assertEqual(r.status_code, requests.codes.ok)
        self.assertEqual(len(r.json()['plans']), 6)
        self.assertIn({'company': 'Humana', 'plan-name': 'Humana Basic 6600', 'state': 'TX', 'type': 'catastrophic'}, r.json()['plans'])

    def test_get_by_exchange (self):
        # r = requests.get('%s/api/v1/search/%s' % (server_uri, json.dumps({'state': 'TX', 'exchange': True})))
        r = requests.get('%s/api/v1/search' % (server_uri,),
                         params={'state': 'TX', 'exchange': True})
        self.assertEqual(r.status_code, requests.codes.ok)
        self.assertEqual(len(r.json()['plans']), 6)
        self.assertIn({'company': 'Humana', 'plan-name': 'blue Advantage Bronze HMO', 'state': 'TX', 'type': 'bronze'}, r.json()['plans'])

    def test_add_experience (self):
        payload = {'date': '2015-08-22',
                   'gender': 'M',
                   'age': 36,
                   'plan': 'blue Advantage Bronze HMO',
                   'company': 'Humana',
                   'procedure': [
                        {'name': 'estradiol',
                         'success': True
                        },
                        {'name': 'spironolactone',
                         'success': True
                        }]
                  }
        r = requests.post('%s/api/v1/experience' % (server_uri,),
                          headers={'Content-Type': 'application/json'},
                          data=payload)
        self.assertEqual(r.status_code, requests.codes.ok)

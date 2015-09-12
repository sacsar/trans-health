#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# pylint: disable=C0111
# pylint: disable=R0201
# pylint: disable=E0602

import spec
import unittest

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
        r = requests.get('%s/api/v1/search/TX' % (server_uri,))
        self.assertEqual(r.status_code, requests.codes.ok)
        self.assertEqual(len(r.json()['plans']), 6)
        self.assertIn({'company': 'Humana', 'plan-name': 'Humana Basic 6600', 'state': 'TX', 'type': 'catastrophic'}, r.json()['plans'])

    def test_get_by_exchange (self):
        r = requests.get('%s/api/v1/search/TX/exchange/bronze' % (server_uri,))
        self.assertEqual(r.status_code, requests.codes.ok)
        self.assertEqual(len(r.json()['plans']), 3)
        self.assertIn({'company': 'Humana', 'plan-name': 'blue Advantage Bronze HMO', 'state': 'TX', 'type': 'bronze'}, )


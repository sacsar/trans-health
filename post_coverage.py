#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import json
import requests

server_uri = 'http://127.0.0.1:5000'

coverage_report = {'date': '2015-08-22',
                   'plan': 'blue Advantage Bronze HMO',
                   'company': 'Humana',
                   'state': 'TX',
                   'service_types': [
                        {'name': 'medication', 'covered': 'yes' },
                        {'name': 'surgery', 'covered': 'yes' }
                        ]
                  }
r = requests.post('%s/api/v1/coverage' % (server_uri,),
                  headers={'Content-Type': 'application/json'},
                  data=json.dumps(coverage_report))
print(r.status_code)

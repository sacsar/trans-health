#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import json
import requests

server_uri = 'http://127.0.0.1:5000'

experience_report = {'date': '2015-08-22',
                     'gender': 'M',
                     'age': 36,
                     'plan': 'blue Advantage Bronze HMO',
                     'company': 'Humana',
                     'state': 'TX',
                     'services': [
                          {'name': 'Estradiol',
                           'success': True
                          },
                          {'name': 'Spironolactone',
                           'success': True
                          }]
                    }
r = requests.post('%s/api/v1/experience' % (server_uri,),
                  headers={'Content-Type': 'application/json'},
                  data=json.dumps(experience_report))
print(r.status_code)

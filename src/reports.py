#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# pylint: disable=C0111
'''
Reports are utility functions that summarize (or report) information. Generally these are specific reports and are in support of the web API, but would clutter up the app module.
'''

def plan_summary (plan):
    ''' Summarize a plan for return to the client software. This report formats the basic data of the plan and tallys up the submitted coverage information and the submitted service experiences.
    '''

    return {
        'company': plan.company.name,
        'plan': plan.name,
        'state': plan.state,
        'exchange': plan.color_code,
        'medicaid': plan.medicaid,
        'coverage': {
            'medication': {
                'yes': len(scan_coverage(plan.coverage_statements, 'medication', 'yes')),
                'no': len(scan_coverage(plan.coverage_statements, 'medication', 'no')),
                'unknown': len(scan_coverage(plan.coverage_statements, 'medication', 'unknown'))
                },
            'surgery': {
                'yes': len(scan_coverage(plan.coverage_statements, 'surgery', 'yes')),
                'no': len(scan_coverage(plan.coverage_statements, 'surgery', 'no')),
                'unknown': len(scan_coverage(plan.coverage_statements, 'surgery', 'unknown'))
                }
            },
        'claims': tally_experiences(plan.experiences)
        }


''' This data structure relates a particular service to a service type. '''
service_types = {
    'Cyproterone': 'medication',
    'Spironolactone': 'medication',
    'Finasteride': 'medication',
    'Estradiol': 'medication',
    'Progesterone': 'medication',
    'Testosterone': 'medication',
    'GnRH analogue': 'medication',
    'Facial Feminization': 'surgery',
    'Mastectomy': 'surgery',
    'Phalloplasty': 'surgery',
    'Vaginaplasty': 'surgery',
    'Labiaplasty': 'surgery',
    'Breast Augmentation': 'surgery',
    'Orchiectomy': 'surgery',
    'Hystorectomy': 'surgery',
    'Oophorectomy': 'surgery',
    'Metoidioplasty': 'surgery',
    'Therapy': 'other',
    'Voice Training': 'other'
    }

def scan_coverage (statements, service_type, status):
    ''' Just get all of the coverage statements that match the specified service type and whether the reporter thought the service type was covered. '''
    return [s for s in statements if s.service_type == service_type and s.covered == status]


def tally_experiences (experiences):
    ''' Tally the result of all of the service experiences, focusing on whether the health plan covered the service requested.
    '''
    results = {}
    for exp in experiences:
        if exp.service not in results:
            results[exp.service] = {'yes': 0, 'no': 0}
        if exp.success:
            results[exp.service]['yes'] += 1
        else:
            results[exp.service]['no'] += 1

    # TODO It is rather ugly how I am doing this transformation. Perhaps I can change it one day.
    tr = {'medication': [],
          'surgery': [],
          'other': []
         }
    for (service, counts) in results.items():
        type_ = service_types[service]
        tr[type_].append({ 'name': service,
                           'yes': counts['yes'],
                           'no': counts['no'],
                           'count': counts['yes'] + counts['no']
                         })

    # These are getting sorted in part because it makes the structure easier to test, but also because it will improve the user experience if the UI does not provide any sorting.
    tr['medication'] = sorted(tr['medication'], key=lambda x: x['name'])
    tr['surgery'] = sorted(tr['surgery'], key=lambda x: x['name'])
    tr['other'] = sorted(tr['other'], key=lambda x: x['name'])
    return tr


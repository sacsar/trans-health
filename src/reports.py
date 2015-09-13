#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# pylint: disable=C0111


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
            'hormones': {
                'yes': len(scan_coverage(plan.coverage_statements, 'Hormone Replacement Therapy', 'true')),
                'no': len(scan_coverage(plan.coverage_statements, 'Hormone Replacement Therapy', 'false')),
                'unknown': len(scan_coverage(plan.coverage_statements, 'Hormone Replacement Therapy', 'unknown'))
                },
            'surgery': {
                'yes': len(scan_coverage(plan.coverage_statements, 'Surgery', 'true')),
                'no': len(scan_coverage(plan.coverage_statements, 'Surgery', 'false')),
                'unknown': len(scan_coverage(plan.coverage_statements, 'Surgery', 'unknown'))
                }
            },
        'claims': tally_experiences(plan.incidents)
        }


care_types = {
    'Cyproterone': 'hormones',
    'Spironolactone': 'hormones',
    'Finasteride': 'hormones',
    'Estradiol': 'hormones',
    'Progesterone': 'hormones',
    'Testosterone': 'hormones',
    'GnRH analogue': 'hormones',
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

def scan_coverage (statements, procedure, status):
    ''' Just get all of the coverage statements that match the specified procedure type and whether the reporter thought the procedure type was covered. '''
    return [s for s in statements if s.procedure == procedure and s.covered == status]


def tally_experiences (experiences):
    ''' Tally the result of all of the service experiences, focusing on whether the health plan covered the service requested.
    '''
    results = {}
    for exp in experiences:
        if exp.procedure not in results:
            results[exp.procedure] = {'yes': 0, 'no': 0}
        if exp.success:
            results[exp.procedure]['yes'] += 1
        else:
            results[exp.procedure]['no'] += 1

    # TODO It is rather ugly how I am doing this transformation. Perhaps I can change it one day.
    tr = {'hormones': [],
          'surgery': [],
          'other': []
         }
    for (procedure_name, counts) in results.items():
        type_ = care_types[procedure_name]
        tr[type_].append({ 'name': procedure_name,
                           'yes': counts['yes'],
                           'no': counts['no'],
                           'count': counts['yes'] + counts['no']
                         })

    # These are getting sorted in part because it makes the structure easier to test, but also because it will improve the user experience if the UI does not provide any sorting.
    tr['hormones'] = sorted(tr['hormones'], key=lambda x: x['name'])
    tr['surgery'] = sorted(tr['surgery'], key=lambda x: x['name'])
    tr['other'] = sorted(tr['other'], key=lambda x: x['name'])
    return tr


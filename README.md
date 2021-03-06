% Transition Related Health Care Database

*   By company/plan(?)
    *   What procedures are covered
    *   What hormones are covered
    *   What do they claim is covered
    *   What experience have people actually had with the coverage

*   Instructions for gathering information about your plan
    *   Exclusions
    *   Formulary
    *   Coverage limits (when they only pay $5 for surgery)


----

Procedures
==========

Medications
-----------
*   cyproterone
*   spironolactone
*   finasteride
*   estradiol
*   progesterone
*   testosterone
*   GnRH analogue

Delivery Methods for Medications
--------------------------------
*   pill
*   transdermal
*   injectable
*   implanted
*   long-lasting injection

Surgeries
---------
*   Facial Feminization
*   Mastectomy
*   Phalloplasty
*   Vaginaplasty
*   Labiaplasty
*   Breast Augmentation
*   Orchiectomy
*   Hystorectomy
*   Oophorectomy
*   Metoidioplasty

Others
------
*   Therapy/Counselling
*   Voice Retraining

Database Structure
==================

Procedure Incident
------------------
*   Date
*   Plan ID
*   Procedure
*   Stated Gender (M/F/??? because it is possible to not know what gender your provider put on the application)
*   Success

Coverage Statement
------------------
*   Date
*   Plan ID
*   Procedure
*   Claims to be covered (Yes / No / Unknown)

Documents
---------
*   Plan ID
*   Coverage Statement ID
*   Date
*   MD5
*   Path on disk

Plan
----
*   Plan ID
*   Company ID
*   Name
*   State
*   Exchange color code (bronze, silver, gold, platinum, catastrophic, not-present, NULL)
*   Medicaid (yes/no)

Flask API
=========

Endpoints
---------
*   POST /api/v1/experience
*   POST /api/v1/plan
*   GET /api/v1/search
    *   state (required)
    *   dimension: one-of "company", "procedure", "exchange", "plan" (optional)
    *   values (required if dimension is provided)
    *   { 'plans': [plan response] }
*   GET /api/v1/companies
    *   { 'companies': [ list of companies ] }

API Data Structures
-------------------
Report JSON:

    { date:
      gender:
      age:
      plan:
      company:
      procedures: [ { name:
                     success:
                    }
                 ]
      }

Plan JSON (for POST):

    { state:
      company:
      plan-name:
      type: (medicaid, private, bronze, silver, gold, platinum, catastrophic)
      exclusions: (all transition-related care, surgery, hormones)
      plan-document: file/link
      coverage-criteria: file/link
      formulary: file/link
    }

Plan Reponse:

    { state:
      company:
      plan-name:
      type:
      plan-document-available:
      coverage-criteria-availabe:
      formulary-available:
    }

Reports and Views
=================
Reporting Plan Information
--------------------------
*   Date
*   Plan
*   Procedure { name, included/excluded }

Reporting an Experience
-----------------------
*   Date
*   Plan
*   Gender on Insurance
*   Age
*   Procedure { name, covered/not covered }

View for a specific plan
------------------------
*   Company
*   Plan name
*   List of procedures
    *   stated info
    *   experiential info
    *   info: covered, not/covered

        The information would be a tally of reports, potentially broken down by time period so that if a plan changes what they cover, that can be made visible

Searches
--------
*   Plans by company
*   Plans by state
*   Plans by procedure
*   Plans on the exchange
*   Medicaid plans

I do not know what the search should make easily visible.


Database Access
===============

    (env)savanni@conway:~/src/trans-health$ PYTHONPATH=src python
    Python 3.4.3 (default, Mar 26 2015, 22:03:40)
    [GCC 4.9.2] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import database
    >>> s = database.connect('trans-health.db')
    >>> s.query(database.Company).all()
    [<database.Company object at 0x7f29e4a5dd30>]
    >>> s.add(database.Plan(company_id=1, name='Super Plan!', state='TX', color_code='None', medicaid=True)
    ... )
    >>> s.query(database.Plan).all()
    [<database.Plan object at 0x7f29e4a885c0>]

To-Do
=====
*   Need to allow for people submitting/updating plans that already exist

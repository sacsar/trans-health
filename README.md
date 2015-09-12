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
*   PUT /incident
*   PUT /
*   ????

API Data Structures
-------------------
Report JSON:

    { date:
      gender:
      age:
      plan:
      company:
      procedure: [ { name:
                     success:
                    }
                 ]
      }

Plan JSON:

    { state:
      company:
      plan-name:
      type: (medicaid, private, bronze, silver, gold, platinum, catastrophic)
      exclusion: yes/no
      plan-document: file/link
      coverage-criteria: file/link
      formulary: file/link
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
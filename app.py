from flask import Flask, jsonify, g, request, make_response
import urllib.parse
import json
import datetime

import src.database as database


app = Flask(__name__)

# DB connection, stuff

@app.before_request
def before_request():
    g.db = database.connect('trans-health.db')

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.commit()
        db.close()

# Add some API routes

@app.route('/api/v1/experience', methods=['POST'])
def post_experience():
    data = request.get_json()
    # need to look up plan and company
    plan = plan_by_company_name(g.db,
                                data['company'],
                                data['plan'],
                                data['state'])
    # there may be multiple procedures in one request
    incidents = []
    for procedure in data['procedures']:
        incident = database.Incident(date=datetime.datetime.strptime(data['date'], '%Y-%m-%d'),
                                           plan_id=plan.id,
                                           stated_gender=data['gender'],
                                           procedure=procedure['name'],
                                           success=procedure['success'],
                                           age=data['age'])
        incidents.append(incident)
    g.db.add_all(incidents)
    g.db.commit()
    r = make_response()
    r.status_code = 200
    return r

@app.route('/api/v1/plan', methods=['POST'])
def post_plan():
    data = request.get_json()
    # check if the plan exists
    add = True
    if add:
        # lookup company
        company = company_by_name(data['company'])
        if company is None:
            # add the company
            g.db.add(database.Company(name=name))
            plan = database.Plan(state=data['state'],
                                 type=data['type'],
                                 exclusions=data['exclusions'],
                                 company=company)
            g.db.add(plan)
            g.db.commit()
    r = make_response()
    r.status_code = 200
    return r

@app.route('/api/v1/search/<search_string>')
def search_plan(search_string):
    params = json.loads(urllib.parse.unquote_plus(search_string))
    state = params['state']
    dimension = params.get('dimension')
    values = params.get('values')
    results = []
    query = g.db.query(database.Plan).filter(database.Plan.state == state)
    if dimension == 'company':
        company = company_by_name(g.db, values[0])
        if company is None:
            results = []
        else:
            results = [p.to_dict() for p in company.plans]
    elif dimension == 'procedure':
        # looking for plans where someone has reported coverage
        results = []
    elif dimension == 'exchange':
        if values[0] == 'true':
            query = query.filter(database.Plan.color_code != 'not-present')
            results = [p.to_dict() for p in query.all()]
        elif values[0] == 'false':
            query = query.filter(database.Plan.color_code == 'not-present')
            results = [p.to_dict() for p in query.all()]
    elif dimension == 'plan':
        plan = plan_by_company_name(g.db, values[0], values[1], state)
        results = [plan.to_dict()]
    elif dimension is None:
        results = [p.to_dict() for p in query.all()]
    return jsonify({'plans': results})

@app.route('/api/v1/companies')
def company_list():
    companies = g.db.query(database.Company).all()
    return jsonify({'companies': [c.name for c in companies]})

def company_by_name(session, name):
    company = session.query(database.Company).filter(database.Company.name == name).all()
    return company[0] if len(company) > 0 else None

def plan_by_company_name(session, company, plan_name, state):
    company = company_by_name(session, company)
    plan = [p for p in company.plans if p.state == state
            and p.name == plan_name][0]
    return plan

if __name__ == '__main__':
    app.run(debug=True)
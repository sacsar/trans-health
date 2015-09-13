from flask import Flask, jsonify, g, request, make_response, send_from_directory
import urllib.parse
import json
import datetime
import requests

import src.database as database
import src.reports as reports


app = Flask(__name__)

# DB connection, stuff

def build_response (json_content=None):
    response = make_response()
    # copied this from http://stackoverflow.com/questions/49547/making-sure-a-web-page-is-not-cached-across-all-browsers
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate" # HTTP 1.1.
    response.headers["Pragma"] = "no-cache" # HTTP 1.0.
    response.headers["Expires"] = "0" # Proxies.   r.status_code = 200

    if json_content:
        response.status_code = requests.codes.ok
        response.headers['Content-type'] = 'application/json'
        response.data = json.dumps(json_content)
    else:
        response.status_code = requests.codes.no_content

    return response


@app.before_request
def before_request():
    g.db = database.connect('trans-health.db')

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.commit()
        db.close()

@app.route('/')
def index():
    return send_from_directory('', 'index.html', cache_timeout=0)

@app.route('/app/<path:path>')
def js(path):
    return send_from_directory('app', path, cache_timeout=0)

# Add some API routes

@app.route('/api/v1/experience', methods=['POST'])
def post_experience():
    data = request.get_json()
    # need to look up plan and company
    plan = database.plan_by_company_name(g.db,
                                         data['company'],
                                         data['plan'],
                                         data['state'])
    if plan is None:
        plan = database.create_plan(g.db, data['company'], data['plan'], data['state'])

    def make_experience (service_data):
        return database.Experience(
                    date=datetime.datetime.strptime(service_data['date'], '%Y-%m-%d'),
                    plan=plan,
                    documented_gender='U',
                    service=service_data['name'],
                    success=service_data['success'],
                    age=service_data['age'])

    # there may be multiple services in one request
    experiences = [make_experience(service_data) for service_data in data['services']]
    g.db.add_all(experiences)
    g.db.commit()
    return build_response()

@app.route('/api/v1/coverage', methods=['POST'])
def post_coverage():
    data = request.get_json()
    # look up by plan and company
    plan = database.plan_by_company_name(g.db,
                                         data['company'],
                                         data['plan'],
                                         data['state'])
    if plan is None:
        plan = database.create_plan(g.db, data['company'], data['plan'], data['state'])

    def make_coverage (service_type_data):
        return database.CoverageStatement(
                    date=datetime.datetime.strptime(data['date'], '%Y-%m-%d'),
                    plan=plan,
                    service_type=service_type_data['name'],
                    covered=service_type_data['covered'])

    # there may be multiple service_types in one request
    coverage_reports = [make_coverage(service_type_data)
                        for service_type_data in data['service_types']]
    g.db.add_all(coverage_reports)
    g.db.commit()
    return build_response()

@app.route('/api/v1/search')
def search_plan():
    state           = request.args.get('state')
    exchange_code   = request.args.get('exchange_code')
    plan_name       = request.args.get('plan_name')

    def plan_filter (plan):
        if exchange_code and plan.color_code != exchange_code:
            return False
        if plan_name and not re.search(plan_name, plan.name):
            return False
        return True


    plans = g.db.query(database.Plan).filter(database.Plan.state == state).all()
    matching_plans = filter(plan_filter, plans)

    return build_response(json_content=[reports.plan_summary(p) for p in matching_plans])

@app.route('/api/v1/companies')
def company_list():
    companies = g.db.query(database.Company).all()
    return build_response(json_content={'companies': [c.name for c in companies]})

@app.route('/api/v1/plans')
def plans_list():
   the_plans = g.db.query(database.Plan).all()
   return build_response(json_content=[{'state': p.state,
                                'company': p.company.name,
                                'plan': p.name}
                                 for p in the_plans])

@app.route('/api/v1/services')
def service_list():
    return build_response(json_content=reports.service_types)

if __name__ == '__main__':
    app.run(debug=True)

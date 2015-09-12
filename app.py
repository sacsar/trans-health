from flask import Flask, jsonify, g, request
import src.database as database


app = Flask(__name__)

# DB connection, stuff

@app.before_request
def before_request():
	g.db = database.connect('trans-health.db'))

@app.teardown_request
	db = getattr(g, 'db', None)
    if db is not None:
    	db.commit()
        db.close()

# Add some API routes

@app.route('/api/v1/experience', methods=['POST'])
def post_experience():
	experience_data = resquest.get_json()
	# need to look up plan and company

@app.route('/api/v1/plan', methods=['POST'])
def post_plan():
	data = request.get_json()
	# check if the plan exists
	add = True
	# lookup company
	company = g.db.query(database.Company).filter(Company.name == data['name']).all()
	if company == []:
		# need to make a new company
		pass
	else:
		company = company[0]
	if add:
		plan = database.Plan(state=data['state'],
							 type=data['type'],
							 exclusions=data['exclusions'],
							 company=company)
		g.db.add(plan)
		g.db.commit()

@app.route('/api/v1/search/<state>')
@app.route('/api/v1/search/<state>/<dimension>/<value>')
def search_plan(state, dimension, value):
	pass

@app.route('/api/v1/companies')
def company_list():
	companies = g.db.query(database.Company).all()
	return jsonify({'companies': companies})

if __name__ == '__main__':
	app.run(debug=True)
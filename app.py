from flask import Flask, jsonify

app = Flask(__name__)

# Add some API routes

@app.route('/api/v1/experience', methods=['POST'])
def post_experience():
	pass


@app.route('/api/v1/plan', methods=['POST'])
def post_plan():
	pass

@app.route('/api/v1/search/<state>')
@app.route('/api/v1/search/<state>/<dimension>/<value>')
def search_plan(state, dimension, value):
	pass

if __name__ == '__main__':
	app.run(debug=True)
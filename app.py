from flask import Flask, request, jsonify, json
from flask_cors import CORS
from routes import breaches
from routes import safebrowsing
from routes import datastore
app = Flask(__name__)

CORS(app, resources={r"//*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/monthly_analytics', methods=['GET'])
def get_monthly_analytics():
    request_content = request.get_json(silent=False)

    

@app.route('/url_analysis', methods=['GET'])
def analyze_url():
    request_content = request.get_json(silent=False)
    print(request)
    print(request.__dict__)
    print(request_content)

    url = request_content.get('url', None)
    user_email = request_content.get('user_email', None)
    
    if not url:
        response = {}
        response['ERROR'] = 'No url found'
        return jsonify(response)

    if not user_email:
        response = {}
        response['ERROR'] = 'No email found'
        return jsonify(response)

    response = safebrowsing.safety_analysis(user_email=user_email, visited_url=url)
    return jsonify(response)

@app.route('/ack_breach', methods=['POST'])
def acknowledge_breach():
    request_content = request.get_json(silent=False)

    user_email = request_content.get('user_email', None)
    breach_name = request_content.get('breach_name', None)

    if not user_email:
        response = {}
        response['ERROR'] = 'No email found'
        return jsonify(response)

    if not breach_name:
        response = {}
        response['ERROR'] = 'No breach name found'
        return jsonify(response)

    result = datastore.ack_breach(user_email=user_email, breach_name=breach_name)
    if result:
        response = {}
        response['MESSAGE'] = 'Acknowledgement received'
        return jsonify(response)
    response = {}
    response['ERROR'] = 'Acknowledgement received, but error occurred'
    return jsonify(response)


@app.route('/breaches', methods=['GET'])
def find_user_breaches():
    request_content = request.get_json(silent=False)

    user_email = request_content.get('user_email', None)
    
    if not user_email:
        response = {}
        response['ERROR'] = 'No email found'
        return jsonify(response)

    response = breaches.get_all_breaches_for_user(user_email)
    return jsonify(response)

@app.route('/test_get/', methods=['GET'])
def respond():
    test_data = request.args.get('test', None)

    response = {}

    if not test_data:
        response["ERROR"] = "No Test data found"
    else:
        response["MESSAGE"] = f"Here is the test: {test_data}"

    return jsonify(response)

@app.route('/test_post/', methods=['POST'])
def post():
    param = request.form.get('test')
    if param:
        return jsonify({
            "message": f'You have posted {param}',
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "No test param found"
        })

@app.route('/sign_up', methods=['GET'])
def sign_up():
    request_content = request.get_json(silent=False)
    user_email = request_content.get('user_email', None)

    if not user_email:
        response = {}
        response['ERROR'] = 'No email found'
        return jsonify(response)

    request_content = request.get_json(silent=False)
    password = request_content.get('password', None)

    if not password:
        response = {}
        response['ERROR'] = 'No password found'
        return jsonify(response)

    response = authflow.sign_up_auth(user_email,password)
    return jsonify(response)

@app.route('/sign_in', methods=['GET'])
def sign_in():
    request_content = request.get_json(silent=False)
    user_email = request_content.get('user_email', None)

    if not user_email:
        response = {}
        response['ERROR'] = 'No email found'
        return jsonify(response)

    request_content = request.get_json(silent=False)
    password = request_content.get('password', None)

    if not password:
        response = {}
        response['ERROR'] = 'No password found'
        return jsonify(response)
    
    response = authflow.sign_in_auth(user_email,password)
    return jsonify(response)

@app.route('/')
def index():
    return "<h1>SecureSurf Backend Server</h1>"

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
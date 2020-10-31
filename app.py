from flask import Flask, request, jsonify, json
from flask_cors import CORS
from routes import breaches
from routes import safebrowsing
from routes import datastore
from routes import analytics
from routes import authflow
from routes.cron_tasks import poll_breaches_for_all_users
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

app = Flask(__name__)

CORS(app, resources={r"//*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=poll_breaches_for_all_users,
    trigger=IntervalTrigger(hours=3),
    id='poll',
    name='Poll All',
    replace_existing=True)
atexit.register(lambda: scheduler.shutdown())

@app.route('/update_breach_watch_list', methods=['POST'])
def update_watch_list():
    request_content = request.get_json(silent=False)

    user_email = request_content.get('user_email', None)
    breach_watch_list = request_content.get('breach_watch_list', None)

    if not user_email:
        response = {}
        response['ERROR'] = 'No email found'
        return jsonify(response)

    if not breach_watch_list:
        response = {}
        response['ERROR'] = 'No updates found'
        return jsonify(response)

    datastore.log_ip(request.environ['REMOTE_ADDR'], user_email)
    
    datastore.update_breach_watch_list(user_email, breach_watch_list)
    return jsonify({"MESSAGE": "Checks out"})


@app.route('/monthly_analytics_aggregated', methods=['POST'])
def get_monthly_analytics_aggregated():
    request_content = request.get_json(silent=False)

    user_email = request_content.get('user_email', None)
    month = request_content.get('month', None)

    if not user_email:
        response = {}
        response['ERROR'] = 'No email found'
        return jsonify(response)

    if not month:
        response = {}
        response['ERROR'] = 'No month found'
        return jsonify(response)

    datastore.log_ip(request.environ['REMOTE_ADDR'], user_email)


    aggregated_records = analytics.get_aggregated_records(user_email=user_email, month=month)
    return jsonify(aggregated_records)

@app.route('/monthly_analytics_detailed', methods=['POST'])
def get_monthly_analytics_detailed():
    request_content = request.get_json(silent=False)

    user_email = request_content.get('user_email', None)
    month = request_content.get('month', None)

    if not user_email:
        response = {}
        response['ERROR'] = 'No email found'
        return jsonify(response)

    if not month:
        response = {}
        response['ERROR'] = 'No month found'
        return jsonify(response)

    datastore.log_ip(request.environ['REMOTE_ADDR'], user_email)


    detailed_records = analytics.get_detailed_records(user_email=user_email, month=month)
    return jsonify(detailed_records)

@app.route('/url_analysis', methods=['POST'])
def analyze_url():
    request_content = request.get_json(silent=False)

    url = request_content.get('url', None)
    user_email = request_content.get('user_email', None)
    request_ip = request.environ['REMOTE_ADDR']
    
    if not url:
        response = {}
        response['ERROR'] = 'No url found'
        return jsonify(response)

    if not user_email:
        response = {}
        response['ERROR'] = 'No email found'
        return jsonify(response)

    datastore.log_ip(request.environ['REMOTE_ADDR'], user_email)


    response = safebrowsing.safety_analysis(user_email=user_email, visited_url=url, remote_ip=request_ip)
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
    datastore.log_ip(request.environ['REMOTE_ADDR'], user_email)


    result = datastore.ack_breach(user_email=user_email, breach_name=breach_name)
    if result:
        response = {}
        response['MESSAGE'] = 'Acknowledgement received'
        return jsonify(response)
    response = {}
    response['ERROR'] = 'Acknowledgement received, but error occurred'
    return jsonify(response)


@app.route('/breaches', methods=['POST'])
def find_user_breaches():
    request_content = request.get_json(silent=False)

    user_email = request_content.get('user_email', None)
    
    if not user_email:
        response = {}
        response['ERROR'] = 'No email found'
        return jsonify(response)

    datastore.log_ip(request.environ['REMOTE_ADDR'], user_email)


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

@app.route('/sign_up', methods=['POST'])
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

    request_content = request.get_json(silent=False)
    first_name = request_content.get('first_name', None)

    if not first_name:
        response = {}
        response['ERROR'] = 'No first name found'
        return jsonify(response)

    request_content = request.get_json(silent=False)
    phone = request_content.get('phone', None)

    if not phone:
        response = {}
        response['ERROR'] = 'No phone number found'
        return jsonify(response)

    ip = request.environ['REMOTE_ADDR']
    response = authflow.sign_up_auth(user_email,password,first_name,phone,ip)

    return jsonify(response)

@app.route('/sign_in', methods=['POST'])
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

    ip = request.environ['REMOTE_ADDR']
    datastore.log_ip(ip, user_email)
    
    response = authflow.sign_in_auth(user_email,password)
    return jsonify(response)

@app.route('/')
def index():
    return "<h1>SecureSurf Backend Server</h1>"


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
    atexit.register(lambda: scheduler.shutdown())
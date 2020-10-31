from flask import Flask, request, jsonify
app = Flask(__name__)

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

@app.route('/')
def index():
    return "<h1>SecureSurf Backend Server</h1>"

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
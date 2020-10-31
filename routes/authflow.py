import pyrebase
from flask import Flask, request, jsonify
from .settings import FIREBASE_CONFIG
app = Flask(__name__)

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
auth = firebase.auth()

def sign_in_auth(user_email, password):
    try:
        auth.sign_in_with_email_and_password(user_email, password)
        response = {}
        response = 'Sign In Successful'
        return jsonify(response)
    except:
        response = {}
        response['ERROR'] = 'Invalid email/password combination'
        return jsonify(response)

def sign_up_auth(user_email,password):
    try:
        auth.create_user_with_email_and_password(user_email, password)
        response = {}
        response = 'Sign Up Successful'
        return jsonify(response)
    except:
        response = {}
        response['ERROR'] = 'Email already exists'
        return jsonify(response)



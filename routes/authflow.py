import pyrebase
from .settings import FIREBASE_CONFIG\
import .datastore

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
auth = firebase.auth()

def sign_in_auth(user_email, password):
    try:
        auth.sign_in_with_email_and_password(user_email, password)
        response = {}
        response['MESSAGE'] = 'Sign In Successful'
        return response
    except:
        response = {}
        response['ERROR'] = 'Invalid email/password combination'
        return response

def sign_up_auth(user_email,password,first_name,phone):  
    try:
        auth.create_user_with_email_and_password(user_email, password)
        response = {}
        response['MESSAGE'] = 'Sign Up Successful'
    except:
        response = {}
        response['ERROR'] = 'Email already exists'
    
    datast

    return response


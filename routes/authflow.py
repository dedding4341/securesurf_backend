import pyrebase
from .settings import FIREBASE_CONFIG

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
auth = firebase.auth()
db = firebase.database()

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
    
    user_email = user_email.replace('@', '')
    user_email = user_email.replace('.', '')
    
    phone = "+1" + phone

    db.child("users").child(user_email).child("user_info").set({'first_name': first_name, 'phone': phone})

    return response

def log_ip(ip, user_email):
    user_email = user_email.replace('@', '')
    user_email = user_email.replace('.', '')

    try:
        known_addr = db.child("users").child(user_email).get()
        known_ips = known_addr.val().get('known_ip_addresses', None)
    except:
        known_ips = None
    
    new_ip = [ip]

    if not known_ips:
        db.child("users").child(user_email).update({'known_ip_addresses': new_ip})
    else:
        updated_ips = known_ips + list(set(new_ip) - set(known_ips))
        db.child("users").child(user_email).update({'known_ip_addresses': updated_ips})

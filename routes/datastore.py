import pyrebase
from .settings import FIREBASE_CONFIG
import datetime
from datetime import timezone

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
db = firebase.database()

month_set = ['January', 'February', 'March', 'April', 'March', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def load_compromised_sites(user_email, detailed_breach_info):
    acknowledged_data = None
    unacknowledged_data = None
    
    # strip forbidden characters for DB interactions
    user_email = user_email.replace('@', '')
    user_email = user_email.replace('.', '')

    try:
        acknowledged_data = db.child("users").child(user_email).child("acknowledged").get()
        acknowledged_names = acknowledged_data.val().get('breach_names', None)
    except:
        acknowledged_names = None
    
    try:
        unacknowledged_data = db.child("users").child(user_email).child("unacknowledged").get()
        unacknowledged_names = unacknowledged_data.val().get('breach_names', None)
    except:
        unacknowledged_names = None

    breach_names = []

    for breach in detailed_breach_info:
        if acknowledged_names and breach['Name'] in acknowledged_names:
            continue
        elif unacknowledged_names and breach['Name'] in unacknowledged_names:
            continue
        else:
            breach_names.append(breach['Name'])
    
    if len(breach_names) == 0:
        return

    # init new datastore
    if not unacknowledged_names:
        db.child("users").child(user_email).child("unacknowledged").set({"breach_names": breach_names})
    else:
        updated_names = unacknowledged_names + list(set(breach_names) - set(unacknowledged_names))
        db.child("users").child(user_email).child("unacknowledged").update({"breach_names": updated_names})

def sanitize_return(user_email, detailed_breach_info):
    acknowledged_data = None
    unacknowledged_data = None
    
    # strip forbidden characters for DB interactions
    user_email = user_email.replace('@', '')
    user_email = user_email.replace('.', '')
    
    try:
        unacknowledged_data = db.child("users").child(user_email).child("unacknowledged").get()
        unacknowledged_names = unacknowledged_data.val().get('breach_names', None)
    except:
        unacknowledged_names = None

    return unacknowledged_names
    
def ack_breach(user_email, breach_name):
    acknowledged_data = None
    unacknowledged_data = None
    
    # strip forbidden characters for DB interactions
    user_email = user_email.replace('@', '')
    user_email = user_email.replace('.', '')
    
    try:
        unacknowledged_data = db.child("users").child(user_email).child("unacknowledged").get()
        unacknowledged_names = unacknowledged_data.val().get('breach_names', None)
    except:
        unacknowledged_names = None
    
    try:
        acknowledged_data = db.child("users").child(user_email).child("acknowledged").get()
        acknowledged_names = acknowledged_data.val().get('breach_names', None)
    except:
        acknowledged_names = None

    try:
        unacknowledged_names.remove(breach_name)
        acknowledged_names.append(breach_name)

        db.child("users").child(user_email).child("unacknowledged").update({"breach_names": unacknowledged_names})
        db.child("users").child(user_email).child("acknowledged").update({"breach_names": acknowledged_names})
        return True
    except:
        return False
    
def record_url_visit(user_email, url):
    user_email = user_email.replace('@', '')
    user_email = user_email.replace('.', '')

    dt_now = datetime.datetime.now(tz=timezone.utc)
    date_year_bucket = f'{month_set[dt_now.month - 1]}-{dt_now.year}'

    db.child("users").child(user_email).child(date_year_bucket).push({"url": url, "timestamp": dt_now.strftime("%m/%d/%Y, %H:%M:%S")})

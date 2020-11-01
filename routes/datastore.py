import pyrebase
from .settings import FIREBASE_CONFIG
import datetime
from datetime import timezone
from .twilio_service import send_sms_new_breach
from .location_service import location_check, get_offending_location

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
db = firebase.database()

month_set = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

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

    if (detailed_breach_info[0:3] == '404'):
        return


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

def polling_load_compromised_sites(user_email, detailed_breach_info):
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
    
    if (detailed_breach_info[0:3] == '404'):
        return

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

    
    if not unacknowledged_names:
        db.child("users").child(user_email).child("unacknowledged").set({"breach_names": breach_names})
    else:
        updated_names = unacknowledged_names + list(set(breach_names) - set(unacknowledged_names))
        db.child("users").child(user_email).child("unacknowledged").update({"breach_names": updated_names})
    user = get_user(user_email=user_email)

    send_sms_new_breach(to_number=user.get('phone', None), user_name=user.get('first_name', None))

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
        unacknowledged_names = []
    
    try:
        acknowledged_data = db.child("users").child(user_email).child("acknowledged").get()
        acknowledged_names = acknowledged_data.val().get('breach_names', None)
    except:
        acknowledged_names = []

    try:
        unacknowledged_names.remove(breach_name)
        acknowledged_names.append(breach_name)

        db.child("users").child(user_email).child("unacknowledged").update({"breach_names": unacknowledged_names})
        print("h")
        try:
            db.child("users").child(user_email).child("acknowledged").update({"breach_names": acknowledged_names})
        except:
            db.child("users").child(user_email).child("acknowledged").set({"breach_names": acknowledged_names})
        return True
    except :
        return False
    
def record_url_visit(user_email, url, remote_ip):
    user_email = user_email.replace('@', '')
    user_email = user_email.replace('.', '')

    dt_now = datetime.datetime.now(tz=timezone.utc)
    date_year_bucket = f'{month_set[dt_now.month - 1]}-{dt_now.year}'

    db.child("users").child(user_email).child(date_year_bucket).push({"url": url, "timestamp": dt_now.strftime("%m/%d/%Y, %H:%M:%S"), "remote_ip": remote_ip})

def load_browsing_data(user_email, date_year_bucket):
    user_email = user_email.replace('@', '')
    user_email = user_email.replace('.', '')

    data = db.child("users").child(user_email).child(date_year_bucket).get()
    print(data)

    data_entries = []
    try:
        for entry in data.each():
            print("run")
            data_entries.append((entry.val().get('url'), entry.val().get('timestamp'), entry.val().get('remote_ip')))
    except:
        return data_entries
    return data_entries

def log_ip(ip, user_email):
    user_email = user_email.replace('@', '')
    user_email = user_email.replace('.', '')

    try:
        known_addr = db.child("users").child(user_email).get()
        known_ips = known_addr.val().get('known_ip_addresses', None)
    except:
        known_ips = None

    try:
        if not ip_check(ip, known_ips):
            user = get_user(user_email=user_email)
            city, region = get_offending_location(ip)
            send_sms_new_location(to_number=user.get('phone', None), user_name=user.get('first_name', None), city=city, region=region)
            
    except:
        print('Are you using dev environment?')

    new_ip = [ip]

    if len(new_ip) == 0:
        return 

    if not known_ips:
        db.child("users").child(user_email).update({'known_ip_addresses': new_ip})
    else:
        updated_ips = known_ips.append(new_ip[0])
        db.child("users").child(user_email).update({'known_ip_addresses': updated_ips})

def ip_check(offending_ip,known_ips):
    if offending_ip not in known_ips:
        for trusted_ip in known_ips:
            if location_check(offending_ip, trusted_ip):
                return True
    else:
        return True
    return False

def set_user(user_email, first_name, phone, ip):
    original_email = user_email
    user_email = user_email.replace('@', '')
    user_email = user_email.replace('.', '')
    
    phone = "+1" + phone
    new_ip = [ip]

    db.child("users").child(user_email).child("user_info").set({'first_name': first_name, 'phone': phone,'user_email': original_email})
    db.child("users").child(user_email).update({'known_ip_addresses': new_ip})

def update_breach_watch_list(user_email, breach_watch_list):
    # strip forbidden characters for DB interactions
    user_email = user_email.replace('@', '')
    user_email = user_email.replace('.', '')
    
    try:
        breach_watch_list_data = db.child("users").child(user_email).child("watch_list").child("breach_watch_list").get()
        domain_names = breach_watch_list_data.val().get('domain_names', None)
    except:
        domain_names = []

    for breach_name in breach_watch_list:
        if breach_name not in domain_names:
            domain_names.append(breach_name)
    
    db.child("users").child(user_email).child("watch_list").set({'breach_watch_list': domain_names})

def get_user(user_email):
    user_email = user_email.replace('@', '')
    user_email = user_email.replace('.', '')

    return db.child("users").child(user_email).child("user_info").get().val()

def get_all_user_email():
    user_ref = db.child("users").get()
    all_user = []
    for user in user_ref.each():
        all_user.append(user.key())
    
    emails = []
    for user in all_user:
        user_email = db.child("users").child(user).child("user_info").get().val().get('user_email', None)
        if user_email: 
            emails.append(user_email)
    return emails

def increment_monthly_safe(user_email):
    user_email = user_email.replace('@', '')
    user_email = user_email.replace('.', '')

    dt_now = datetime.datetime.now(tz=timezone.utc)
    date_year_bucket_safe = f'{month_set[dt_now.month - 1]}-{dt_now.year}-safe'

    try:
        data = db.child("users").child(user_email).child(date_year_bucket_safe).get().val().get('occurances')
        db.child("users").child(user_email).child(date_year_bucket_safe).update({"occurances": data + 1})

    except:
        db.child("users").child(user_email).child(date_year_bucket_safe).set({"occurances": 1})


def increment_monthly_unsafe(user_email):
    user_email = user_email.replace('@', '')
    user_email = user_email.replace('.', '')

    dt_now = datetime.datetime.now(tz=timezone.utc)
    date_year_bucket_unsafe = f'{month_set[dt_now.month - 1]}-{dt_now.year}-unsafe'

    try:
        data = db.child("users").child(user_email).child(date_year_bucket_unsafe).get().val().get('occurances')
        db.child("users").child(user_email).child(date_year_bucket_unsafe).update({"occurances": data + 1})

    except:
        db.child("users").child(user_email).child(date_year_bucket_unsafe).set({"occurances": 1})

def get_monthly_counts(user_email):
    user_email = user_email.replace('@', '')
    user_email = user_email.replace('.', '')

    dt_now = datetime.datetime.now(tz=timezone.utc)
    date_year_bucket_safe = f'{month_set[dt_now.month - 1]}-{dt_now.year}-safe'
    date_year_bucket_unsafe = f'{month_set[dt_now.month - 1]}-{dt_now.year}-unsafe'

    try:
        data_unsafe = db.child("users").child(user_email).child(date_year_bucket_unsafe).get().val().get('occurances')
    except:
        data_unsafe = 0

    try:
        data_safe = db.child("users").child(user_email).child(date_year_bucket_safe).get().val().get('occurances')
    except:
        data_safe = 0

    return [data_safe, data_unsafe]

def get_breach_watch_list(user_email):
    user_email = user_email.replace('@', '')
    user_email = user_email.replace('.', '')
    
    try:
        breach_watch_list_data = db.child("users").child(user_email).child("watch_list").child("breach_watch_list").get().val()
        return breach_watch_list_data
    except:
        response = {}
        response['MESSAGE'] = "Watchlist is empty"
        return response

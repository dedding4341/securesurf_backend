import schedule
import time
from .breaches import polling_get_all_breaches_for_user
from .datastore import get_all_user_email

def poll_breaches_for_all_users():
    print("Running polling background task")
    all_emails = get_all_user_email()
    
    for email in all_emails:
        polling_get_all_breaches_for_user(user_email=email)


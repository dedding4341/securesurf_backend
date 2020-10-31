from settings import HIBP_KEY
import pypwned as breach_service

breach_service = breach_service.pwned(HIBP_KEY)

def get_all_breaches_for_user(user_email):
    return breach_service.getAllBreachesForAccount(email=user_email)
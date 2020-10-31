from .settings import HIBP_KEY
import pypwned as breach_service

breach_service = breach_service.pwned(HIBP_KEY)

def get_all_breaches_for_user(user_email):
    return build_detailed_breach_information(breach_service.getAllBreachesForAccount(email=user_email))

def build_detailed_breach_information(breach_list):
    detailed_breach_info = []
    for breach in breach_list:
        detailed_breach = breach_service.getSingleBreachedSite(name=breach['Name'])
        detailed_breach_info.append(detailed_breach)
    return detailed_breach_info
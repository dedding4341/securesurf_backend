from .settings import HIBP_KEY
import pypwned as breach_service
from .datastore import load_compromised_sites, sanitize_return

breach_service = breach_service.pwned(HIBP_KEY)

def get_all_breaches_for_user(user_email):
    return build_detailed_breach_information(user_email, breach_service.getAllBreachesForAccount(email=user_email))

def build_detailed_breach_information(user_email, breach_list):

    # This needs to be run by acknowledged vs unacknowledged list in firebase

    load_compromised_sites(user_email=user_email, detailed_breach_info=breach_list)
    breaches_to_report_on = sanitize_return(user_email=user_email, detailed_breach_info=breach_list)

    detailed_breach_info = []
    for breach in breach_list:
        if breach['Name'] in breaches_to_report_on:
            detailed_breach = breach_service.getSingleBreachedSite(name=breach['Name'])
            detailed_breach_info.append(detailed_breach)

    # Sanitize + update list against acknowledged and unacknowledged in firebase
    
    return detailed_breach_info
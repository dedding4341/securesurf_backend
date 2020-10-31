from pysafebrowsing import SafeBrowsing
from .settings import SAFE_BROWSING_KEY
from .twilio_service import send_sms_message
from .datastore import record_url_visit, get_user

site_safety_service = SafeBrowsing(SAFE_BROWSING_KEY)

def safety_analysis(user_email, visited_url, remote_ip):
    # Record webpage habit here ?
    record_url_visit(user_email=user_email, url=visited_url, remote_ip=remote_ip)
    results = site_safety_service.lookup_url(visited_url)

    if results['malicious']:
        user_phone_number = get_user(user_email=user_email).get('phone', None)
        user_name = get_user(user_email=user_email).get('first_name', None)
        # Alert via text
        send_sms_message(to_number=user_phone_number, visited_url=visited_url, security_details=results, user_name=user_name)

    # Return results to extension
    return results

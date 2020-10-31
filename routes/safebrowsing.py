from pysafebrowsing import SafeBrowsing
from .settings import SAFE_BROWSING_KEY
from .twilio_service import send_sms_message

site_safety_service = SafeBrowsing(SAFE_BROWSING_KEY)

def safety_analysis(user_email, visited_url):
    # Record webpage habit here ?

    results = site_safety_service.lookup_url(visited_url)

    if results['malicious']:
        user_phone_number = None

        # Alert via text
        send_sms_message(to_number=user_phone_number, visited_url=visited_url, security_details=results)

    # Return results to extension
    return results

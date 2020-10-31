from twilio.rest import Client
from .settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_NUMBER

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_sms_message(to_number, visited_url, security_details, user_name):
    # Potentially include IP?
    seperator = ' '
    platforms_string = seperator.join(security_details['platforms'])
    threats_string = seperator.join(security_details['threats'])
    message_body=f'Hello {user_name}, this is a message from SecureSurf! \n \nThis message is to alert you that a browser session has been started with your credentials and has visited a potentially insecure URL: \n \nURL: {visited_url} \n \nVulnerable Platforms: {platforms_string} \n \nPotential Threats: {threats_string}'

    message = twilio_client.messages.create(
        to=to_number,
        from_=TWILIO_NUMBER,
        body=message_body
    )
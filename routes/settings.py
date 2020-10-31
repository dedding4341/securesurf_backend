from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

# Load super secrets here here, they'll never know they're actually in env
HIBP_KEY = os.getenv('HIBP_KEY')
SAFE_BROWSING_KEY = os.getenv('SAFE_BROWSING_KEY')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')

FIREBASE_CONFIG = {
    'apiKey': os.getenv('API_KEY'),
    'authDomain': os.getenv('AUTH_DOMAIN'),
    'databaseURL': os.getenv('DATABASE_URL'),
    'projectId': os.getenv('PROJECT_ID'),
    'storageBucket': os.getenv('STORAGE_BUCKET'),
    'messagingSenderId': os.getenv('MESSAGING_SENDER_ID'),
    'appId': os.getenv('APP_ID'),
    'measurementId': os.getenv('MEASUREMENT_ID')
}
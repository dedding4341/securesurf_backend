from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

# Load super secrets here here, they'll never know they're actually in env
HIBP_KEY = os.getenv('HIBP_KEY')
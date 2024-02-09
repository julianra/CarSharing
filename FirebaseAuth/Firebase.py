# firebase_auth/firebase.py
import firebase_admin
from firebase_admin import credentials

# Pad naar de serviceaccount-sleutel JSON-bestand
SERVICE_ACCOUNT_KEY_PATH = "FirebaseAuth/config.json"

def initialize_firebase():
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
    firebase_admin.initialize_app(cred)
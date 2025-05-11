# Token generálás

import hashlib
from django.utils.crypto import get_random_string

def generate_email_token():
    return hashlib.sha256(get_random_string(length=64).encode()).hexdigest()

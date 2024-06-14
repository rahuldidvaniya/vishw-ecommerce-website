# userauths/utils.py
import secrets
import string

def generate_activation_code(length=6):
    characters = string.ascii_letters + string.digits  # Using letters and digits
    activation_code = ''.join(secrets.choice(characters) for _ in range(length))
    return activation_code

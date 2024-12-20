import secrets
import string

def generate_random_string(length=16):
    characters = string.ascii_letters + string.digits  # Все буквы (A-Z, a-z) и цифры (0-9)
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string

random_string = generate_random_string(16)
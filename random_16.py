import string
import random

def random_string(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# random_string = generate_random_string(16)
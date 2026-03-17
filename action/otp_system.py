import random

def generate_otp():
    return random.randint(100000,999999)

def verify_otp(input_otp,real_otp):
    return input_otp == real_otp
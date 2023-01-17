import pyotp
import os

def otp():
    # function to fetch authentication code using the generated key from my.torontomu.ca
    return pyotp.TOTP(os.environ["TMU_OTP_KEY"]).now()
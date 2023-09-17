def generate_otp_code() -> str:
    """
    Generate a six-digits OTP code
    """

    import random

    return str(random.randint(100000, 999999))
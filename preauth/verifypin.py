

def pin_auth(user_pin, confirm_pin):
    if int(user_pin) == int(confirm_pin):
        return True
    else:
        return False

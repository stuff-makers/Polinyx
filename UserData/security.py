import bcrypt

# class for password hashing,validation and authentication confirmation


class Secure:
    def __init__(self):
        pass

# method to validate and hash user pw while creating account
    def safe_password(self, password):
        has_number = False
        has_uppercase = False

        for c in password:
            if c.isdigit():
                has_number = True
            if c.isupper():
                has_uppercase = True
        if(len(password) >= 7 and has_number == True and has_uppercase == True):
            byte_password = bytes(password, 'utf-8')
            hashed_password = bcrypt.hashpw(byte_password, bcrypt.gensalt())
            return hashed_password
        else:
            return False

# method for checking hashed pw and user entered pw
    def match_password(self, password, password_fetch):
        byte_password = bytes(password, 'utf-8')
        byte_password_fetch = bytes(password_fetch, 'utf-8')
        if bcrypt.checkpw(byte_password, byte_password_fetch):
            return True
        else:
            return False

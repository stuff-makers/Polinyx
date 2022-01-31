from UserData.ServerConnection import db, cursor
from UserData.security import Secure
import secrets as sec
import pickle as pk


# Master class for user related task
class User:
    def __init__(self):
        self.checker = Secure()

    def logout(self):
        t = open(r"assets/auth_token.dat", "wb")
        pk.dump([], t)
        t.close()

    # method to fetch data at home page

    def fetch_data(self, token):
        command = f"Select fullname,username,email from UserInfo where auth_token=\'{token}\'"
        cursor.execute(command)
        self.data = cursor.fetchall()
        return self.data

    # create_account method to be triggered on user clicking the signUp button
    def create_account(self, first_name, username, email, password):
        pw = str(self.checker.safe_password(password))
        command = f"INSERT INTO UserInfo(fullname,username,email,password) values('{first_name}', '{username}', '{email}', '{pw[2:len(pw)-1:1]}')"
        cursor.execute(command)
        db.commit()
        auth_state = self.login(email, password)
        return auth_state

    # login method to be triggered on user clicking the login button
    def login(self, email, chk_password):

        user_file = open(r"assets/auth_token.dat", "wb+")
        user_auth_details = tuple()
        # sql db stuff
        command = f"Select password from UserInfo where email=\'{email}\'"
        cursor.execute(command)
        password_fetch = cursor.fetchone()[0]
        cred_validity = self.checker.match_password(
            chk_password, password_fetch)

        # token and local storage stuff
        token = sec.token_urlsafe()
        user_auth_details += (token,)

        pk.dump(user_auth_details, user_file)

        user_file.close()

        command = f"UPDATE UserInfo SET auth_token=\'{token}\' WHERE email=\'{email}\'"
        cursor.execute(command)

        data = self.fetch_data(token)

        db.commit()
        return token, cred_validity, data

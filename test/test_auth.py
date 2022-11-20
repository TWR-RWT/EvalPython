import unittest
import jwt
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import auth

class TestAuth(unittest.TestCase):
    def test_login(self):
        self.assertEqual(auth.login("User1", "Password1"), 'success') # vrai utilisateur et mot de passe
        self.assertEqual(auth.login('User1', 'Password2'), 'wrong password') # vrai utilisateur et mauvais mot de passe
        self.assertEqual(auth.login('nimportequoi', 'Password1'), 'wrong username') # faux utilisateur et vrai mot de passe

    def test_jwt(self):
        self.assertEqual(auth.test_jwt("User1", "secret_keyyy"), "User1") # devrait toujours être vrai, test de la librairie jwt
        self.assertEqual(auth.test_jwt("blob", "secret_keyyy"), "blob")

if __name__ == '__main__':
    unittest.main()
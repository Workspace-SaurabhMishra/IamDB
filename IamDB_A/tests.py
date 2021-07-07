import json
import random
import unittest
import requests


'''
Testcases for delete not included bcz once deleted it will not exist so in other test run it will fail for same movie-name
'''

# Happy or Positive Flow
class Positive_Flow(unittest.TestCase):
    def test_sample(self):
        self.assertEqual(requests.get('http://127.0.0.1:8000/app/sample').content.decode(),
                         "API endpoint working fine!!")

    def test_signin(self):
        creds = {
            "username": "saurabh",
            "password": "12"
        }
        recv_data = json.loads(requests.post(url='http://127.0.0.1:8000/app/signin', data=creds).content.decode())
        x = recv_data["token"]
        self.assertEqual(len(x), 40)
        self.assertRegex(x, "^[0-9a-z]*$")

    def test_signup(self):
        uname = input("enter username for signup\n")
        creds = {
            "username": uname,
            "password": "12",
            "email": uname + "@email"
        }
        recv_data = json.loads(requests.post(url='http://127.0.0.1:8000/app/signup', data=creds).content.decode())
        x = recv_data["token"]
        y = recv_data["response"]

        self.assertEqual(len(x), 40)
        self.assertRegex(x, "^[0-9a-z]*$")

        self.assertEqual(y, "Succesfully registered User")

    def test_search(self):
        send_data = {
            "search-key": "clyde",
            "token": "00165ac34badfff3df03045ae15c3c51268f8e31"
        }
        recv_data = json.loads(requests.post(url='http://127.0.0.1:8000/app/search', data=send_data).content.decode())
        x = recv_data["data"]
        a = []
        for i in x:
            a.append(i["movie-name"])
        self.assertIn("Peter Pan", a)

    def test_update(self):
        send_data = {
            "parameter": "director",
            "key": "Luis el",
            "data": {
                "movie-name": "Luis El's Biography"
            },
            "token": "8c84460c59e563ef525b49852dffa0034f84ef36"
        }

        recv_data = json.loads(requests.patch(url='http://127.0.0.1:8000/app/update', data=send_data).content.decode())
        x = recv_data["response"]
        self.assertEqual(x, "Updation Successful")

    def test_signout(self):
        send_data = {
            "token": "8c84460c59e563ef525b49852dffa0034f84ef36"
        }
        recv_data = json.loads(requests.post(url='http://127.0.0.1:8000/app/signout').content.decode())
        x = recv_data["response"]
        self.assertIn(x, ["Logged Out", "Invalid User"])

#All the exceptions
class Negative_Flow(unittest.TestCase):
    # Wrong Username or Password
    def test_signin(self):
        creds = {
            "username": "saurab_wrong",
            "password": "12"
        }
        recv_data = json.loads(requests.post(url='http://127.0.0.1:8000/app/signin', data=creds).content.decode())

        self.assertEqual(recv_data, {
            "non_field_errors": [
                "Unable to log in with provided credentials."
            ]
        })

    def test_signup(self):
        # Invalid Email Format
        cred1 = {
            "username": "saurabh" + str(random.choice(range(0, 879))),
            "email": "Wrong_email.com",
            "password": "12"
        }

        # Missing Username,password or email
        cred2 = {
            "username": "saurabh" + str(random.choice(range(0, 879))),
            "email": "Wrong_email.com",
            # "password": "12"
        }

        recv_data1 = json.loads(requests.post(url='http://127.0.0.1:8000/app/signup', data=cred1).content.decode())
        recv_data2 = json.loads(requests.post(url='http://127.0.0.1:8000/app/signup', data=cred2).content.decode())

        self.assertEqual(recv_data1, {
            "response": "Invalid Email"
        })

        self.assertEqual(recv_data2, {
            "response": "Something is missing from Username, Password, Email, Please provide that also!!"
        })

    def test_search(self):
        # Without Token Access
        send_data1 = {
            "search-key": "clyde"
        }

        # Wrong Search Key
        send_data2 = {
            "searchkey": "clyde",
            "token": "00165ac34badfff3df03045ae15c3c51268f8e31"
        }
        recv_data1 = json.loads(
            requests.post(url='http://127.0.0.1:8000/app/search', data=send_data1).content.decode())

        recv_data2 = json.loads(
            requests.post(url='http://127.0.0.1:8000/app/search', data=send_data2).content.decode())

        self.assertEqual(recv_data1, {
            "response": "You're not authenticated to access this feature"
        })

        self.assertEqual(recv_data2, {
            "response": "Search Key not provided"
        })

    def test_update(self):
        # wrong parameter type
        send_data1 = {
            "parameter": "dirctor",
            "key": "Luis el",
            "data": {
                "movie-name": "Luis El's Biography"
            },
            "token": "8c84460c59e563ef525b49852dffa0034f84ef36"
        }

        # without token
        send_data2 = {
            "parameter": "dirctor",
            "key": "Luis el",
            "data": {
                "movie-name": "Luis El's Biography"
            }
        }

        recv_data1 = json.loads(
            requests.patch(url='http://127.0.0.1:8000/app/update', data=send_data1).content.decode())
        recv_data2 = json.loads(
            requests.patch(url='http://127.0.0.1:8000/app/update', data=send_data2).content.decode())

        self.assertEqual(recv_data1, {
            "response": "Invalid updation parameter"
        })

        self.assertEqual(recv_data2, {
            "response": "You're not authenticated to access this feature"
        })


if __name__ == "__main__":
    unittest.main()

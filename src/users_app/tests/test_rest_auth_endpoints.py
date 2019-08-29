#test rest-auth endpoints

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from users_app.models import Sub

from django.contrib.auth.models import User
from django.test.utils import override_settings

#user every time a user has to be created for testing
test_user_data = {
    'username': "testuser100",
    'email': "testemail@test.com",
    'password': "testingpassword"
}

@override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
class TestRestAuthEndpoints(APITestCase):
    '''test login and logout endpoints from rest-auth'''

    def setUp(self):
        self.user = User.objects.create_user(**test_user_data)
        self.login_url = "/rest-auth/login/"
        self.logout_url = "/rest-auth/logout/"
        self.register_url = "/rest-auth/registration/"
        self.recover_password_url = '/password-reset/'
        self.client = APIClient()
        self.data = {
            'username': test_user_data['username'],
            'password': test_user_data['password']
        }
    
    def test_login_endpoint(self):

        response = self.client.post(path=self.login_url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_logout_endpoint(self):

        self.client.login(username="testinguser10", password="testingpassword10")

        response = self.client.post(path=self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_register_endpoint(self):

        register_data = {
            'username': 'newregistereduser10',
            'password1': 'newtestingpassword10',
            'password2': 'newtestingpassword10',
            'email': 'testigemail@test.com'
        }

        response = self.client.post(path=self.register_url, data=register_data, format="json")
        self.assertTrue(isinstance(Sub.objects.first(), Sub))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_recover_password(self):
        data = {'email': 'fabyjesusrivas10@gmail.com'}
        user = User.objects.create_user(
            username='thisistheusername',
            password='thisisasd123',
            email='fabyjesusrivas10@gmail.com'
        )
        
        response = self.client.post( path=self.recover_password_url, data=data)
        
        token = str(input("token: "))
        uid = str(input("uid here: "))
        path2 = '/password-reset/confirm/{0}/{1}/'.format(uid, token)
        data2 = {
            'new_password1':'thisisnewpassword34',
            'new_password2':'thisisnewpassword34',
            'uid': uid,
            'token': token
            }
        response2 = self.client.post(path=path2, data=data2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

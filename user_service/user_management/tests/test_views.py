from django.test import TestCase
from user_management.views import *


class RegisterView(TestCase):

    def test_register_customer_valid(self):
        """Customer are register correctly"""
        data = {
            "username": "User1",
            "password": "12345678",
            "fullname": "Test",
            "address": "1234/12",
            "province": "Bangkok",
            "post_code": "10300",
            "tel": "123456789",
        }
        response = self.client.post(
            "/api/register/", content_type="application/json", data=data
        )
        self.assertEqual(response.status_code, 201)

    def test_register_customer_in_valid(self):
        """Customer are register not correctly"""
        response = self.client.post(
            "/api/register/", content_type="application/json", data={}
        )
        self.assertEqual(response.status_code, 400)

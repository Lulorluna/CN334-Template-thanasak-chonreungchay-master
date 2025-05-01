from django.test import TestCase
from user_management.models import Customer
from django.contrib.auth.models import User


class CustomerTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="Test_user", password="12345678")

    def test_create_customer_true(self):
        """Customer can create correctly"""
        register_data = {
            "fullname": "Test",
            "address": "1234/12",
            "province": "Bangkok",
            "post_code": "10300",
            "tel": "123456789",
        }
        user = User.objects.get(username="Test_user")
        customer = Customer(user=user, **register_data)
        customer.save()
        customer_dict = customer.__dict__
        del customer_dict["_state"]
        del customer_dict["id"]
        del customer_dict["user_id"]
        self.assertEqual(customer_dict, register_data)

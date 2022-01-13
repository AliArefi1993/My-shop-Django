from django.urls.base import reverse
from model_mommy import mommy
from rest_framework.test import APITestCase
from users.models import CustomUser
from order.models import Order

User = CustomUser


class TestOrderListPend(APITestCase):
    "Test for getting detail and updating a customer"

    def setUp(self):
        self.user = mommy.make(User)
        self.Customer = mommy.make(Order, status='PEND')
        self.Customer = mommy.make(Order, status='PAID')
        self.Customer = mommy.make(Order, status='CANC')

    def test_put_customer_profile(self):
        url = reverse('order_api:order_pend_list')
        self.client.force_authenticate(self.user)

        resp = self.client.get(url)
        #   check the response status
        self.assertEqual(resp.status_code, 200)

        #   check the response lenght
        self.assertEqual(len(resp.data), 1)

from django.urls.base import reverse
from model_mommy import mommy
from rest_framework.test import APITestCase
from order.models import OrderItem
from shop.models import Product
from users.models import CustomUser
from order.models import Order

User = CustomUser


class TestOrderListPend(APITestCase):
    "Test for getting list of pended orders"

    def setUp(self):
        self.user = mommy.make(User)
        self.order1 = mommy.make(Order, status='PEND')
        self.order2 = mommy.make(Order, status='PAID')
        self.order3 = mommy.make(Order, status='CANC')

    def test_get_pend_order_list(self):
        url = reverse('order_api:order_pend_list')
        self.client.force_authenticate(self.user)

        resp = self.client.get(url)
        #   check the response status
        self.assertEqual(resp.status_code, 200)

        #   check the response lenght
        self.assertEqual(len(resp.data), 1)


class TestOrderListPrevious(APITestCase):
    "Test for getting List of previous orders"

    def setUp(self):
        self.user = mommy.make(User)
        self.order1 = mommy.make(Order, status='PEND')
        self.order2 = mommy.make(Order, status='PAID')
        self.order3 = mommy.make(Order, status='CANC')

    def test_get_previous_order_list(self):
        url = reverse('order_api:order_previous_list')
        self.client.force_authenticate(self.user)

        resp = self.client.get(url)
        #   check the response status
        self.assertEqual(resp.status_code, 200)

        #   check the response lenght
        self.assertEqual(len(resp.data), 2)


class TestOrderPay(APITestCase):
    "Test for paying an order"

    def setUp(self):
        self.user = mommy.make(User)
        self.order1 = mommy.make(Order, status='PEND')
        self.order2 = mommy.make(Order, status='PAID')
        self.order3 = mommy.make(Order, status='CANC')

    def test_get_previous_order_list(self):
        url = reverse('order_api:order_pay', args=[self.order1.pk])

        self.client.force_authenticate(self.user)

        resp = self.client.patch(url)
        #   check the response status
        self.assertEqual(resp.status_code, 200)

        #   check the status of order after pay
        self.assertEqual(Order.objects.get(pk=self.order1.pk).status, 'PAID')


class TestOrderAddItem(APITestCase):
    "Test for adding item to an order"

    def setUp(self):
        self.user = mommy.make(User)
        self.order1 = mommy.make(Order, status='PEND')
        self.order2 = mommy.make(Order, status='PAID')
        self.order3 = mommy.make(Order, status='CANC')
        self.product1 = mommy.make(Product)

    def test_get_previous_order_list(self):
        url = reverse('order_api:order_add_item', args=[self.order1.pk])

        self.client.force_authenticate(self.user)
        data = {"item_ids": [1]}
        resp = self.client.patch(url, data=data)
        #   check the response status
        self.assertEqual(resp.status_code, 200)

        #   check the status of order after pay
        self.assertIsNotNone(OrderItem.objects.get(order__pk=self.order1.pk))

        # test Order_item quantity after 2 addition
        resp = self.client.patch(url, data=data)
        self.assertEqual(OrderItem.objects.get(
            order__pk=self.order1.pk).quantity, 2)

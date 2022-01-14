from django.urls.base import reverse
from model_mommy import mommy
from rest_framework.test import APITestCase
from shop.models import Supplier
from order.models import OrderItem
from shop.models import Product
from users.models import CustomUser
from order.models import Order
from customer.models import Customer


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
        self.supplier = mommy.make(Supplier, status='CONF')
        self.product1 = mommy.make(Product, supplier=self.supplier, quantity=5)

    def test_get_add_order_to_order(self):
        url = reverse('order_api:order_add_item', args=[self.order1.pk])

        self.client.force_authenticate(self.user)
        data = {"item_ids": [self.product1.pk]}
        resp = self.client.patch(url, data=data)
        #   check the response status
        self.assertEqual(resp.status_code, 200)

        #   check the status of order after pay
        self.assertIsNotNone(OrderItem.objects.get(order__pk=self.order1.pk))

        # test Order_item quantity after 2 addition
        resp = self.client.patch(url, data=data)
        self.assertEqual(OrderItem.objects.get(
            order__pk=self.order1.pk).quantity, 2)
        self.assertEqual(Product.objects.get(
            pk=self.product1.pk).quantity, 3)


class TestOrderSubtractItem(APITestCase):
    "Test for subtracting an item to an order"

    def setUp(self):
        self.user = mommy.make(User)
        self.order1 = mommy.make(Order, status='PEND')
        self.order2 = mommy.make(Order, status='PAID')
        self.order3 = mommy.make(Order, status='CANC')
        self.supplier = mommy.make(Supplier, status='CONF')
        self.product1 = mommy.make(Product, supplier=self.supplier, quantity=5)

    def test_substract_item_from_order(self):
        url = reverse('order_api:order_add_item', args=[self.order1.pk])
        self.client.force_authenticate(self.user)
        data = {"item_ids": [self.product1.pk]}
        # add two number of a product
        resp = self.client.patch(url, data=data)
        resp = self.client.patch(url, data=data)
        self.assertEqual(OrderItem.objects.get(
            order__pk=self.order1.pk).quantity, 2)

        # reduce a product from order
        url = reverse('order_api:order_subtract_item', args=[self.order1.pk])
        resp = self.client.patch(url, data=data)

        #   check the response status
        self.assertEqual(resp.status_code, 200)

        # test Order_item quantity one substraction
        self.assertEqual(OrderItem.objects.get(
            order__pk=self.order1.pk).quantity, 1)
        self.assertEqual(Product.objects.get(
            pk=self.product1.pk).quantity, 4)

        # test order_item price
        total_order_item_price = OrderItem.objects.get(
            order__pk=self.order1.pk).price
        self.assertEqual(total_order_item_price, self.product1.unit_price)

        # test order total price
        total_price = Order.objects.get(pk=self.order1.pk).total_price
        self.assertEqual(total_price, self.product1.unit_price)

        # test cancelig order after eleminating all items
        resp = self.client.patch(url, data=data)
        status = Order.objects.get(pk=self.order1.pk).status
        self.assertEqual(status, 'CANC')


class TestOrderCreate(APITestCase):
    "Test for creating an order "

    def setUp(self):
        self.user = mommy.make(User)
        self.customer = mommy.make(Customer, custom_user=self.user)
        self.supplier = mommy.make(Supplier, status='CONF')
        self.product1 = mommy.make(Product, supplier=self.supplier, quantity=5)
        self.supplier2 = mommy.make(Supplier, status='PEND')
        self.product2 = mommy.make(Product, supplier=self.supplier2)

    def test_create_new_order(self):
        url = reverse('order_api:order_create')
        self.client.force_authenticate(self.user)
        data = {"item_ids": [self.product1.pk]}
        resp = self.client.post(url, data=data)
        order_id = resp.data['id']

        #   check the response status
        self.assertEqual(resp.status_code, 201)

        # test Order_item quantity after creation
        self.assertIsNotNone(OrderItem.objects.get(
            order__pk=order_id).quantity, 1)

        # test order_item price
        self.assertEqual(OrderItem.objects.get(
            order__pk=order_id).price, self.product1.unit_price)

        # check don't allow to buy from pend supplier
        data = {"item_ids": [self.product2.pk]}
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 404)

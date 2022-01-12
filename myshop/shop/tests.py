from rest_framework import status
from shop.models import Type, Tag
from shop.models import Supplier, Product
from users.models import CustomUser
from rest_framework.test import APITestCase
from model_mommy import mommy
from django.urls import reverse

User = CustomUser


class TestSupplierList(APITestCase):

    def setUp(self):
        self.user = mommy.make(User)
        self.type1 = mommy.make(Type, name='Digital')
        self.type2 = mommy.make(Type, name='Stationery')
        mommy.make(Supplier, custom_user=self.user,
                   type=self.type1, status='CONF')
        mommy.make(Supplier, custom_user=self.user,
                   type=self.type2, status='CONF')
        mommy.make(Supplier, custom_user=self.user,
                   type=self.type2, status='PEND')

    def test_supplier_list(self):
        self.client.force_authenticate(self.user)
        url = reverse('shop_api:supplier')

        resp = self.client.get(url)

        #   check the response status
        self.assertEqual(resp.status_code, 200)

        #   check the response lenght
        self.assertEqual(len(resp.data), 2)

    def test_supplier_list_filter_type(self):
        self.client.force_authenticate(self.user)
        url = reverse('shop_api:supplier')
        resp = self.client.get(url, {'type__name': 'Digital'})

        #   check the response status
        self.assertEqual(resp.status_code, 200)

        #   check the response lenght
        self.assertEqual(len(resp.data), 1)


class TestSupplierTypeList(APITestCase):

    def setUp(self):
        self.user = mommy.make(User)
        self.type1 = mommy.make(Type, name='Digital')
        self.type2 = mommy.make(Type, name='Stationery')

    def test_supplier_list(self):
        self.client.force_authenticate(self.user)
        url = reverse('shop_api:supplier_types')

        resp = self.client.get(url)

        #   check the response status
        self.assertEqual(resp.status_code, 200)

        #   check the response lenght
        self.assertEqual(len(resp.data), 2)


class TestSupplierProductList(APITestCase):
    def setUp(self):
        self.user = mommy.make(User)
        self.tag1 = mommy.make(Tag, name='new')
        self.tag2 = mommy.make(Tag, name='fantasy')
        self.tag3 = mommy.make(Tag, name='amazing')
        self.unit_price1 = 1000
        self.unit_price2 = 2000
        self.unit_price3 = 3000
        self.supplier_name1 = 'DJ Phone'
        self.supplier_name2 = 'Book Shop'
        self.supplier_slug1 = 'dj-phone'
        self.supplier_slug2 = 'book-shop'
        self.supplier1 = mommy.make(Supplier, custom_user=self.user,
                                    supplier_name=self.supplier_name1, status='CONF')
        self.supplier2 = mommy.make(Supplier, custom_user=self.user,
                                    supplier_name=self.supplier_name2, status='CONF')
        self.product1 = mommy.make(Product, supplier=self.supplier1,
                                   tag=self.tag1, is_available=True, quantity=5, unit_price=self.unit_price1)
        self.product2 = mommy.make(Product, supplier=self.supplier2,
                                   tag=self.tag2, is_available=False, quantity=3, unit_price=self.unit_price2)
        self.product3 = mommy.make(Product, supplier=self.supplier2,
                                   tag=self.tag2, is_available=True, quantity=0)
        self.product4 = mommy.make(Product, supplier=self.supplier2,
                                   tag=self.tag3, is_available=True, quantity=2, unit_price=self.unit_price3)

    def test_supplier_product_list(self):
        self.client.force_authenticate(self.user)
        # check the first supplier products
        url = reverse('shop_api:supplier_products', args=[self.supplier_slug1])
        resp = self.client.get(url)

        #   check the response status
        self.assertEqual(resp.status_code, 200)

        #   check the response lenght
        self.assertEqual(len(resp.data), 1)
        #   check to not show products with zero quantity
        url = reverse('shop_api:supplier_products', args=[self.supplier_slug2])
        resp = self.client.get(url)
        self.assertEqual(len(resp.data), 2)

    def test_supplier_list_filter_tag(self):
        self.client.force_authenticate(self.user)
        url = reverse('shop_api:supplier_products', args=[self.supplier_slug2])
        resp = self.client.get(url, {'tag__name': self.tag3})

        #   check the response status
        self.assertEqual(resp.status_code, 200)

        #   check the response lenght
        self.assertEqual(len(resp.data), 1)

    def test_supplier_list_filter_price(self):
        self.client.force_authenticate(self.user)
        url = reverse('shop_api:supplier_products', args=[self.supplier_slug2])
        resp = self.client.get(
            url, {'unit_price__gt': self.unit_price1, 'unit_price__lt': self.unit_price3})

        #   check the response status
        self.assertEqual(resp.status_code, 200)

        # #   check the response lenght
        self.assertEqual(len(resp.data), 1)

    def test_supplier_list_filter_is_available(self):
        self.client.force_authenticate(self.user)
        url = reverse('shop_api:supplier_products', args=[self.supplier_slug2])
        resp = self.client.get(
            url, {'is_available': True})

        #   check the response status
        self.assertEqual(resp.status_code, 200)

        # #   check the response lenght
        self.assertEqual(len(resp.data), 1)

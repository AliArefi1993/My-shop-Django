from rest_framework import status
from shop.models import Type
from shop.models import Supplier
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
        # url = reverse('shop_api:supplier', type__name='dd')
        # print(url)
        # print(url)
        # print(url)
        # resp = self.client.get(url)

        #   check the response status
        # self.assertEqual(resp.status_code, 200)

        #   check the response lenght
        # self.assertEqual(len(resp.data), 2)


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

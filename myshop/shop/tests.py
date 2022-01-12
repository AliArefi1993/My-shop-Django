from shop.models import Supplier
from users.models import CustomUser
from rest_framework.test import APITestCase
from model_mommy import mommy
from django.urls import reverse


User = CustomUser


class TestSupplierList(APITestCase):

    def setUp(self):
        self.user = mommy.make(User)
        mommy.make(Supplier, custom_user=self.user, _quantity=2)
        # mommy.make(Post, _quantity=5)
        # mommy.make(Post, title='test here', _quantity=1)

    def test_create_user(self):
        self.client.force_authenticate(self.user)
        url = reverse('shop_api:supplier')

        resp = self.client.get(url)

        #   check the response status
        self.assertEqual(resp.status_code, 200)

        #   check the response lenght
        self.assertEqual(len(resp.data), 2)

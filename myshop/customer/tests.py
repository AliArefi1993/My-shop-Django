from django.core.files.uploadedfile import SimpleUploadedFile
from customer.models import Customer
from users.models import CustomUser
from rest_framework.test import APITestCase
from model_mommy import mommy
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


User = CustomUser


class TestCreateUserView(APITestCase):

    def setUp(self):
        pass
        # user = mommy.make(User)
        # mommy.make(Post, owner=user, _quantity=10)
        # mommy.make(Post, _quantity=5)
        # mommy.make(Post, title='test here', _quantity=1)

    def test_create_user(self):
        url = reverse('customer_api:register')
        password = "ali1234789"
        phone = "09301605685"
        data = {
            "phone": phone,
            "password": password,
            "password2": password,
            "last_name": "aref",
            "first_name": "ahmad",
            "national_code": "1234234",
            "email": "asdjsad@sad.com"
        }
        resp = self.client.post(url, data=data)

        #   check the response status
        self.assertEqual(resp.status_code, 201)

        #   check the response data
        resp_data = {"id": 1,
                     "phone": phone,
                     "last_name": "aref",
                     "first_name": "ahmad",
                     "email": "asdjsad@sad.com"}
        self.assertEqual(resp.data, resp_data)

        #   check the hashed saved password
        test_user = User.objects.get(id=1)
        self.assertTrue(check_password(password, test_user.password))

        #   check the database saved data except password
        database_data = {"phone": test_user.phone,
                         "last_name": test_user.last_name,
                         "first_name": test_user.first_name,
                         "email": test_user.email,
                         "national_code": test_user.national_code
                         }
        data.pop('password')
        data.pop('password2')
        self.assertEqual(database_data, data)

    # test the appropriate error message
    def test_create_user(self):
        url = reverse('customer_api:register')
        password = "ali1234789"
        wrong_password = "ali"
        phone = "09301605685"
        data = {
            "phone": phone,
            "password": password,
            "password2": wrong_password,
            "last_name": "aref",
            "first_name": "ahmad",
            "national_code": "1234234",
            "email": "asdjsad@sad.com"
        }
        resp = self.client.post(url, data=data)

        #   check the response status
        self.assertEqual(resp.status_code, 400)
        #   check the response message
        expected_message = {"password": [
            "Password fields didn't match."
        ]}
        self.assertEqual(resp.data, expected_message)


#
    # def test_post_detail(self):
    #     url = reverse('post_detail', args=[16])
    #     resp = self.client.get(url)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertEqual(resp.data['title'], 'test here')


# class TestTokenObtainPairView(APITestCase):

#     def setUp(self):
#         self.user = mommy.make(User, phone='09301605684', password='1')

#     def test_login(self):
#         data = {
#             "phone": self.user.phone,
#             "password": self.user.password
#         }
#         print(self.user)
#         self.client.force_authenticate(self.user)
#         url = reverse('customer_api:token_obtain_pair')
#         print(url)
#         print(data)
#         resp = self.client.post(url, data)
#         print(resp)
#         self.assertEqual(resp.status_code, 200)


class TestCreateCustomerProfileView(APITestCase):
    "Test for creating new customer(create a profile)"

    def setUp(self):
        self.user = mommy.make(User)

    def test_create_customer(self):
        url = reverse('customer_api:create_profile')
        self.client.force_authenticate(self.user)

        image = SimpleUploadedFile(name='test_image.jpeg', content=open(
            '/Users/...a/Documents/programming/maktab/project/maktab_final_project/myshop/customer/test_image.jpeg', 'rb').read(), content_type='image/jpeg')
        data = {
            "customer_username": "ALI",
            "country": "Iran",
            "state": "Kerman",
            "city": "Jiroft",
            "address": "Street 2",
            "post_code": "1234223434",
            "image": image
        }
        resp = self.client.post(url, data=data)

        #   check the response status
        self.assertEqual(resp.status_code, 201)

        #   check the response data
        desired_resp_data = {
            "customer_username": "ALI",
            "country": "Iran",
            "state": "Kerman",
            "city": "Jiroft",
            "address": "Street 2",
            "post_code": "1234223434",
            "custom_user": 1
        }
        self.assertEqual(resp.data, desired_resp_data)

        #   check the database saved data
        test_customer = Customer.objects.get(pk=1)

        database_data = {"customer_username": test_customer.customer_username,
                         "country": test_customer.country,
                         "state": test_customer.state,
                         "city": test_customer.city,
                         "address": test_customer.address,
                         "post_code": test_customer.post_code,
                         "city": test_customer.city,

                         }
        data.pop('image')
        self.assertEqual(database_data, data)

        # Test custom_user id
        print(resp.data)
        self.assertEqual(1, resp.data['custom_user'])

    # test the appropriate error message

    def test_create_customer(self):
        url = reverse('customer_api:create_profile')
        image = SimpleUploadedFile(name='test_image.jpeg', content=open(
            '/Users/...a/Documents/programming/maktab/project/maktab_final_project/myshop/customer/test_image.jpeg', 'rb').read(), content_type='image/jpeg')
        data = {
            "customer_username": "ALI",
            "country": "Iran",
            "state": "Kerman",
            "city": "Jiroft",
            "address": "Street 2",
            "post_code": "1234223434",
            # "image": image  #data without image
        }
        self.client.force_authenticate(self.user)

        resp = self.client.post(url, data=data)

        #   check the response status
        self.assertEqual(resp.status_code, 400)
        #   check the response message
        expected_message = {"image": ["This field is required."]}
        # self.assertEqual(resp.data, expected_message)


class TestCustomerProfileUpdateDetail(APITestCase):
    "Test for getting detail and updating a customer"

    def setUp(self):
        self.user = mommy.make(User)
        self.Customer = mommy.make(Customer, custom_user=self.user,)

    def test_put_customer_profile(self):
        url = reverse('customer_api:profile', args=[self.Customer.pk])
        self.client.force_authenticate(self.user)
        image = SimpleUploadedFile(name='test_image.jpeg', content=open(
            '/Users/...a/Documents/programming/maktab/project/maktab_final_project/myshop/customer/test_image.jpeg', 'rb').read(), content_type='image/jpeg')
        new_data = {
            "customer_username": "ALI",
            "country": "Iran",
            "state": "Kerman",
            "city": "Jiroft",
            "address": "Street 2",
            "post_code": "1234223434",
            "image": image
        }
        resp = self.client.put(url, new_data)
        #   check the response status
        self.assertEqual(resp.status_code, 200)

        #   check the response data without image
        desired_resp_data = {
            "customer_username": "ALI",
            "country": "Iran",
            "state": "Kerman",
            "city": "Jiroft",
            "address": "Street 2",
            "post_code": "1234223434",
            "custom_user": self.Customer.pk,
            # "image": image

        }
        resp_data_without_image = resp.data
        resp_image = resp_data_without_image.pop('image')
        self.assertEqual(resp_data_without_image, desired_resp_data)

        # check image in response image
        self.assertIsNotNone(resp_image)

        #   check the database saved data
        test_customer = Customer.objects.get(pk=self.Customer.pk)

        database_data = {"customer_username": test_customer.customer_username,
                         "country": test_customer.country,
                         "state": test_customer.state,
                         "city": test_customer.city,
                         "address": test_customer.address,
                         "post_code": test_customer.post_code,
                         "custom_user": test_customer.custom_user.pk,
                         }
        self.assertEqual(database_data, resp_data_without_image)

    # test the appropriate error message
        url = reverse('customer_api:profile', args=[self.Customer.pk])
        image = SimpleUploadedFile(name='test_image.jpeg', content=open(
            '/Users/...a/Documents/programming/maktab/project/maktab_final_project/myshop/customer/test_image.jpeg', 'rb').read(), content_type='image/jpeg')
        data = {
            "customer_username": "ALI",
            # "country": "Iran",  #data without country
            "state": "Kerman",
            "city": "Jiroft",
            "address": "Street 2",
            "post_code": "1234223434",
            "image": image
        }
        self.client.force_authenticate(self.user)
        resp = self.client.put(url, data=data)

        #   check the response status
        self.assertEqual(resp.status_code, 400)

        #   check the response message
        expected_message = {"country": ["This field is required."]}
        self.assertEqual(resp.data, expected_message)

    def test_patch_customer_profile(self):
        url = reverse('customer_api:profile', args=[self.Customer.pk])
        self.client.force_authenticate(self.user)
        image = SimpleUploadedFile(name='test_image.jpeg', content=open(
            '/Users/...a/Documents/programming/maktab/project/maktab_final_project/myshop/customer/test_image.jpeg', 'rb').read(), content_type='image/jpeg')
        new_data = {
            # "customer_username": "ALI",
            "country": "Iran",
            # "state": "Kerman",
            # "city": "Jiroft",
            # "address": "Street 2",
            # "post_code": "1234223434",
            "image": image
        }
        resp = self.client.patch(url, new_data)
        #   check the response status
        self.assertEqual(resp.status_code, 200)

        #   check the  updated field in response data
        desired_resp_data = {
            "customer_username": "ALI",
            "country": "Iran",
            "state": "Kerman",
            "city": "Jiroft",
            "address": "Street 2",
            "post_code": "1234223434",
            "custom_user": self.Customer.pk,
            # "image": image

        }
        self.assertEqual(resp.data['country'], desired_resp_data['country'])

        # check image in response image
        self.assertIsNotNone(resp.data['country'])
        #   check the database saved data
        test_customer = Customer.objects.get(pk=self.Customer.pk)

        database_data = {
            "country": test_customer.country,
        }
        self.assertEqual(database_data['country'], resp.data['country'])

    def test_get_customer_profile(self):
        url = reverse('customer_api:profile', args=[self.Customer.pk])
        self.client.force_authenticate(self.user)
        image = SimpleUploadedFile(name='test_image.jpeg', content=open(
            '/Users/...a/Documents/programming/maktab/project/maktab_final_project/myshop/customer/test_image.jpeg', 'rb').read(), content_type='image/jpeg')
        new_data = {
            # "customer_username": "ALI",
            "country": "Iran",
            # "state": "Kerman",
            # "city": "Jiroft",
            # "address": "Street 2",
            # "post_code": "1234223434",
            "image": image
        }
        resp = self.client.get(url, new_data)

        #   check the response status
        self.assertEqual(resp.status_code, 200)

        # check database data
        test_customer = Customer.objects.get(pk=self.Customer.pk)
        database_data = {"customer_username": test_customer.customer_username,
                         "country": test_customer.country,
                         "state": test_customer.state,
                         "city": test_customer.city,
                         "address": test_customer.address,
                         "post_code": test_customer.post_code,
                         "custom_user": self.Customer.pk,
                         "city": test_customer.city,

                         }
        resp_image = resp.data.pop('image')
        self.assertEqual(database_data, resp.data)

        # test image field should be none
        self.assertIsNone(resp_image)

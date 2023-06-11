from django.test import TestCase

from .models import *

class ModelsTest(TestCase):
    def test_create_user_profile_user_exists(self):
        seller_user = User.objects.create_user('john')
        username = 'john'
        register_as = 'Seller'
        profile_picture = ''
        self.assertFalse(create_user_profile(seller_user,username,register_as,profile_picture))

    def test_create_user_profile(self):
        seller_user = User.objects.create_user('john')
        seller_user.delete()
        username = 'john'
        register_as = 'Seller'
        profile_picture = ''
        self.assertTrue(create_user_profile(seller_user,username,register_as,profile_picture))
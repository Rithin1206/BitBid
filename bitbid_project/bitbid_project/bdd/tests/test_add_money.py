import os
import sys

# We need to set the DJANGO_SETTINGS_MODULE to appropriate path
current_path = os.path.abspath('.')
parent_path = os.path.dirname(current_path)
abs_path = os.path.join(parent_path, 'bitbid_project/')
sys.path.append(abs_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bitbid_project.settings')

import django
django.setup()

from django.db import models
from django.contrib.auth.models import User
import pytest
from pytest_bdd import scenario, given, when, then
from bitbid_project.models import *

from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client

# Since tests are run only on dev environment, we can use localhost
homepage = 'http://127.0.0.1:8000'

@pytest.fixture(scope='function')
def context():
    return {}

# Scenario 1
@pytest.mark.django_db
@scenario(feature_name='../features/add_money.feature', scenario_name='User adds monmey to wallet')
def test_seller_creates_new_item():
    print("Finished test_user_adds_monmey_to_wallet")

@given("I am a registered user")
def i_am_a_registered_user(context):
    # flush DB
    os.system("python manage.py flush --no-input")
    client = Client()
    user = User.objects.get_or_create(username='testuser')[0]
    # _wallet=Wallet.objects.create(balance=0.00)
    # Profile.objects.create(user=user, wallet=_wallet, profile_picture=None, user_type=)
    client.force_login(user)
    response= client.post(homepage+"/User", data={'username': 'Testuser', 'register_as':'Seller', 'profile_picture':''}, follow=True)
    assert response.status_code == 200
    context['client'] = client

@when("I click on Add Money")
def i_click_on_add_money(context):
    client = context['client']
    context['add_money'] = 100
    response= client.post(homepage+'/addMoney', data={'added_money': context['add_money'] },follow=True)
    context['response'] = response

@then('I should see the wallet updated')
def i_should_see_the_wallet_updated(context):
    response = context['response']
    assert response.status_code == 200
    index = context['response'].content.decode("utf-8").find(str(context['add_money']))
    assert index!=-1


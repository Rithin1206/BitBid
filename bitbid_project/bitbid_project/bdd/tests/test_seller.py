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
from datetime import datetime
from datetime import timedelta

# Since tests are run only on dev environment, we can use localhost
homepage = 'http://127.0.0.1:8000'

@pytest.fixture(scope='function')
def context():
    return {}

# Scenario 1
@pytest.mark.django_db
@scenario(feature_name='../features/seller.feature', scenario_name='Seller creates new item')
def test_seller_creates_new_item():
    print("Finished test_seller_creates_new_item")

@given("I am a registered seller")
def i_am_a_registered_seller(context):
    # flush DB
    os.system("python manage.py flush --no-input")
    client = Client()
    user = User.objects.get_or_create(username='testuser')[0]
    client.force_login(user)
    client.post(homepage+"/User", data={'username': 'Testuser', 'register_as':'Seller', 'profile_picture':''}, follow=True)
    context['client'] = client

@when("I click on create new item")
def i_click_on_create_new_item(context):
    client = context['client']
    start_date =  datetime.utcnow()
    end_date = start_date+ timedelta(days=2)
    context['start_date']= start_date
    response = client.post(homepage+'/newItem', data={'name': 'test_item',
                                                     'description': 'test Item description', 
                                                     'start_date': start_date, 
                                                     'end_date': end_date, 
                                                     'base_amount': 100.23,
                                                     'item_value': 60, 
                                                     'increment_amount': 10.22},  follow=True)
    context['response'] = response

@then('I should successfuly be allowed to enter item details and submit them')
def i_should_be_successfully_taken_to_buyer_page(context):
    response = context['response']
    assert response.status_code == 200
    # check if we see the new item's start date on the resulting page
    index = context['response'].content.decode("utf-8").find('test_item')
    assert index!=-1



# Scenario 2
@pytest.mark.django_db
@scenario(feature_name='../features/seller.feature', scenario_name='Buyer should not be able to create new item')
def test_buyer_creates_new_item():
    print("Finished test_buyer_creates_new_item")

@given("I am a registered buyer")
def i_am_a_registered_buyer(context):
    # flush DB
    os.system("python manage.py flush --no-input")
    client = Client()
    user = User.objects.get_or_create(username='testuser')[0]
    client.force_login(user)
    client.post(homepage+"/User", data={'username': 'Testuser', 'register_as':'Buyer', 'profile_picture':''}, follow=True)
    context['client'] = client

@when("I am go to newItem page")
def i_am_on_my_items_page(context):
    client = context['client']
    response = client.get(homepage+'/newItem')
    context['response'] = response

@then('I should not be allowed to create an item')
def i_should_not_be_allowed_to_create_an_item(context):
    response = context['response']
    assert response.status_code == 403


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
from django.utils import timezone

# Since tests are run only on dev environment, we can use localhost
homepage = 'http://127.0.0.1:8000'

@pytest.fixture(scope='function')
def context():
    return {}

# Scenario #1
@pytest.mark.django_db
@scenario(feature_name='../features/buyer_view.feature', scenario_name='Buyer wants to view items')
def test_buyer_view():
    print("Finished test_buyer_view")



@given("I am a registered user as a buyer")
def i_am_a_registered_user_as_buyer(context):
    # flush DB
    os.system("python manage.py flush --no-input")
    my_user = User.objects.get_or_create(username='Testuser')[0]
    context['my_user'] = my_user
    client = Client()
    client.force_login(my_user)
    response= client.post(homepage+"/User", data={'username': 'buyer_1', 'register_as':'Buyer', 'profile_picture':''}, follow=True)
    assert response.status_code == 200
    context['client'] = client


@given("Seller posts items")
def seller_posts_items(context):
    my_seller = User.objects.get_or_create(username='test_seller')[0]
    context['my_seller'] = my_seller
    client = context['client']
    client.force_login(my_seller)
    response= client.post(homepage+"/User", data={'username': 'seller_1', 'register_as':'Seller', 'profile_picture':''}, follow=True)
    assert response.status_code == 200
    context['client'] = client

    # populate items
    item1 = {'name':'item_1','description': 'desc 1','item_value':100.00,'base_amount':10.00,'increment_amount':1.00}
    item2 = {'name':'item_2','description': 'desc 2','item_value':200.00,'base_amount':20.00,'increment_amount':2.00}
    items = [item1,item2]
    populate_items(items,my_seller.profile)
    


@when("I log in")
def i_enter_my_username_and_register_as_buyer(context):
    context['client'].force_login(context['my_user'])
    response = context['client'].get(homepage+"/Buyer", follow=True)
    context['response'] = response

    
@then('I should be able to see items available for bidding')
def i_should_be_successfully_taken_to_buyer_page(context):
    assert context['response'].status_code == 200
    index = context['response'].content.decode("utf-8").find('item_1')
    assert index!=-1
    index = context['response'].content.decode("utf-8").find('item_1')
    assert index!=-1

def populate_items(items,seller):
    for item in items:
        start_date =  timezone.now()
        end_date = start_date+ timedelta(days=2)
        Item.objects.create(name=item['name'],seller=seller, description=item['description'],
                            item_image=None, start_date=start_date, end_date=end_date,
                            item_value=item['item_value'],
                            base_amount=item['base_amount'],
                            increment_amount=item['increment_amount'],
                            status='Active')
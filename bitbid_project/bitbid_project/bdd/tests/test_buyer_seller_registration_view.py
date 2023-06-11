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
@scenario(feature_name='../features/buyer_seller_registration.feature', scenario_name='First time buyer registration')
def test_buyer_view():
    print("Finished test_buyer_view")

@given("I am a new authenticated user")
def i_am_a_new_authenticated_user(context):
    # flush DB
    os.system("python manage.py flush --no-input")
    my_user = User.objects.get_or_create(username='Testuser')[0]
    context['my_user'] = my_user

@when("I enter my username and register as buyer")
def i_enter_my_username_and_register_as_buyer(context):
    client = Client()
    client.force_login(context['my_user'])
    response = client.post(homepage+"/User", data={'username': 'Testuser', 'register_as':'Buyer', 'profile_picture':''}, follow=True)
    context['client']= client
    response = context['client'].get(homepage+"/Buyer", follow=True)
    context['response'] = response

@then('I should be successfully taken to buyer page')
def i_should_be_successfully_taken_to_buyer_page(context):
    assert context['response'].status_code == 200
    index = context['response'].content.decode("utf-8").find('BUYER')
    assert index!=-1

# Scenario 2
@pytest.mark.django_db
@scenario(feature_name='../features/buyer_seller_registration.feature', scenario_name='First time seller registration')
def test_seller_view():
    print("Finished test_seller_view")

@given("I am a new authenticated user")
def i_am_a_new_authenticated_user(context):
    # flush DB
    os.system("python manage.py flush --no-input")
    my_user = User.objects.get_or_create(username='Testuser')[0]
    context['my_user'] = my_user

@when("I enter my username and register as seller")
def i_enter_my_username_and_register_as_seller(context):
    client = Client()
    client.force_login(context['my_user'])
    response = client.post(homepage+"/User", data={'username': 'Testuser', 'register_as':'Seller', 'profile_picture':''}, follow=True)
    context['client']= client
    response = context['client'].get(homepage+"/Seller", follow=True)
    context['response'] = response

@then('I should be successfully taken to seller page')
def i_should_be_successfully_taken_to_seller_page(context):
    assert context['response'].status_code == 200
    index = context['response'].content.decode("utf-8").find('SELLER')
    assert index!=-1

# Scenario 3
@pytest.mark.django_db
@scenario(feature_name='../features/buyer_seller_registration.feature', scenario_name='First time unknown user type registration')
def test_unknown_user_type_view():
    print("Finished test_unknown_user_type_view")

@given("I am a new authenticated user")
def i_am_a_new_authenticated_user(context):
    # flush DB
    os.system("python manage.py flush --no-input")
    my_user = User.objects.get_or_create(username='Testuser')[0]
    context['my_user'] = my_user

@when("I enter my username and register as someone other than buyer/seller")
def i_enter_my_username_and_register_as_someone_other_than_buyer_seller(context):
    client = Client()
    client.force_login(context['my_user'])
    response = client.post(homepage+"/User", data={'username': 'Testuser', 'register_as':'Garbage', 'profile_picture':''}, follow=True)
    context['client']= client
    context['response'] = response

@then('I should receive an invalid response')
def i_should_receive_an_invalid_response(context):
    print('the response is', context['response'])
    assert context['response'].status_code == 404
import pytest
from pytest_bdd import scenario, given, when, then
from selenium import webdriver
import os

# This will prevent the firefox window to open when running the tests.
# We can remove the line for easier debugging. 
os.environ['MOZ_HEADLESS'] = '1'

# Since tests are run only on dev environment, we can use localhost
homepage = 'http://127.0.0.1:8000'

# geckodriver path
driver_path = '/tmp/geckodriver'

# We define the fixture before the steps so that every other step function can use this
@pytest.fixture
def browser():
    b = webdriver.Firefox(executable_path=driver_path)
    b.implicitly_wait(20)
    yield b
    b.quit()

# Scenario 1
@pytest.mark.django_db
@scenario(feature_name='../features/login.feature', scenario_name='Google authentication for login')
def test_google_authentication():
    print("Finish test")

@given("I am on homepage")
def i_am_on_homepage(browser):
    browser.get(homepage)

@when("I click on Login button")
def click_login(browser):
    browser.find_element("link text", "Login").click()

@then('I should be presented with sign in to google option')
def i_check_to_see(browser):
    assert browser.title == "Sign in - Google Accounts"

# Scenario 3
@pytest.mark.django_db
@scenario(feature_name='../features/login.feature', scenario_name='Unauthenticated access')
def test_unauthenticated_user():
    print("Finish test")

@given("I am an Unauthenticated user")
def i_am_unauthenticated(browser):
    # remain un-authenticated (by default)
    pass

@when("I try to access my user page")
def access_user_profile(browser):
    browser.get(homepage+"/User")

@then('I should be re-directed to homepage')
def stay_on_homepage(browser):
    try:
        browser.find_element("link text", "Login").click()
        assert True
    except:
        assert False
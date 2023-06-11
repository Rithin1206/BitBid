# content of login.feature

Feature: Login

    Scenario: Google authentication for login
        Given I am on homepage

        When I click on Login button

        Then I should be presented with sign in to google option

    Scenario: Login authentication
        Given I enter correct credentials on google login page

        When I click submit

        Then it should display a welcome message on the resulting page

    Scenario: Unauthenticated access
        Given I am an Unauthenticated user 

        When I try to access my user page

        Then I should be re-directed to homepage
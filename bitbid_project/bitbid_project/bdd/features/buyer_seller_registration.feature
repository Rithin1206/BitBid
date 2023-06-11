# content of buyer_seller_registration

Feature: Buyer_seller_registration

    Scenario: First time buyer registration
        Given I am a new authenticated user 

        When I enter my username and register as buyer

        Then I should be successfully taken to buyer page

    Scenario: First time seller registration
        Given I am a new authenticated user 

        When I enter my username and register as seller

        Then I should be successfully taken to seller page

    Scenario: First time unknown user type registration
        Given I am a new authenticated user 

        When I enter my username and register as someone other than buyer/seller

        Then I should receive an invalid response


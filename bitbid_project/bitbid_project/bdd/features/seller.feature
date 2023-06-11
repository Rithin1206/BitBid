# content of buyer_seller_registration

Feature: Seller view

    Scenario: Seller creates new item
        Given I am a registered seller

        When I click on create new item

        Then I should successfuly be allowed to enter item details and submit them

    Scenario: Buyer should not be able to create new item
        Given I am a registered buyer

        When I am go to newItem page

        Then I should not be allowed to create an item


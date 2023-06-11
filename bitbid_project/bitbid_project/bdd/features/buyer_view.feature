# content of buyer_view

Feature: Buyer_view

    Scenario: Buyer wants to view items
        Given I am a registered user as a buyer

        Given Seller posts items

        When I log in

        Then I should be able to see items available for bidding

    Scenario: Buyer wants to view expired items
        Given I am a registered user as a buyer

        When I log in

        Then I should not be able to see expired items


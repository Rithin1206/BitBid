Feature: Seller view

    Scenario: User adds monmey to wallet
        Given I am a registered user
        
        When I click on Add Money

        Then I should see the wallet updated


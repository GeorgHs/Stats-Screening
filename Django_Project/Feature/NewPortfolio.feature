# Created by hertzg at 11.11.2019
Feature: New Portfolio
  Scenario: Check Ticker
    Given I am on the New Portfolio Page
    When I type in Ticker
    And Ticker is correct
    Then Red Check Availability Button should turn to green Add Button
    When I Press Add button
    Then Ticker added to List of Stocks
    

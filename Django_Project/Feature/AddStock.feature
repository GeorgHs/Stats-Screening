# Created by hertzg at 26.12.2019
Feature: AddToolbox
  Add something from toolbox to portfolio
  Scenario: Add Stock
    Given I am on the Portfolio
    When I click on Add Stock
    Then it opens dialog
    Given I enter ticker
    When the ticker is valid
    And I press Add
    Then It adds another row to the portfolio
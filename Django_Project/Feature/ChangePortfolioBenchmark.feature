# Created by hertzg at 28.04.2020
Feature: Benchmark
  is index that stocks are computed against
  Scenario: Change Benchmark
    Given user is logged in
    When I click on portfolio settings
    Then Portfolio Settings show up
    Given Benchmark-Textbox has combobox items
    When I choose combobox items
    Then it selects combobox item
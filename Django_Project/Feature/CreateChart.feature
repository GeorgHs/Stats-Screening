# Created by hertzg at 26.12.2019
Feature: Create Chart
  this is creating a chart
  Scenario: CreateChart
    Given Switch to charts tab
    And  I have my Portfolio opened
    And  I have choosen a prefered chart
    When clicking the create Chart button
    Then It should download the chart in an png format
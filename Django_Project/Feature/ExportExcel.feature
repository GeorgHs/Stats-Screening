# Created by hertzg at 11.11.2019
Feature: ExportFile Test
  Scenario: Exporting Excel File
    Given I am on the PortfolioView Page
    When I press Export Excel
    Then It should output Excel-File
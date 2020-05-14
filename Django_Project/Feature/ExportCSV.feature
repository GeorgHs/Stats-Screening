# Created by hertzg at 11.11.2019
Feature: ExportFile Test
  Scenario: Exporting CSV File
    Given  I am on the PortfolioView Page
    When I press Export CSV
    Then It should output CSV-File
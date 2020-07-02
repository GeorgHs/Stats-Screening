# Created by hertzg at 11.11.2019
Feature: ExportFile Test
  Scenario: Exporting PDF File
    Given I am on the PortfolioView Page
    When I press Export PDF
    Then It should output PDF-File
# Created by hertzg at 28.04.2020
Feature: AccessSavePortfolio
  Open an existing Portfolio of user
  Scenario: OpenPortfolio
    Given Another Portfolio is opened
    When I click on Open Portfolio
    Then it opens dialog
    Given All Portfolios are loaded
    When I select Portfolio
    Then opens Portfolio

  Scenario: SavePortfolio
    Given My Portfolio is opened
    When I click on Save Portfolio
    Then it opens dialog
    And loads name of portfolio (from PortfolioSettings)
    Given Dialog is loaded
    When I click save
    Then saves Portfolio
# Created by hertzg at 28.04.2020
Feature: HistoricalData
  load prices of stocks into dictionary
  Scenario: Refresh Portfolio
    Given the portfolio is open
    When I click on Refresh whole portfolio
    And Ticker is correct
    Then fetch stock prices for 1 year
    When All prices are fetched
    Then Compute daily returns
  Scenario: Add Figure
    Given the portfolio is open
    When I type in Ticker
    And Ticker is correct
    Then Check if Benchmark prices are already existent for 1 year
    When Benchmark prices are already existent for 1 year
    Then Compute daily returns
  Scenario: Recompute column
    Given the portfolio is open
    When I type in Ticker
      And Ticker is correct
    Then Check if Benchmark prices are already existent for 1 year
    When Benchmark prices are already existent for 1 year
    Then Compute daily returns

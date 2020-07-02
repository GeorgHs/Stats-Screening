# Created by hertzg at 29.04.2020
Feature: Listing all Tickers
  list of all tickers that can be selected
  Scenario: adding tickers to benchmark
    Given user is logged in
    When user enters Ticker of Index
    And clicks 'Add Stock-Ticker of Benchmark'
    Then check if Index-Ticker is existent
    Given Index-Ticker is existent
    Then add all tickers of Index to List
# Created by hertzg at 26.12.2019
Feature: Refreshing Portfolio
  wanting to refresh the portfolio
  Scenario: user starts refresh
    Given the Portfolio is opened
    When rightclick on table
    Then contextmenu shows up
    Given contextmenu is open
    When I click on Refresh whole Portfolio
    Then it refreshes
  Scenario: more than 20 stocks to reload
    Given refreshing has been initiated
    When portfolio contains above 20 stocks
    Then progressbar in dialog shows up
  Scenario: ticker not working
    Given refreshing has been initiated
    When ticker not working
    Then show Errordialog
    And stop
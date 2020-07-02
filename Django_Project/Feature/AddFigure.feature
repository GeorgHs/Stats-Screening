# Created by hertzg at 26.12.2019
Feature: AddToolbox
  Add something from toolbox to portfolio
  Scenario: AddFigure
   Given I am in Toolbox on the left side
    And  I have my Portfolio opened
    When I drag&drop on specific Figure
    Then it should add column to my portfolio
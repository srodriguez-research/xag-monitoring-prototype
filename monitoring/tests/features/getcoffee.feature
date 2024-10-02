# Simple feature just for testing
@goal
Feature: GetCoffee
  As researcher ,
  I want to GetCoffee
  so I can finish my AAMAS experiments
  
  @goal-plan
  Scenario: plan-KitchenCoffee
    Given I believe staffCardAvailable is true
    When I adopt the GetCoffee goal
    Then plan KitchenCoffee is applicable
  

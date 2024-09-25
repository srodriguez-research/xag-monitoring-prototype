@goal
Feature: GetCoffee

  As researcher ,
  I want to GetCoffee
  so I can finish my AAMAS experiments
  
  # @goal-success
  # Scenario: goal-success
  #   Given I believe coffee is present
  #   When I evaluate current_goal success
  #   Then goal success is true

  @goal-plan
  Scenario: plan-KitchenCoffee
    Given I believe staffCardAvailable is true
    When I adopt the GetCoffee goal
    Then plan KitchenCoffee is applicable
  
  @goal-plan
  Scenario: plan-OfficeCoffee
    Given I believe annInOffice is true
    When I adopt the GetCoffee goal
    Then plan OfficeCoffee is applicable

  @goal-plan
  Scenario: plan-KitchenCoffee
    Given I believe haveMoney is true
    When I adopt the GetCoffee goal
    Then plan ShopCoffee is applicable

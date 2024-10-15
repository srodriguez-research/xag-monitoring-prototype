@goal
Feature: GetCoffee
  As researcher,
  I want to GetCoffee
  so I can finish my AAMAS experiments
  
  @goal-plan
  Scenario: plan-kitchencoffee
    Given I believe staffCardAvailable is true
    When I adopt the GetCoffee goal
    Then plan KitchenCoffee is applicable
  
  @goal-plan
  Scenario: plan-officecoffee
    Given I believe annInOffice is true
    When I adopt the GetCoffee goal
    Then plan OfficeCoffee is applicable

  @goal-plan
  Scenario: plan-shopcoffee
    Given I believe haveMoney is true
    When I adopt the GetCoffee goal
    Then plan ShopCoffee is applicable

  @goal-plan-preference @rating
  Scenario Outline: plan-rating
    Given I have an applicable plan with valuing coffee.quality <quality>
    Given I have an applicable plan with valuing cost <cost>
    When I select the plan
    Then I rate it with <rate>
    And I select the highest-rated plan

    Examples:
      | quality   | cost | rate |
      | VERY_GOOD | NONE | 1.0  |
      | VERY_GOOD | HIGH | 0.7  |
      | GOOD      | NONE | 0.6  |
      | GOOD      | HIGH | 0.4  |
      | BAD       | NONE | 0.3  |
      | BAD       | HIGH | 0.2  |


  # @goal-success
  # Scenario: goal-success
  #   Given I believe coffee is present
  #   When I evaluate current_goal success
  #   Then goal success is true
  #

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

  @goal-preference
  Scenario: pref-quality
    Given I could have OfficeCoffee  with coffee.quality GOOD for cost None
    And I could have ShopCoffee with coffee.quality VERY_GOOD for cost HIGH
    When I select the plan
    Then I select ShopCoffee

  @goal-preference
  Scenario Outline: pref-quality
    Given I have <option1> with coffee.quality <quality1> for cost <cost1>
    And I have <option2 > coffee.quality <quality2> for cost <cost2>
    When I select the plan
    Then I select <result>

    Examples:
      | option1    | quality1  | price1 | option2      | quality2 | price2 | result     | 
      | ShopCoffee | VERY_GOOD | HIGH   | OfficeCoffee | GOOD     | None   | ShopCoffee | 

  @goal-success
  Scenario: goal-success
    Given I believe coffee is present
    When I evaluate current_goal success
    Then goal success is true


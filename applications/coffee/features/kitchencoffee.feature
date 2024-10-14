@plan
Feature: Get Kitchen Coffee
  As researcher,
  I want to get Coffee from the Kitchen
  so I can Get Coffee

  # New tag to reference the goal Scenario so this spec is self-contained
  # Not sure is a best way to do it in a strict BDD  
  @plan-applicability(GetCoffee.plan-KitchenCoffee)
  Scenario: applicable
    Given I believe staffCardAvailable is true
    When I adopt the GetCoffee goal
    Then plan KitchenCoffee is applicable

  @plan-achieves-goal
  Scenario: Have Coffee
    When plan completes
    Then I believe coffee.present is true

  # Rename plan-actions (AAMAS23) to plan-steps to be more generic
  @plan-steps 
  Scenario: plan-steps
    When I start the plan 
    Then I post the subgoal GetStaffCard

  @plan-steps 
  Scenario: plan-steps
    Given I have achieved GetStaffCard
    And I believe haveCard is true # must be if achieved GetStaffCard
    When I progress the plan
    Then I do action goto(Kitchen)


  @plan-steps 
  Scenario: plan-steps
    Given I believe location is KITCHEN
    And I believe haveCard is true
    When I progress the plan
    Then I do action obatainCoffee
    # changed GetCoffee(Kitchen) to obatainCoffee to avoid confusion

  @plan-valueings
  Scenario: valueings
    When plan is rated
    Then future value of coffee.quality is expected to be BAD
    And future value of cost is expected to be None

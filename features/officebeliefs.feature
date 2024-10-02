@belief
Feature: Office Coffee Beliefs
  As a research, 
  I want to infer belief based on my perceptions
  so I can make better decisions

  @belief-infer
  Scenario: staffCardAvaible based on ownCard
    Given I believe ownCard is true
    When I query belief staffCardAvaible
    Then I believe staffCardAvaible is true


  @belief-infer
  Scenario: staffCardAvaible based on colleagueAvailable
    Given I believe colleagueAvailable is true
    When I query belief staffCardAvaible
    Then I believe staffCardAvaible is true
  
  @belief-infer
  Scenario: staffCardAvaible false
    Given I believe colleagueAvailable is false
    Given I believe ownCard is false
    When I query belief staffCardAvaible
    Then I believe staffCardAvaible is false

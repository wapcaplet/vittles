Feature: Shopping list

  Scenario: Manually add items to shopping list
    Given I have an empty shopping list
    When I add "potatoes" to my shopping list
    Then I should see "potatoes" on my shopping list

  Scenario: Add to shopping list when a recipe is used
    Given I have the following in my pantry:
      | flour | 1 | pound |
      | milk  | 1 | gallon |
    And I have an empty shopping list
    When I make a recipe using:
      | flour | 1 | pound |
      | milk  | 2 | cups  |
    Then my shopping list should include:
      | flour |


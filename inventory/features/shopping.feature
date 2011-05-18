Feature: Shopping list

  Scenario: Manually add items to shopping list
    Given I have an empty shopping list
    When I add "potatoes" to my shopping list
    Then my shopping list should include:
      | flour |

  Scenario: Add to shopping list when a recipe is used
    Given I have a pantry containing:
      | food  | qty | unit   |
      | flour | 1   | pound  |
      | milk  | 1   | gallon |
    And I have an empty shopping list
    When I make a recipe using:
      | food  | qty | unit  |
      | flour | 1   | pound |
      | milk  | 2   | cups  |
    Then my shopping list should include:
      | food  |
      | flour |


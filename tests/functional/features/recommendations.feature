Feature: recommendations
  Get recommendations for a user

  Background:
    Given a trained recommender model
    And a running recommendation server

  Scenario Outline: Recommend items for an existing user
    Given the recommend API is called with <user_id> and <num_recs>
    Then the response status code is "200"
    And the response returns a list of recommendations 
    And the response has <num_recs> items
    Examples:
      | user_id  |  num_recs  |
      | 1        |  5         |
      | 2        |  10        |
      | 3        |  15        |

  Scenario Outline: Recommend items for a new user
    Given the recommend API is called with <user_id> and <num_recs>
    Then the response status code is "200"
    And the response returns a list of recommendations
    Examples:
      | user_id   |  num_recs  |
      | -1        |  5         |
      | -2        |  10        |
      | -3        |  15        |

  Scenario Outline: Get recommendations from the default algorithm
    Given the default recommendation endpoint is called with <user_id> and <num_recs>
    Then the response status code is "200"
    And the response returns a list of recommendations
    Examples:
      | user_id  |  num_recs  |
      | 1        |  5         |
      | 2        |  10        |
      | 3        |  15        |
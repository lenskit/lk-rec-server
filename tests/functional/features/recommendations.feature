Feature: recommendations
  Get recommendations for a user

  Scenario Outline: Recommend items for an existing user
    Given the recommend API is called with <user_id> and <num_recs>
    Then the response status code is "200"
    And the response returns a result list for <user_id> and <num_recs>

    Examples:
      | user_id  |  num_recs  |
      | 1        |  5         |
      | 2        |  10        |
      | 3        |  15        |

  Scenario Outline: Recommend items for a new user
    Given the recommend API is called with <user_id> and <num_recs>
    Then the response status code is "200"
    And the response returns a result list for <user_id> and <num_recs>

        Examples:
      | user_id   |  num_recs  |
      | -1        |  5         |
      | -2        |  10        |
      | -3        |  15        |
Feature: predictions
  Get predictions for a user

  Background:
    Given a trained recommender model
    And a running recommendation server

  Scenario Outline: Get items predictions for an existing user
    Given the predict API is called with <user_id> and <items>
    Then the response status code is "200"
    And the response returns a list of predictions 
    Examples:
      | user_id  |  items       |
      | 1        |  1,10        |
      | 2        |  2,20        |
      | 3        |  3,30        |  

  Scenario Outline: Get items predictions for a new user
    Given the predict API is called with <user_id> and <items>
    Then the response status code is "200"
    And the response returns an empty list
    Examples:
      | user_id   |  items      |
      | -1        |  1,10       |
      | -2        |  2,20       |
      | -3        |  3,30       |
    
  Scenario Outline: Get items predictions for non existing items
    Given the predict API is called with <user_id> and <items>
    Then the response status code is "200"
    And the response returns an empty list
    Examples:
      | user_id   |  items        |
      | 1        |  -1,-10       |
      | 2        |  -2,-20       |
      | 3        |  -3,-30       |

  Scenario Outline: Get items predictions for a user with new ratings
    Given the predict API is called with <user_id> and <items>
    Then the response status code is "200"
    And the response returns a list of predictions 
    Examples:
      | user_id   |  items      |
      | 4         |  10,100     |

  Scenario Outline: Get items predictions for a new user with new ratings
    Given the predict API is called with <user_id> and <items>
    Then the response status code is "200"
    And the response returns an empty list
    Examples:
      | user_id   |  items      |
      | 0         |  10,100     |            
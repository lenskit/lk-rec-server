Feature: models
  Get model information

  Background:
    Given a running recommendation server

  Scenario Outline: Upload a new model
    Given upload model for <algo>
    Then the response status code is "200" and the json result is 200
    Examples:
      | algo        |  
      | popular     |
      | bias        |
      | topn        |
      | implicitmf  |
      | biasedmf    |

  Scenario Outline: Get model info for an existing model file
    Given a trained recommender model for <algo>
    Then the response status code is "200"
    And the response returns the model creation_date and size
    Examples:
      | algo        |  
      | popular     |
      | bias        |
      | topn        |
      | implicitmf  |
      | biasedmf    |

  Scenario Outline: Get model info for a non-existing model file
    Given a trained recommender model for <algo>
    Then the response status code is "200"
    And the response returns empty information for the model
    Examples:
      | algo        |  
      | no_popular  |
      | bias2       |
      | topn10      |
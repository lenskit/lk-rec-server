Feature: models
  Get model information

  Background:
    Given a running recommendation server

  Scenario Outline: Get model info for an existing model file
    Given a trained recommender model for <algo>
    Then the response status code is "200"
    And the response returns the model creation_date and size
    Examples:
      | algo        |  
      | popular     |
      | bias        |
      | topn        |
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

  Scenario Outline: Upload a new model
    #Given a trained recommender model for <algo>
    Given upload model for <algo>
    Then the response status code is "200" and "Ok"
    Examples:
      | algo        |  
      | popular     |
      | bias        |
      | topn        |
      | implicitmf    |
Feature: predictions
  Get predictions for a user

  Background:
    Given a trained ALS recommender model
    And a running recommendation server

  Scenario Outline: Get items predictions for an existing user

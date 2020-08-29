Recommendation Server for Lenskit
====================================

Recommendation Server for Lenskit is a web server that exposes LensKit’s recommendation and rating prediction capabilities.

Endpoints:

.. http:get:: | POST /recommendations

    Get `num_recs` recommendations from the default configured algorithm for the `user_id` sent.

    **Example requests**:

    .. sourcecode:: none

        GET /recommendations/?user_id=1&num_recs=5
        Host: example.com
        Accept: application/json, text/javascript

    .. sourcecode:: none

        POST /recommendations
        Data: { "user_id" : 1, "num_recs" : 5 }
        Host: example.com
        Accept: application/json, text/javascript        

    **Example response**:

    .. sourcecode:: none

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json
        {
        "recommendations": [
                {
                    "item": 356.0, 
                    "score": 341.0
                }, 
                {
                    "item": 296.0, 
                    "score": 324.0
                }, 
                {
                    "item": 318.0, 
                    "score": 311.0
                }, 
                {
                    "item": 593.0, 
                    "score": 304.0
                }, 
                {
                    "item": 260.0, 
                    "score": 291.0
                }
            ]
        }
    
    :query int user_id: user id to get recommendations for
    :query int num_recs: number of recommendations to return

    :jsonparam int user_id: user id to get recommendations for.
    :jsonparam int num_recs: number of recommendations to return.

.. http:get:: | POST /algorithms/(string:algo)/recommendations

    Get `num_recs` recommendations using the `algorithm` and `user_id` sent.

    **Example requests**:

    .. sourcecode:: none

        GET /algorithms/popular/recommendations?user_id=1&num_recs=5
        Host: example.com
        Accept: application/json, text/javascript

    .. sourcecode:: none

        POST /algorithms/popular/recommendations
        Data: { "user_id" : 1, "num_recs" : 5 }
        Host: example.com
        Accept: application/json, text/javascript        

    **Example response**:

    .. sourcecode:: none

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json
        {
        "recommendations": [
                {
                    "item": 356.0, 
                    "score": 341.0
                }, 
                {
                    "item": 296.0, 
                    "score": 324.0
                }, 
                {
                    "item": 318.0, 
                    "score": 311.0
                }, 
                {
                    "item": 593.0, 
                    "score": 304.0
                }, 
                {
                    "item": 260.0, 
                    "score": 291.0
                }
            ]
        }
    
    :query int user_id: user id to get recommendations for
    :query int num_recs: number of recommendations to return

    :jsonparam int user_id: user id to get recommendations for.
    :jsonparam int num_recs: number of recommendations to return.

.. http:get:: | POST /algorithms/(string:algo)/predictions

    Get predictions using the `algorithm`, `user_id` and `items` sent.

    **Example requests**:

    .. sourcecode:: none

        GET /algorithms/bias/predictions?user_id=1&items=5,102,203,304,400
        Host: example.com
        Accept: application/json, text/javascript

    .. sourcecode:: none

        POST /algorithms/bias/predictions
        Data: { "user_id" : 1, "items" : 5,102,203,304,400 }
        Host: example.com
        Accept: application/json, text/javascript        

    **Example response**:

    .. sourcecode:: none

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json
        {
        "predictions": [
                {
                    "item": 5, 
                    "score": 3.268
                }, 
                {
                    "item": 102, 
                    "score": 2.591
                }, 
                {
                    "item": 203, 
                    "score": 3.304
                }, 
                {
                    "item": 304, 
                    "score": 3.333
                }, 
                {
                    "item": 400, 
                    "score": 3.544
                }
            ]
        }
    
    :query int user_id: user id to get predictions for
    :query list_of_ints items: items to get predictions for

    :jsonparam int user_id: user id to get predictions for
    :jsonparam list_of_ints items: items to get predictions for

.. http:get:: /algorithms/(string:algo)/info

    Get the model file information from the `algorithm` sent.

    **Example requests**:

    .. sourcecode:: none

        GET /algorithms/popular/info
        Host: example.com
        Accept: application/json, text/javascript   

    **Example response**:

    .. sourcecode:: none

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json
        {
            "model": {
                "creation_date": "2020-08-28 18:38:42", 
                "size": 200.826, 
                "updated_date": "2020-08-21 18:32:55"
            }
        }

.. http:put:: /algorithms/(string:algo)/modelfile

    Update the model file for the `algorithm` and `file` sent.

    **Example requests**:

    .. sourcecode:: none

        GET /algorithms/popular/info
        Host: example.com
        Accept: application/json, text/javascript   

    **Example response**:

    .. sourcecode:: none

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json
        { 'result' : 200 }
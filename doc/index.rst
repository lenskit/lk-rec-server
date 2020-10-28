The recommendation server for Lenskit
==========================================

The recommendation server for Lenskit is a web server that exposes LensKit’s recommendation and rating prediction capabilities.

The recommendation server makes it much easier to use LensKit in deployed applications and interactive research where end users 
are actively involved, extending the reach and research impact of LensKit. The user of the recommendation server can be anyone 
who knows how to build a web application, such as a software developer or a researcher. They need to create an application, 
which will itself have end users, and the recommendation server will generate recommendations for them. The recommendation server 
is able to handle multiple concurrent requests and load and reload of recommendation models. It also provides recommendations 
on demand based on the latest ratings end users have provided. 

.. toctree::
    :maxdepth: 2
    :caption: Overview

    userguide
    configuration
    deployment
    training_quality
    endpoints

.. toctree::
    :maxdepth: 2
    :caption: Results
    
    examples
    accuracy
    performance
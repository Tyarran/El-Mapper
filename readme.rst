El Mapper
#########

Goal
----
The goal is to create a Mapper system to import easy data from a CSV (or whatever) feed. The system would be used mainly for seller feed import.

Why
---
When importing a seller feed, we have to match the feed columns with our internal attributes
For attributes that are a Choices List or a foreign key (Brand, Category, etc.), we need to map the ids from the seller external system with our ids.

Installation
------------

from sources
############

.. code-block:: bash

    git clone https://github.com/rcommande/El-Mapper.git 
    cd El-Mapper
    # Standard installation
    pip install -r requirements.ext
    # In develop installation
    pip install -r requirements-develop.txt

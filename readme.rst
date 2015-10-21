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
    cd elmapper
    python manage.py migrate
    python manage.py createsuperuser

Run application
---------------

.. code-block:: bash

    python manage.py runserver

Go to http://localhost:8000/

Usage
-----

* The database must be filled with the DJango Administration site: http://localhost:8000.
* Add brands, colors and categories objects
* Upload impload a Product CSV
* Create a mapping configuration (read Mapping configuration specifications first)
* Try to perform a mapping et see the result

Mapping configuration specifications
------------------------------------

The Mapping configuration is a JSON like:

.. code-block:: json

    [
        {
            "foreign_key_mapping": [
                {
                    "pattern": "pk", 
                    "external_fk": "3", 
                    "internal_value": "1"
                }
            ], 
            "external_name": "category", 
            "model_name": "category"
        }, 
    ]

**external_name**: the CSV column
**model_name**: the Product field corresponding to the CV column 
**foreign_key_mapping**: a list of foreign key mapping
    **external_fk**: a CSV value
    **internal_value**: the internal value (or primary key)
    **pattern (optional)**: the subobject field where the value should be sought  

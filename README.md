# etc - various handy scripts

In general scripts have a help (run with -h/--help) and have no dependencies, other than microcouch.

## fetch\_subset.py

Copy a subset of documents from one database to another.


## gen\_docs.py

Generate realistic random documents based on a schema. Data types are:

 * **int** - options: min, max
 * **float** - options: min, max
 * **string** - options: length
 * **ipsum** - options: lines
 * **choice** - options: values (list)
 * **bool** - options: *no options*
 * **name** - options: *no options*

Example schema:

    {
        "player": {"type": "name"},
        "score": {"type": "int", "min":0, "max": 1000000},
        "game": {"type": "choice", "values": ["jetpack george", "mega plumber", "avenue warrior", "space conflict"]}
    }

## microcouch.py

Minimal python Couch API, creates a DB, pushes documents into it.


## situp.py

Deals with more complex CouchApps (including those that use chained MR).

See http://drsm79.github.com/situp

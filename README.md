# etc - various handy scripts

In general scripts have a help (run with -h/--help) and have no dependencies, other than microcouch.

## fetch\_subset.py

Copy a subset of documents from one database to another.


## gen\_docs.py

Generate realistic random documents based on a schema. Data types are:

 * **int**: random integer between `min`/`max` - options: `min`, `max`
 * **float**: random float between `min`/`max` - options: `min`, `max`
 * **string**: random string, length <=15 - options: *no options*
 * **seededstring**: random string, length <=15 appended to `seed` - options: `seed`
 * **ipsum**: lines of lorem ipsum text - options: `lines`
 * **choice**: random pick from a list of `values` - options: `values` (list)
 * **bool**: random `true`/`false` - options: *no options*
 * **name**: random name chosen from 100 popular names - options: *no options*
 * **nest**: a nested structure, `value` should be another type (including nest) - options: value

Example schema:

    {
        "player": {"type": "name"},
        "score": {"type": "int", "min":0, "max": 1000000},
        "game": {"type": "choice", "values": ["jetpack george", "mega plumber", "avenue warrior", "space conflict"]},
        "a": {"type": "nest", "value": {
          "b": {
            "type": "nest", "value": {
              "string": {"type": "string"},
              "integer": {"max": 1000000, "type": "int", "min": 0}
            }
          }
        }
      }
    }

For a more complete example check out test.json.

Depends on [requests](http://docs.python-requests.org/).

## microcouch.py

Minimal python Couch API, creates a DB, pushes documents into it.


## situp.py

Deals with more complex CouchApps (including those that use chained MR).

See http://drsm79.github.com/situp

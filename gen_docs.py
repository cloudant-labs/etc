import random
import json
import time
import datetime
import requests
import string
import sys
import getpass
from optparse import OptionParser
from urlparse import urlparse, urlunparse

names = ["Isabella", "Sophia", "Emma", "Olivia", "Ava", "Emily", "Abigail",
         "Madison", "Chloe", "Mia", "Addison", "Elizabeth", "Ella", "Natalie",
         "Samantha", "Alexis", "Lily", "Grace", "Hailey", "Alyssa", "Lillian",
         "Hannah", "Avery", "Leah", "Nevaeh", "Sofia", "Ashley", "Anna",
         "Brianna", "Sarah", "Zoe", "Victoria", "Gabriella", "Brooklyn",
         "Kaylee", "Taylor", "Layla", "Allison", "Evelyn", "Riley", "Amelia",
         "Khloe", "Makayla", "Aubrey", "Charlotte", "Savannah", "Zoey",
         "Bella", "Kayla", "Alexa", "Jacob", "Ethan", "Michael", "Jayden",
         "William", "Alexander", "Noah", "Daniel", "Aiden", "Anthony",
         "Joshua", "Mason", "Christopher", "Andrew", "David", "Matthew",
         "Logan", "Elijah", "James", "Joseph", "Gabriel", "Benjamin", "Ryan",
         "Samuel", "Jackson", "John", "Nathan", "Jonathan", "Christian",
         "Liam", "Dylan", "Landon", "Caleb", "Tyler", "Lucas", "Evan", "Gavin",
         "Nicholas", "Isaac", "Brayden", "Luke", "Angel", "Brandon", "Jack",
         "Isaiah", "Jordan", "Owen", "Carter", "Connor", "Justin"]


def gen_doc(schema, counter=0):
    doc = {}
    for field in schema.keys():
        doc[field] = schema[field](counter)
    return doc


def options():
    parser = OptionParser()
    parser.add_option("-u",
                      "--url",
                      default="http://localhost:5984/test",
                      help="Url of the database - don't put password in "
                           "it [default %default]")
    parser.add_option("-s",
                      "--schema",
                      default="schema.json",
                      help="JSON file describing the schema of documents "
                           "to generate [default %default]")
    parser.add_option("-n",
                      "--number",
                      default=10,
                      type="int",
                      help="Number of docs to generate [default %default]")
    parser.add_option("-b",
                      "--batch",
                      default=500,
                      type="int",
                      help="Batch size (push this many docs per request)"
                           " [default %default]")
    opts, args = parser.parse_args()
    return opts, args


def ipsum(nlines):
    #This text is under public domain
    #Lorem ipsum
    #Cicero
    ipsum_text = u"""lorem ipsum dolor sit amet consetetur sadipscing elitr sed
    diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat
    sed diam voluptua at vero eos et accusam et justo duo dolores et ea rebum
    stet clita kasd gubergren no sea takimata sanctus est lorem ipsum dolor sit
    amet lorem ipsum dolor sit amet consetetur sadipscing elitr sed diam nonumy
    eirmod tempor invidunt ut labore et dolore magna aliquyam erat sed diam
    voluptua at vero eos et accusam et justo duo dolores et ea rebum stet clita
    kasd gubergren no sea takimata sanctus est lorem ipsum dolor sit amet lorem
    ipsum dolor sit amet consetetur sadipscing elitr sed diam nonumy eirmod
    tempor invidunt ut labore et dolore magna aliquyam erat sed diam voluptua
    at vero eos et accusam et justo duo dolores et ea rebum stet clita kasd
    gubergren no sea takimata sanctus est lorem ipsum dolor sit amet

    duis autem vel eum iriure dolor in hendrerit in vulputate velit esse
    molestie consequat vel illum dolore eu feugiat nulla facilisis at vero eros
    et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril
    delenit augue duis dolore te feugait nulla facilisi lorem ipsum dolor sit
    amet consectetuer adipiscing elit sed diam nonummy nibh euismod tincidunt
    ut laoreet dolore magna aliquam erat volutpat

    ut wisi enim ad minim veniam quis nostrud exerci tation ullamcorper
    suscipit lobortis nisl ut aliquip ex ea commodo consequat duis autem vel
    eum iriure dolor in hendrerit in vulputate velit esse molestie consequat
    vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et
    iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis
    dolore te feugait nulla facilisi

    nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet
    doming id quod mazim placerat facer possim assum lorem ipsum dolor sit
    amet consectetuer adipiscing elit sed diam nonummy nibh euismod tincidunt
    ut laoreet dolore magna aliquam erat volutpat ut wisi enim ad minim veniam
    quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex
    ea commodo consequat

    duis autem vel eum iriure dolor in hendrerit in vulputate velit esse
    molestie consequat vel illum dolore eu feugiat nulla facilisis

    at vero eos et accusam et justo duo dolores et ea rebum stet clita kasd
    gubergren no sea takimata sanctus est lorem ipsum dolor sit amet lorem
    ipsum dolor sit amet consetetur sadipscing elitr sed diam nonumy eirmod
    tempor invidunt ut labore et dolore magna aliquyam erat sed diam voluptua
    at vero eos et accusam et justo duo dolores et ea rebum stet clita kasd
    gubergren no sea takimata sanctus est lorem ipsum dolor sit amet lorem
    ipsum dolor sit amet consetetur sadipscing elitr at accusam aliquyam diam
    diam dolore dolores duo eirmod eos erat et nonumy sed tempor et et invidunt
    justo labore stet clita ea et gubergren kasd magna no rebum sanctus sea sed
    takimata ut vero voluptua est lorem ipsum dolor sit amet lorem ipsum dolor
    sit amet consetetur sadipscing elitr sed diam nonumy eirmod tempor invidunt
    ut labore et dolore magna aliquyam erat

    consetetur sadipscing elitr sed diam nonumy eirmod tempor invidunt ut
    labore et dolore magna aliquyam erat sed diam voluptua at vero eos et
    accusam et justo duo dolores et ea rebum stet clita kasd gubergren no sea
    takimata sanctus est lorem ipsum dolor sit amet lorem ipsum dolor sit amet
    consetetur sadipscing elitr sed diam nonumy eirmod tempor invidunt ut
    labore et dolore magna aliquyam erat sed diam voluptua at vero eos et
    accusam et justo duo dolores et ea rebum stet clita kasd gubergren no sea
    takimata sanctus est lorem ipsum dolor sit amet lorem ipsum dolor sit amet
    consetetur sadipscing elitr sed diam nonumy eirmod tempor invidunt ut
    labore et dolore magna aliquyam erat sed diam voluptua at vero eos et
    accusam et justo duo dolores et ea rebum stet clita kasd gubergren no sea
    takimata sanctus est lorem ipsum dolor sit amet"""

    # Done this way in case I decide to do words/paragraphs/sentences
    lorem_text = ipsum_text.replace('\n\n', '\n')
    lines = lorem_text.split('\n')
    return "\n".join(lines[:nlines])


def randdate(field):
    """
    Return a random date between two dates, either as epoch seconds or human
    readable string.
    """
    timefmt = "%B %d, %Y %H:%M:%S"
    if 'format' in field.keys() and field['format'] != 'stamp':
        start = int(time.mktime(time.strptime(field['start'], timefmt)))
        end = int(time.mktime(time.strptime(field['end'], timefmt)))
    else:
        start = field['start']
        end = field['end']

    stamp = random.randint(start, end)

    if 'output' not in field.keys() or field['output'] == 'stamp':
        return stamp
    elif field['output'] == 'string':
        return datetime.datetime.fromtimestamp(stamp).strftime(timefmt)


def nest(field):
    obj = {}
    value = field["value"]
    for k, v in value.items():
        obj[k] = bind_function(v)(v)
    return obj


def bind_function(field):
    """
    Return the appropriate (lambda) function for the given field
    """
    t = field['type']
    try:
        if t == 'int':
            return lambda x: random.randint(field['min'], field['max'])
        elif t == 'float':
            return lambda x: field['min'] + ((field['max'] - field['min']) * random.random())
        elif t == 'string':
            return lambda x: ''.join(random.choice(string.letters) for i in xrange(random.randint(1, 15))).lower()
        elif t == 'seededstring':
            return lambda x: field['seed'] + ''.join(random.choice(string.letters) for i in xrange(random.randint(1, 15))).lower()
        elif t == 'ipsum':
            return lambda x: ipsum(field['lines'])
        elif t == 'choice':
            return lambda x: random.choice(field['values'])
        elif t == 'bool':
            return lambda x: bool(random.randint(0,1))
        elif t == 'name':
            return lambda x: random.choice(names)
        elif t == 'date':
            return lambda x: randdate(field)
        elif t == 'fixed':
            return lambda x: field['value']
        elif t == 'nest':
            return lambda x: nest(field)
        elif t == 'counter':
            return lambda x: x * field.get("multiplier", 1) + field.get("offset", 0)
        else:
            print 'Unknown field type, exiting'
            sys.exit(1)
    except KeyError, k:
        print k
        sys.exit(1)


def bulk(url, docs, auth):
    resp = requests.post(url,
                         data=json.dumps({"docs": docs}),
                         headers={'content-type': 'application/json'},
                         auth=auth)
    if resp.status_code > 250:
        print resp.text
    else:
        print "%s docs posted" % len(docs)


def parse_url(url):
    parsed_url = urlparse(url)
    url = '%s/_bulk_docs' % url
    auth = ()
    netloc = parsed_url.netloc
    try:
        if netloc.index('@') > -1:
            netloc = netloc.split('@')[1]
    except:
        pass
    url = urlunparse([parsed_url.scheme,
                      netloc,
                      parsed_url.path,
                      '', '', ''])
    if parsed_url.password:
        auth = (parsed_url.username, parsed_url.password)
    elif parsed_url.username:
        auth = (parsed_url.username, getpass.getpass())

    return url, auth


if __name__ == "__main__":
    opts, args = options()

    schema = json.load(open(opts.schema))
    function_schema = {}
    for field in schema:
        function_schema[field] = bind_function(schema[field])

    url, auth = parse_url(opts.url)
    # Quickest way to check the db exists and create it if not
    r = requests.put(url,
                     auth=auth,
                     headers={'content-type': 'application/json'},)

    if r.status_code > 220:
        print r.text

    url = '%s/_bulk_docs' % url
    print "writing to {0}".format(url)

    docs = []

    for d in xrange(opts.number):
        docs.append(gen_doc(function_schema, d))
        if len(docs) >= opts.batch:
            bulk(url, docs, auth)
            docs = []
    if len(docs) > 0:
        bulk(url, docs, auth)

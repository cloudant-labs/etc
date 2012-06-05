import random
import json
import time
import datetime
from optparse import OptionParser
from microcouch import MicroCouch

names = ["Isabella", "Sophia", "Emma", "Olivia", "Ava", "Emily", "Abigail",
        "Madison", "Chloe", "Mia", "Addison", "Elizabeth", "Ella", "Natalie",
        "Samantha", "Alexis", "Lily", "Grace", "Hailey", "Alyssa", "Lillian",
        "Hannah", "Avery", "Leah", "Nevaeh", "Sofia", "Ashley", "Anna",
        "Brianna", "Sarah", "Zoe", "Victoria", "Gabriella", "Brooklyn",
        "Kaylee", "Taylor", "Layla", "Allison", "Evelyn", "Riley","Amelia",
        "Khloe", "Makayla", "Aubrey", "Charlotte", "Savannah", "Zoey", "Bella",
        "Kayla", "Alexa", "Jacob", "Ethan", "Michael", "Jayden", "William",
        "Alexander", "Noah", "Daniel", "Aiden", "Anthony", "Joshua", "Mason",
        "Christopher", "Andrew", "David", "Matthew", "Logan", "Elijah",
        "James", "Joseph", "Gabriel", "Benjamin", "Ryan", "Samuel", "Jackson",
        "John", "Nathan", "Jonathan", "Christian", "Liam", "Dylan", "Landon",
        "Caleb", "Tyler", "Lucas", "Evan", "Gavin", "Nicholas", "Isaac",
        "Brayden", "Luke", "Angel", "Brandon", "Jack", "Isaiah", "Jordan",
        "Owen", "Carter","Connor", "Justin"]


def gen_doc(schema):
    doc = {}
    for field in schema.keys():
        doc[field] = schema[field]()
    return doc

def options():
    parser = OptionParser()
    parser.add_option("-u", "--url", default="http://localhost:5984/test",
            help="Url of the database - don't put password in it [default %default]")
    parser.add_option("-s", "--schema", default="schema.json",
            help="JSON file describing the schema of documents to generate [default %default]")
    parser.add_option("-n","--number", default=10, type="int",
            help="Number of docs to generate [default %default]")
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
    amet consectetuer adipiscing elit sed diam nonummy nibh euismod tincidunt ut
    laoreet dolore magna aliquam erat volutpat

    ut wisi enim ad minim veniam quis nostrud exerci tation ullamcorper suscipit
    lobortis nisl ut aliquip ex ea commodo consequat duis autem vel eum iriure
    dolor in hendrerit in vulputate velit esse molestie consequat vel illum
    dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio
    dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te
    feugait nulla facilisi

    nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet
    doming id quod mazim placerat facer possim assum lorem ipsum dolor sit amet
    consectetuer adipiscing elit sed diam nonummy nibh euismod tincidunt ut
    laoreet dolore magna aliquam erat volutpat ut wisi enim ad minim veniam quis
    nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea
    commodo consequat

    duis autem vel eum iriure dolor in hendrerit in vulputate velit esse
    molestie consequat vel illum dolore eu feugiat nulla facilisis

    at vero eos et accusam et justo duo dolores et ea rebum stet clita kasd
    gubergren no sea takimata sanctus est lorem ipsum dolor sit amet lorem ipsum
    dolor sit amet consetetur sadipscing elitr sed diam nonumy eirmod tempor
    invidunt ut labore et dolore magna aliquyam erat sed diam voluptua at vero
    eos et accusam et justo duo dolores et ea rebum stet clita kasd gubergren no
    sea takimata sanctus est lorem ipsum dolor sit amet lorem ipsum dolor sit
    amet consetetur sadipscing elitr at accusam aliquyam diam diam dolore
    dolores duo eirmod eos erat et nonumy sed tempor et et invidunt justo labore
    stet clita ea et gubergren kasd magna no rebum sanctus sea sed takimata ut
    vero voluptua est lorem ipsum dolor sit amet lorem ipsum dolor sit amet
    consetetur sadipscing elitr sed diam nonumy eirmod tempor invidunt ut labore
    et dolore magna aliquyam erat

    consetetur sadipscing elitr sed diam nonumy eirmod tempor invidunt ut labore
    et dolore magna aliquyam erat sed diam voluptua at vero eos et accusam et
    justo duo dolores et ea rebum stet clita kasd gubergren no sea takimata
    sanctus est lorem ipsum dolor sit amet lorem ipsum dolor sit amet consetetur
    sadipscing elitr sed diam nonumy eirmod tempor invidunt ut labore et dolore
    magna aliquyam erat sed diam voluptua at vero eos et accusam et justo duo
    dolores et ea rebum stet clita kasd gubergren no sea takimata sanctus est
    lorem ipsum dolor sit amet lorem ipsum dolor sit amet consetetur sadipscing
    elitr sed diam nonumy eirmod tempor invidunt ut labore et dolore magna
    aliquyam erat sed diam voluptua at vero eos et accusam et justo duo dolores
    et ea rebum stet clita kasd gubergren no sea takimata sanctus est lorem
    ipsum dolor sit amet"""

    # Done this way in case I decide to do words/paragraphs/sentences
    lorem_text = ipsum_text.replace('\n\n','\n')
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

def bind_function(field):
    """
    Return the appropriate (lambda) function for the given field
    """
    t = field['type']

    if t == 'int':
        return lambda: random.randint(field['min'], field['max'])
    elif t == 'float':
        return lambda: field['min'] + ((field['max'] - field['min']) * random.random())
    elif t == 'string':
        return lambda: ''.join(random.choice(string.letters) for i in xrange(random.randint(1, 15))).title()
    elif t == 'ipsum':
        return lambda: ipsum(field['lines'])
    elif t == 'choice':
        return lambda: random.choice(field['values'])
    elif t == 'bool':
        return lambda: bool(random.randint(0,1))
    elif t == 'name':
        return lambda: random.choice(names)
    elif t == 'date':
        return lambda: randdate(field)
    else:
        raise KeyError, "Unknown field type %s" % t



if __name__ == "__main__":
    opts, args = options()

    schema = json.load(open(opts.schema))
    function_schema = {}
    try:
        for field in schema:
            function_schema[field] = bind_function(schema[field])
    except KeyError, k:
        print k
        sys.exit(1)
    docs = []

    microcouch = MicroCouch(opts.url)
    for d in xrange(opts.number):
        docs.append(gen_doc(function_schema))
        if len(docs) > 500:
            microcouch.push(docs)
            docs = []
    microcouch.push(docs)

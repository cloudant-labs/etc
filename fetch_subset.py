#!/usr/bin/env python
"""
Retrieve a subset of a database and put it in another. Run via:
py scripts/fetch_subset.py -s http://localhost:5984/demo -d http://localhost:5984/demo2
"""
import json
import urllib
import urllib2
from optparse import OptionParser
from microcouch import MicroCouch

def do_options():
  parser = OptionParser()
  parser.set_usage('copy a subset from one CouchDB to another')
  parser.add_option("-s", "--source", dest="source", metavar="SOURCE",
                help="copy from SOURCE (URL to database root)")
  parser.add_option("-f", "--file", dest="file", metavar="JSONFILE",
                help="Read from JSONFILE (formatted like _all_docs?include_docs=true) instead of a remote couch")
  parser.add_option("-d", "--dest", dest="dest", metavar="DESTINATION",
                help="write into DESTINATION (URL to database root)")
  parser.add_option("-l", "--limit", dest="limit", metavar="N", default=100,
                help="copy N documents, default=100")
  parser.add_option("-o", "--offset", dest="offset", metavar="N", default=0,
                help="skip the first N documents, default=0")
  parser.add_option("-r", "--reverse", dest="descending", action="store_true",
                default=False, help="get the last N docs instead of the first N")
  return parser.parse_args()

def clean(d):
  d = d['doc']
  del d['_rev']
  return d

def get_docs(src, limit, offset, descending):
  """
  Get limit docs from src, skipping offset docs
  """
  values = {'limit': limit, 'skip': offset, 'include_docs': True, 'descending': descending}
  data = urllib.urlencode(values).lower()
  req = urllib2.Request('%s/_all_docs?%s' % (src, data))
  try:
    f = urllib2.urlopen(req)
    docs = json.loads(f.read())
    f.close()
  except Exception, e:
    print 'troubles contacting %s' % req.get_full_url()
    print e
  return map(clean, docs['rows'])


def copy_subset(src, dest, limit, offset, descending):
  """
  copy limit documents, skipping offset docs, from src to dest
  """
  i = 1
  for docs in chunks(get_docs(src, limit, offset, descending), 500):
    print "pushing batch %s" % i
    dest.push(docs)
    i += 1

def chunks(l, n):
  """
  Yield successive n-sized chunks from l.
  """
  for i in xrange(0, len(l), n):
    yield l[i:i+n]


if __name__ == "__main__":
  options, args = do_options()
  microcouch = MicroCouch(options.dest)

  if options.file:
    docs = json.load(open(options.file))
    for docs in chunks(map(clean, docs['rows'])):
      microcouch.push(docs)
  else:
    copy_subset(options.source, microcouch, options.limit, options.offset, options.descending)

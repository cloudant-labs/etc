import getpass
import base64
import json
import urllib
import urllib2
from urlparse import urlunparse, urlparse


class PutRequest(urllib2.Request):
    def get_method(self):
        return "PUT"

class PostRequest(urllib2.Request):
    def get_method(self):
        return "POST"

class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"

class MicroCouch:
    """
    An ugly class that provides minimal interactions with CouchDB
    """

    def __init__(self, database):
        parts = urlparse(database)

        self.auth = False
        self.created = False

        if parts.port:
            netloc = '%s:%s' % (parts.hostname, parts.port)
        else:
            netloc = parts.hostname

        url_tuple = (
                parts.scheme,
                netloc,
                parts.path,
                parts.params,
                parts.query,
                parts.fragment
                )
        self.url = urlunparse(url_tuple)
        self.do_auth(parts)
        self.create_db()

    def do_auth(self, parts):
        if parts.username and parts.password:
            auth_tuple = (parts.username, parts.password)
            self.auth = base64.encodestring('%s:%s' % auth_tuple).strip()
        elif parts.username:
            auth_tuple = (parts.username, getpass.getpass())
            self.auth = base64.encodestring('%s:%s' % auth_tuple).strip()

    def create_db(self):
        try:
            req = PutRequest(self.url)
            if self.auth:
                req.add_header("Authorization", "Basic %s" % self.auth)
            urllib2.urlopen(req)
            self.created = True
        except Exception, e:
            # The data base probably already exists
            print 'Database exists?', e
            pass

    def push(self, docs, update=True):
        """
        Push a list of docs to the database
        """

        if not self.created:
            # if the database didn't exist the docs won't either!
            def pull_id(doc):
                try:
                    return doc['_id']
                except:
                    pass
            # get id's out of the incoming docs
            in_ids = map(pull_id, docs)
            doc_dict = dict(zip(in_ids, docs))
            retrieved_ids = filter(None, map(pull_id, docs))
            if len(retrieved_ids):
                req = PostRequest('%s/_all_docs' % self.url)
                req.add_header("Content-Type", "application/json")
                req.add_data(json.dumps({'keys': retrieved_ids}))

                f = urllib2.urlopen(req)
                data = json.load(f)
                f.close()
                # Remove or update docs from the incoming list

                for row in data['rows']:
                    if "error" in row.keys() and row['error'] == 'not_found':
                        pass
                    else:
                        if update:
                            try:
                                doc_dict[row['id']]['_rev'] = row['value']['rev']
                            except:
                                print "Error:", row
                        else:
                            del doc_dict[row['id']]
                docs = doc_dict.values()

        response = {'error': 'no documents inserted'}
        if len(docs):
            req = urllib2.Request('%s/_bulk_docs' % self.url)
            req.add_header("Content-Type", "application/json")

            if self.auth:
                req.add_header("Authorization", "Basic %s" % self.auth)

            data = {'docs': docs}
            req.add_data(json.dumps(data))
            f = urllib2.urlopen(req)
            response = json.load(f)
            f.close()
        return response

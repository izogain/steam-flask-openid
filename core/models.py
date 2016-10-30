from google.appengine.ext import ndb

class User(ndb.Model):
  nickname = ndb.StringProperty()
  id_provider = ndb.StringProperty()
  email = ndb.StringProperty()
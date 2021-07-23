from google.appengine.ext import ndb
class MyUser(ndb.Model):
    # email address of this User
    emailaddress=ndb.StringProperty();

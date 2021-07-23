from google.appengine.ext import ndb
#EV Entity with all the required attributes
class EV(ndb.Model):
    name=ndb.StringProperty(indexed=True)
    manufacturer=ndb.StringProperty()
    year=ndb.IntegerProperty()
    battery_size=ndb.FloatProperty()
    cost=ndb.FloatProperty()
    power=ndb.FloatProperty()
    WLTP_Range=ndb.FloatProperty()
#EVReview entity to store the review, rating of the EV according to the id of the corresponding EV and rv_date for the date.
class EVReview(ndb.Model):
    ev_id=ndb.IntegerProperty()
    review=ndb.StringProperty()
    rating=ndb.IntegerProperty()
    rv_date = ndb.DateTimeProperty(auto_now_add=True)

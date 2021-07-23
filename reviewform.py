import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from ev import EV
from ev import EVReview
import datetime
JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)
class ReviewForm(webapp2.RequestHandler):
    #to render EVReview and user object to reviewform.html
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user=users.get_current_user()
        key = ndb.Key('EVReview', 'default')
        ev_r = key.get()
        if ev_r == None:
            ev_r = EVReview(id='default')
        template_values = {
        'ev_r':ev_r,
        'user':user
        }
        template = JINJA_ENVIRONMENT.get_template('reviewform.html')
        self.response.write(template.render(template_values))
#gets the EV reviews and ratings, and stores them in the EVReview Datastore
    def post(self):
        action = self.request.get('button')
        user=users.get_current_user()
        id = self.request.get('id')
        ev_key=ndb.Key('EV',int(self.request.get('id')))
        ev=ev_key.get()
        ev_r=EVReview()
        if action == 'Submit Review':
            ev_r.ev_id=int(id)
            ev_r.review = self.request.get('ev_review')
            ev_r.rating=int(self.request.get('ev_rating'))
            ev_r.rv_date =  datetime.datetime.now()
            ev_r.put()
            self.redirect('/list')
        elif action == 'Cancel':
            template_values = {
                    'id':id,
                    'ev':ev,
                    'evkey':ev_key,
                    'user':user

            }
            template = JINJA_ENVIRONMENT.get_template('evinfo.html')
            self.response.write(template.render(template_values))

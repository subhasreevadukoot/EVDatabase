import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from ev import EV
from ev import EVReview
JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)
class List(webapp2.RequestHandler):

    def get(self):
        evs,cursor,more = EV.query().fetch_page(80)
        user=users.get_current_user()
        # gets the id from the dynamically generated hyperlink.
        id = self.request.get('id')
        rating_list=[]
        sum=0
        avg=0
        if id:
            ev_key=ndb.Key('EV',int(self.request.get('id')))
            ev=ev_key.get()
            # to display reviews in reverse chronological orders, order() function is used.
            query=EVReview.query(EVReview.ev_id==int(id)).order(-EVReview.rv_date).fetch()
            for i in query:
                sum=sum+i.rating
            if(len(query)!=0):
                avg=float(sum)/len(query)
                avg=round(avg,3)
            #calculates the average rating, one variable is converted to float to allow float value as result.
            template_values = {
                    'id':id,
                    'ev':ev,
                    'evkey':ev_key,
                    'user':user,
                    'avg':avg,
                    'query':query
            }
            template = JINJA_ENVIRONMENT.get_template('evinfo.html')
            self.response.write(template.render(template_values))
        else:
            template_values = {
                'evs' : evs,
                'user':user
            }
            template = JINJA_ENVIRONMENT.get_template('list.html')
            self.response.write(template.render(template_values))
    def post(self):
        user=users.get_current_user()
        action = self.request.get('button')
        id = self.request.get('id')
        if id:
            ev_key=ndb.Key('EV',int(self.request.get('id')))
            ev=ev_key.get()
            if action == 'Edit':
                template_values = {
                    'ev' : ev,
                    'user':user
                }
                template = JINJA_ENVIRONMENT.get_template('edit.html')
                self.response.write(template.render(template_values))
            elif action == 'Back':
                self.redirect('/list')
                #delete functionality
            elif action == 'Delete':
                ev.key.delete()
                evs,cursor,more = EV.query().fetch_page(80)
#to render ev list after the deletion
                template_values = {
                    'evs' : evs,
                    'user':user
                }
                template = JINJA_ENVIRONMENT.get_template('list.html')
                self.response.write(template.render(template_values))
            elif action=='Review' :
                template_values = {
                    'ev' : ev,
                    'user':user
                }
                template = JINJA_ENVIRONMENT.get_template('reviewform.html')
                self.response.write(template.render(template_values))

class Edit(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        myuser=None
        user=users.get_current_user()
        id = self.request.get('id')
        ev_key=ndb.Key('EV',int(self.request.get('id')))
        ev=ev_key.get()
        template_values = {
            'ev' : ev,
            'user':user
        }
        template = JINJA_ENVIRONMENT.get_template('edit.html')
        self.response.write(template.render(template_values))

    def post(self):
        action = self.request.get('button')
        user=users.get_current_user()
        error=None
        condition=None
        id = self.request.get('id')
        ev_key=ndb.Key('EV',int(self.request.get('id')))
        ev=ev_key.get()
        oldname=ev.name
        oldmanufacturer=ev.manufacturer
        oldyear=ev.year
        total_query=None
        #updates the database after retrieving form values
        if action == 'Update':
            ev.name = self.request.get('ev_name')
            Ename=self.request.get('ev_name')
            ev.manufacturer = self.request.get('ev_manufacturer')
            Emanufacturer=self.request.get('ev_manufacturer')
            ev.battery_size=float(self.request.get('ev_battery_size'))
            ev.year=int(self.request.get('ev_year'))
            Eyear=int(self.request.get('ev_year'))
            ev.cost=float(self.request.get('ev_cost'))
            ev.power=float(self.request.get('ev_power'))
            ev.WLTP_Range=float(self.request.get('ev_WLTP_Range'))
            if(not(oldname==Ename and oldmanufacturer==Emanufacturer and oldyear==Eyear)):
                query= EV.query(EV.name == Ename).fetch(keys_only=True)
                query1=EV.query(EV.manufacturer==Emanufacturer ).fetch(keys_only=True)
                query2=EV.query(EV.year==Eyear).fetch(keys_only=True)
                total_query = ndb.get_multi(set(query1).intersection(query2).intersection(query))
            #values will be updated only if there is no another EV with the same name, manufacturer and EV. if it is there, an error message will be displayed
                if len(total_query) == 0:
                    ev.put()
                    message="Successfully updated ! "
                    condition=False
                else:
                    message="Sorry, the ev information you provided is already existing.!"
                    condition=True
            else:
                ev.put()
                message="Successfully updated ! "
            template_values = {
            'message':message,
            'user':user,
            'condition':condition
            }
            template = JINJA_ENVIRONMENT.get_template('edit.html')
            self.response.write(template.render(template_values))
        elif action == 'Cancel':
            self.redirect('/list')

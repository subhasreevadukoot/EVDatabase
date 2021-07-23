import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from ev import EV

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)
class Add(webapp2.RequestHandler):
    #creates default ids, and passes the status of the user to the add.html page
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user=users.get_current_user()
        key = ndb.Key('EV', 'default')
        ev = key.get()
        if ev == None:
            ev = EV(id='default')
        template_values = {
        'ev':ev,
        'user':user
        }
        template = JINJA_ENVIRONMENT.get_template('add.html')
        self.response.write(template.render(template_values))

#takes the ev information values from the form fields and puts them in the EV datastore object only if the condition that ev with same name , manufacturer, year cannot be added is met
    def post(self):
        action = self.request.get('button')
        ev = EV()
        user=users.get_current_user()
        if action == 'Add':
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
            query= EV.query(EV.name ==Ename).fetch(keys_only=True)
            query1=EV.query(EV.manufacturer==Emanufacturer ).fetch(keys_only=True)
            query2=EV.query(EV.year==Eyear).fetch(keys_only=True)
            #intersection is used because we cannot add ev that have all three of year, manufacturer, name same
            total_query = ndb.get_multi(set(query1).intersection(query2).intersection(query))
            #values will be added only if there is no another EV with the same name, manufacturer and EV. if it is there, an error message will be displayed
            if len(total_query) == 0:
                ev.put()
                message="Successfully added ! "
            else:
                message="Sorry, you cannot add a duplicate ev"
            template_values = {
            'message':message,
            'user':user
            }
            template = JINJA_ENVIRONMENT.get_template('add.html')
            self.response.write(template.render(template_values))
        elif action == 'Cancel':
            self.redirect('/')

from __future__ import print_function
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
class Search(webapp2.RequestHandler):
#Handles HTTP get request
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user=users.get_current_user()
        action = self.request.get('button')
        filtered_data={}
        total_query=EV.query().fetch()
        tmpQuery = []
        resultList = []
        no_data = None
        query=EV.query()
        evs,cursor,more=query.fetch_page(80)

        
#First,  search if these inputs fields are filled, if yes they are appended to a query list.
        checked = False
        if action == 'Search':
            name = self.request.get('ev_name')
            if name :
                tmpQuery.append(EV.query(EV.name==name).fetch(keys_only=True))

            manufacturer = self.request.get('ev_manufacturer')
            if manufacturer :
                tmpQuery.append(EV.query(EV.manufacturer==manufacturer).fetch(keys_only=True))
                #total_query = total_query.filter(EV.manufacturer==manufacturer)

            if not self.request.get('ev_yearf')=="" and not self.request.get('ev_yeart')=="" :
                yearf=int(self.request.get('ev_yearf'))
                yeart=int(self.request.get('ev_yeart'))
                tmpQuery.append(EV.query(EV.year >= yearf,EV.year <= yeart).fetch(keys_only=True))

            if not self.request.get('ev_battery_sizef')=="" and not self.request.get('ev_battery_sizet')=="" :
                battery_sizef=float(self.request.get('ev_battery_sizef'))
                battery_sizet=float(self.request.get('ev_battery_sizet'))
                tmpQuery.append(EV.query(EV.battery_size >= battery_sizef,EV.battery_size <= battery_sizet).fetch(keys_only=True))

            if not self.request.get('ev_costf')=="" and not self.request.get('ev_costt') =="" :
                costf=float(self.request.get('ev_costf'))
                costt=float(self.request.get('ev_costt'))
                tmpQuery.append(EV.query(EV.cost >= costf,EV.cost <= costt).fetch(keys_only=True))

            if not self.request.get('ev_powerf')=="" and not self.request.get('ev_powert') =="" :
                powerf=float(self.request.get('ev_powerf'))
                powert=float(self.request.get('ev_powert'))
                tmpQuery.append(EV.query(EV.power >= powerf,EV.power <= powert).fetch(keys_only=True))

            if not self.request.get('ev_WLTP_Rangef')=="" and not self.request.get('ev_WLTP_Ranget') =="" :
                WLTP_Rangef=float(self.request.get('ev_WLTP_Rangef'))
                WLTP_Ranget=float(self.request.get('ev_WLTP_Ranget'))
                tmpQuery.append(EV.query(EV.WLTP_Range >= WLTP_Rangef,EV.WLTP_Range <= WLTP_Ranget).fetch(keys_only=True))


            no_data = "No Result Found"

            length = len(tmpQuery)
#length of the query is checked to see if there is more than one query in the query list.
            for i in range(length):
                 if i==0 :
                     total_query = ndb.get_multi(set(tmpQuery[i]))
                # if query length is not 0, intersection of the queries in the queries list is taken using the loop counter variable i.
                 else :
                     total_query = ndb.get_multi(set(tmpQuery[i-1]).intersection(tmpQuery[i]))


        elif action == "Cancel":
            self.redirect('/')
            #values to be rendered to the search webpage. This includes, the query list, user status, no data message and ev list.
        template_values = {
                'total_query': total_query ,
                'mainList': tmpQuery ,
                'action':action,
                'user':user,
                'no_data':no_data,
                'evs':evs
            }
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

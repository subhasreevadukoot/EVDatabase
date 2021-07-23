import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from ev import EV,EVReview
import array as arr
JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)
class Compare(webapp2.RequestHandler):
#renders ev list to compare page where they will be displayed as checkboxes.
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        query=EV.query()
        user=users.get_current_user()
        evs,cursor,more=query.fetch_page(80)
        template_values = {
            'evs':evs,
            'user':user
        }
        template = JINJA_ENVIRONMENT.get_template('compare.html')
        self.response.write(template.render(template_values))

    def post(self):
        user=users.get_current_user()
        error_message=None
        comparecondition=False
        action=self.request.get('button')
        #the list of evs to compare obtained from checkbox
        evs=self.request.params.getall('comparenames')
        evc=[]
        ev_r_list=[]
        list={}
        battery_dict={}
        cost_dict={}
        power_dict={}
        WLTP_dict={}
        score=[]
        avg=0
        list2=[]
        list3=[]
        list4=[]
        list5=[]
        list6=[]
        if action == 'Compare':
            if len(evs)<2:
                comparecondition=False
            else:
                comparecondition=True
            for e in evs:
                evkey = ndb.Key('EV', int(e))
                ev_obj=evkey.get()
                evc.append(ev_obj)
                # to display reviews in reverse chronological orders, order() function is used.
                query=EVReview.query(EVReview.ev_id==evkey.id()).order(-EVReview.rv_date).fetch()
                sum=0
                for i in query:
                    ev_r_list.append(i)
                    sum=sum+i.rating
                if(len(query)!=0):
                    avg=float(sum)/len(query)  #calculates the average rating, one variable is converted to float to allow float value as result.
                    avg=round(avg,3)
                for ev in evc:
                    list2.append(ev.battery_size)
                    list3.append(ev.cost)
                    list4.append(ev.power)
                    list5.append(ev.WLTP_Range)
                    list6.append(ev.year)

                list[int(e)]=avg
            list1=list.values()
            #maximum and minimum  of all attributes rendered to compare-result page
            max_rating=max(list1)
            min_rating=min(list1)

            max_battery=max(list2)
            min_battery=min(list2)

            max_cost=max(list3)
            min_cost=min(list3)

            max_power=max(list4)
            min_power=min(list4)

            max_WLTP=max(list5)
            min_WLTP=min(list5)

            max_year=max(list6)
            min_year=min(list6)

            template_values = {
                    'user':user,
                    'evc':evc,
                    'error_message':error_message,
                    'comparecondition':comparecondition,
                    'evs':evs,
                    'ev_r_list':ev_r_list,
                    'list':list,
                    'max_rating':max_rating,
                    'min_rating':min_rating,
                    'max_battery':max_battery,
                    'min_battery':min_battery,
                    'max_cost':max_cost,
                    'min_cost':min_cost,
                    'max_WLTP':max_WLTP,
                    'min_WLTP':min_WLTP,
                    'max_power':max_power,
                    'min_power':min_power,
                    'max_year':max_year,
                    'min_year':min_year
                    }
            template = JINJA_ENVIRONMENT.get_template('compare-result.html')
            self.response.write(template.render(template_values))
        elif action == "Cancel":
            self.redirect('/')

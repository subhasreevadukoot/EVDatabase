import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
from myuser import MyUser
from add import Add
from list import List
from list import Edit
from compare import Compare
from search import Search
from reviewform import ReviewForm
import os

#setting up the environment for Jinja to work in as this construct a jinja2.Environment object. The loader line tells Jinja where to find all of the templates that will be used by this request handler.
# By specifying os.path.dirname( __file__ ) this is asking Jinja to use the same directory as the currentfile that is being edited
JINJA_ENVIRONMENT=jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)
class MainPage(webapp2.RequestHandler):
    #get function renders url and url string values for login-logout service to the main.html(homepage)
    #Google App Engine's  login-logout service is used.

    #This method will respond to the GET HTTP verb and will be responsible
#for rendering the result of a GET request to this class
    def get(self):
        self.response.headers['Content-type']='text/html'
        url=''
        url_string=''
        welcome='Welcome back'
        myuser=None
        user=users.get_current_user()
        if user:
            url=users.create_logout_url(self.request.uri)
            url_string='Logout'
            myuser_key=ndb.Key('MyUser',user.user_id())
            myuser=myuser_key.get()
            if myuser == None:
                welcome= 'Welcome to the application'
                myuser= MyUser(id=user.user_id())
                myuser.put()
        else:
            url= users.create_login_url(self.request.uri)
            url_string= 'Login'
        template_values= {
        'url': url,
        'url_string': url_string,
        'user': user,
        'welcome': welcome
        }
        template= JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

# starts the web application we specify the full routing table
# A routing table is provided using the python list and tuple that states that any requests to the root of the application at '/' should call the appropriate
#methods of an instance of the MainPage class.

app = webapp2.WSGIApplication([
    ('/',MainPage),
    ('/add',Add),
    ('/evinfo',List),
    ('/edit',Edit),
    ('/list',List),
    ('/compare',Compare),
    ('/search',Search),
    ('/compare-result',Compare),
    ('/reviewform',ReviewForm),
     ],debug=True)

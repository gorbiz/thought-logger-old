import cgi
import datetime
import urllib
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import uuid
from urlparse import urlparse

class Log(db.Model):
  """Models an individual Log entry with an author, content, and date."""
  # TODO Remove author
  author = db.UserProperty()
  read_key = db.StringProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)

class Book(db.Model):
  """Models a user/account/book with email, read key, write key and date."""
  author = db.UserProperty()
  read_key = db.StringProperty()
  write_key = db.StringProperty()
  updated = db.DateTimeProperty(auto_now_add=True)
  

def logbook_key(logbook_name=None):
  """Constructs a datastore key for a Log entity with logbook_name."""
  return db.Key.from_path('Log', logbook_name or 'default_log')

class MainPage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()

    if user:
      self.response.headers['Content-Type'] = 'text/plain'
      self.response.out.write('Hello, ' + user.nickname())

      # TODO Get Book by user_id or email
      # else:

      book = Book()
      book.author = users.get_current_user()
      book.read_key = str(uuid.uuid4())
      book.write_key = str(uuid.uuid4())
      book.put()

    else:
      self.redirect(users.create_login_url(self.request.uri))

    application = webapp.WSGIApplication([('/', MainPage)], debug=True)
    
    # TODO Make this uuid attach to the google account instead...
    #self.response.out.write('<html><header><title>Though logger links</title></header><body>')
    #logbook_name=uuid.uuid4()
    #self.response.out.write('<p>Put this under "Where to pass entries" in your Thought logger: <div>http://thought-logger.appspot.com/%s/log</div></p>' % logbook_name)
    #self.response.out.write('<p>Here is the RSS stream where your entries are stored: <div>http://thought-logger.appspot.com/%s/get</div></p>' % logbook_name)
    #self.response.out.write('</body></html>')

class Logbook(webapp.RequestHandler):
  def post(self):
    # We set the same parent key on the 'Log' to ensure each log is in
    # the same entity group. Queries across the single entity group will be
    # consistent. However, the write rate to a single entity group should
    # be limited to ~1/second.

    self.response.headers['Access-Control-Allow-Origin'] = '*'

    logbook_name = urlparse(self.request.url).path.split('/')[1]
    log = Log(parent=logbook_key(logbook_name))

    if users.get_current_user():
      log.author = users.get_current_user()

    log.content = self.request.get('content')
    log.put()

class GetRss(webapp.RequestHandler):
  def get(self):
    logbook_name = urlparse(self.request.url).path.split('/')[1]
    self.response.headers['Content-Type'] = 'text/xml' 
    self.response.out.write('<rss version="2.0"><channel>')
    self.response.out.write('<title>Thought log</title>')
    self.response.out.write('<description>This is a personal thought log</description>""")')
    self.response.out.write('<link>http://thought-logger.appspot.com/' + logbook_name + '/get</link>')
    self.response.out.write('<lastBuildDate>%s GMT</lastBuildDate>' % datetime.datetime.now())
    self.response.out.write('<pubDate>%s GMT</pubDate>' % datetime.datetime.now())

    # Ancestor Queries, as shown here, are strongly consistent with the High
    # Replication datastore. Queries that span entity groups are eventually
    # consistent. If we omitted the ancestor from this query there would be a
    # slight chance that Log that had just been written would not show up
    # in a query.
    logs = db.GqlQuery("SELECT * "
                            "FROM Log "
                            "WHERE ANCESTOR IS :1 "
                            "ORDER BY date DESC LIMIT 10",
                            logbook_key(logbook_name))

    for log in logs:
      self.response.out.write('<item>')
      self.response.out.write('<title>%s</title>' % cgi.escape(log.content))
      self.response.out.write('<description>%s</description>' % cgi.escape(log.content))
      self.response.out.write('<link>http://www.example.com/</link>')
      self.response.out.write('<pubDate>%s GMT</pubDate>' % log.date)
      self.response.out.write('</item>')

    self.response.out.write('</channel></rss>')
    
class Test(webapp.RequestHandler):
  def get(self):
    logbook_name = urlparse(self.request.url).path.split('/')[1]
    self.response.out.write(logbook_name)
    self.response.out.write(uuid.uuid4())

application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/[^/]+/log', Logbook),
  ('/[^/]+/get', GetRss),
  ('/[^/]+/test', Test)
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()

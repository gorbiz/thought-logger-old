import cgi
import datetime
import urllib
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from urlparse import urlparse
import uuid

class Log(db.Model):
  """Models an individual Log entry with an author, content, and date."""
  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)


def logbook_key(logbook_name=None):
  """Constructs a datastore key for a Log entity with logbook_name."""
  return db.Key.from_path('Log', logbook_name or 'default_log')


class MainPage(webapp.RequestHandler):
  def get(self):
    # TODO Make this uuid attach to the google account instead...
    self.response.out.write('<html><header><title>Though logger links</title></header><body>')
    logbook_name=uuid.uuid4()
    self.response.out.write('<p>Put this under "Where to pass entries" in your Thought logger: <div>http://thought-logger.appspot.com/%s/log</div></p>' % logbook_name)
    self.response.out.write('<p>Here is the RSS stream where your entries are stored: <div>http://thought-logger.appspot.com/%s/get</div></p>' % logbook_name)
    self.response.out.write('</body></html>')

#    logbook_name=self.request.get('logbook_name')

    # Ancestor Queries, as shown here, are strongly consistent with the High
    # Replication datastore. Queries that span entity groups are eventually
    # consistent. If we omitted the ancestor from this query there would be a
    # slight chance that Log that had just been written would not show up
    # in a query.
"""    logs = db.GqlQuery("SELECT * "
                            "FROM Log "
                            "WHERE ANCESTOR IS :1 "
                            "ORDER BY date DESC LIMIT 10",
                            logbook_key(logbook_name))

    for log in logs:
      if log.author:
        self.response.out.write(
            '<b>%s</b> wrote:' % log.author.nickname())
      else:
        self.response.out.write('An anonymous person wrote:')
      self.response.out.write('<blockquote>%s</blockquote>' %
                              cgi.escape(log.content))
"""

#    self.response.out.write("""
#          <form action="/log?%s" method="post">
#            <div><textarea name="content" rows="3" cols="60"></textarea></div>
#            <div><input type="submit" value="Log"></div>
#          </form>
#          <hr>
#          <form>Logbook name: <input value="%s" name="logbook_name">
#          <input type="submit" value="switch"></form>
#        </body>
#      </html>""" % (urllib.urlencode({'logbook_name': logbook_name}),
#                          cgi.escape(logbook_name)))


class Logbook(webapp.RequestHandler):
  def post(self):
    # We set the same parent key on the 'Log' to ensure each log is in
    # the same entity group. Queries across the single entity group will be
    # consistent. However, the write rate to a single entity group should
    # be limited to ~1/second.
    logbook_name = urlparse(self.request.url).path.split('/')[1]
    log = Log(parent=logbook_key(logbook_name))

    if users.get_current_user():
      log.author = users.get_current_user()

    log.content = self.request.get('content')
    log.put()
    self.redirect('/?' + urllib.urlencode({'logbook_name': logbook_name}))

class GetRss(webapp.RequestHandler):
  def get(self):
    logbook_name = urlparse(self.request.url).path.split('/')[1]
    self.response.headers['Content-Type'] = 'text/xml' 
    self.response.out.write("""<rss version="2.0">
	<channel>
		<title>Thought log</title>
		<description>This is a personal thought log</description>""")
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

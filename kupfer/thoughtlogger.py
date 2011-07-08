__kupfer_name__ = _("Thought logger")
__kupfer_actions__ = ("Log", )
__description__ = _("Makes it easy to write down thoughts without interrupting")
__version__ = "0.1"
__author__ = "Karl Svartholm <gorbiz@gmail.com>"

import httplib, urllib
from urlparse import urlparse
from kupfer.objects import Action, TextLeaf
from kupfer import kupferstring
from kupfer import plugin_support

__kupfer_settings__ = plugin_support.PluginSettings(
	{
		"key" : "receiver_url",
		"label": _("Where to pass entries"),
		"type": str,
		"value": "http://localhost/thought-logger/log/",
	},
)
# TODO Optional potential setting: "Source", could be for example "My laptop", "My desktop"

class Log (Action):
	def __init__(self, name=None):
		if not name:
			name = _("Log")
		Action.__init__(self, name)

	def activate(self, leaf):
		leaf_text = kupferstring.tolocale(leaf.object)

		url = (__kupfer_settings__["receiver_url"])
		o = urlparse(url)
		host = o.netloc
		path = o.path

		# XXX This will fail with HTTPS, right?
		params = urllib.urlencode({'content': leaf_text})
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		conn = httplib.HTTPConnection(host)
		conn.request("POST", path, params, headers)
		response = conn.getresponse()

		data = response.read()
		conn.close()

	def item_types(self):
		yield TextLeaf

	def get_icon_name(self):
		return "list-add"





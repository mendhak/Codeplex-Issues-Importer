#! /usr/bin/python

import urllib2
import HTMLParser
import re

class MyParser(HTMLParser.HTMLParser):
	foundWorkItem = False
	foundHTwo = False

	def __init__(self, url):
		HTMLParser.HTMLParser.__init__(self)
		request = urllib2.urlopen(url)
		self.feed(request.read())



	def handle_starttag(self, tag, attrs):
		if tag == "a" and len(attrs) > 0 and attrs[0][0] == "href":
			href = attrs[0][1]
			if re.match("(.)*/workitem/[0-9]+", href):
				print href

	def handle_data(self, data):
		pass

theUrl = "http://gpslogger.codeplex.com/workitem/list/basic?size=2147483647"
print "Querying", theUrl
MyParser(theUrl)
			


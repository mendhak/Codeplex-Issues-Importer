#! /usr/bin/python

import urllib2
import HTMLParser

class MyParser(HTMLParser.HTMLParser):
	foundWorkItem = False
	foundHTwo = False

	def __init__(self, url):
		HTMLParser.HTMLParser.__init__(self)
		request = urllib2.urlopen(url)
		self.feed(request.read())



	def handle_starttag(self, tag, attrs):
		if tag == 'div':
			if len(attrs) > 0 and attrs[0][1] == 'workItemSummary':
				self.foundWorkItem = True
		if self.foundWorkItem and tag == 'h2':
			self.foundHTwo = True

	def handle_data(self, data):
		if self.foundHTwo == True:
			print data
			self.foundHTwo = False;

theUrl = "http://gpslogger.codeplex.com/workitem/list/basic?field=CreationDate&direction=Descending&issuesToDisplay=Open&keywords=&emailSubscribedItemsOnly=false"
print theUrl
MyParser(theUrl)
			


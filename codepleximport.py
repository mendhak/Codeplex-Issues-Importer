#! /usr/bin/python

import urllib2
import HTMLParser
import re

def getTupleValue(lst, key):
	for k, v in lst:
		if k == key:
			return v


class CodePlexWorkItem():
	heading = ""
	description = ""
	comments = []
	submittedby = ""

	def __init__(self):
		pass
	
	def SetHeading(self, h):
		self.heading = h
	
	def SetDescription(self, d):
		self.description = d

	def AppendDescription(self, d):
		self.description = self.description + d
	
	def SetSubmittedBy(self, s):
		self.submittedby =  s

	def AddComment(self, c):
		self.comments.append(c)


class IssuesListParser(HTMLParser.HTMLParser):

	itemLinks = []

	def __init__(self, url):
		HTMLParser.HTMLParser.__init__(self)
		request = urllib2.urlopen(url)
		self.feed(request.read())



	def handle_starttag(self, tag, attrs):
		if tag == "a" and len(attrs) > 0:
			href = getTupleValue(attrs, "href")

			if re.match("(.)*/workitem/[0-9]+", href):
				self.itemLinks.append(href)

	def handle_data(self, data):
		pass


class WorkItemParser(HTMLParser.HTMLParser):
	titleFound = False
	descriptionFound = False

	commentByFound = False
	commentFound = False
	comment = ""
	
	submittedByFound = False

	wi = CodePlexWorkItem()

	def __init__(self, url):
		HTMLParser.HTMLParser.__init__(self)
		request = urllib2.urlopen(url)
		self.feed(request.read())

	def handle_starttag(self, tag, attrs):

		if tag == "span" and len(attrs) > 0: 
			spanId = getTupleValue(attrs, "id")
			if spanId == "TitleLabel":
				self.titleFound = True
		if tag == "div" and len(attrs) > 0:
			divId = getTupleValue(attrs, "id")
			if divId == "DescriptionPanel":
				self.descriptionFound = True
			elif divId != None and "MessageLabel" in divId:
				self.commentFound = True

		if tag == "a" and len(attrs) > 0:
			aId = getTupleValue(attrs, "id")
			if aId != None and "PostedByLink" in aId:
				self.commentByFound = True
			if aId == "ReportedByLink":
				self.submittedByFound = True


	def handle_data(self, data):
		if self.titleFound:
			self.wi.SetHeading(data)
		if self.descriptionFound:
			self.wi.AppendDescription(data)
		if self.commentByFound:
			self.comment = self.comment + data
		if self.commentFound:
			self.comment = self.comment + data
		if self.submittedByFound:
			self.wi.SetSubmittedBy(data)

	def handle_endtag(self, tag):
		if self.titleFound and tag == "span":
			self.titleFound = False
		if self.descriptionFound and tag == "div":
			self.descriptionFound = False
		if self.commentByFound and tag == "a":
			self.commentByFound = False
		if self.commentFound and tag == "div":
			self.commentFound = False
			self.wi.AddComment(self.comment)
			self.comment = ''
		if self.submittedByFound:
			self.submittedByFound = False

	def handle_entityref(self, name):
		if self.descriptionFound:
			self.wi.AppendDescription(name)
		if self.commentFound:
			self.comment = self.comment + data

	def handle_charref(self, name):
		if self.descriptionFound:
			self.wi.AppendDescription("&#" + name)
		if self.commentFound:
			self.comment = self.comment + "&#" + name


theUrl = "http://gpslogger.codeplex.com/workitem/list/basic?size=2147483647"
print "Querying", theUrl

#Extract links from the main issues page
#ilp = IssuesListParser(theUrl)


#Loop through, process each work item link
#for itemUrl in ilp.itemLinks:
#	WorkItemParser(itemUrl)
workItem = CodePlexWorkItem()
wip = WorkItemParser("http://gpslogger.codeplex.com/workitem/7465")
print wip.wi.submittedby
			


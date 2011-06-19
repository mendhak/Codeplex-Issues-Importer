#! /usr/bin/python


#Download the github2 package from http://packages.python.org/github2/

#User specific values
CODEPLEX_PROJECT = "gpslogger.codeplex.com"
GITHUB_PROJECT = "Codeplex-Issues-Importer" 
GITHUB_USERNAME = "mendhak"
GITHUB_ISSUELABEL = "CodePlex"
GITHUB_APITOKEN = ""

if GITHUB_APITOKEN == "":
	raise Exception("You haven't supplied an API Token in this file")


import urllib2
import HTMLParser
import re

try:
	from github2.client import Github
except ImportError, e:
	print "You haven't installed the github2 package"
	exit()




def getTupleValue(lst, key):
	"""From a given list of tuples, searches for the key and returns its corresponding value
		List should be of the form [(a,b),(c,d),(e,f)]"""
	for k, v in lst:
		if k == key:
			return v


class CodePlexWorkItem():
	"""Class to represent a single workitem on codeplex"""
	heading = ""
	description = ""
	comments = []
	submittedby = ""
	isClosed = False

	def __init__(self):
			self.comments = []
	
	def AppendHeading(self, h):
		self.heading = self.heading + h
	
	def SetDescription(self, d):
		self.description = d

	def AppendDescription(self, d):
		self.description = self.description + d
	
	def SetSubmittedBy(self, s):
		self.submittedby =  s

	def AddComment(self, c):
		self.comments.insert(0,c)
		
	def SetIsClosed(self, c):
		self.isClosed = c


class IssuesListParser(HTMLParser.HTMLParser):
	"""Uses HTMLParser to parse the /workitem/list/basic page for workitem links to follow"""
	itemLinks = []

	def __init__(self, url):
		"""Begins the parsing on the given URL"""
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
	"""Class to handle parsing a /workitem/XXXX page for information"""
	titleFound = False
	descriptionFound = False

	commentByFound = False
	commentFound = False
	comment = ""
	
	submittedByFound = False
	
	itemStatusFound = False

	currentWorkItem = None

	def __init__(self, url):
		"""Begins the parsing process"""
		HTMLParser.HTMLParser.__init__(self)
		request = urllib2.urlopen(url)
		self.currentWorkItem = CodePlexWorkItem()
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
			elif divId != None and "VotedLabel" in divId:
				self.itemStatusFound = True

		if tag == "a" and len(attrs) > 0:
			aId = getTupleValue(attrs, "id")
			if aId != None and "PostedByLink" in aId:
				self.commentByFound = True
			if aId == "ReportedByLink":
				self.submittedByFound = True


	def handle_data(self, data):
		if self.titleFound:
			self.currentWorkItem.AppendHeading(data)
		if self.descriptionFound:
			self.currentWorkItem.AppendDescription(data)
		if self.commentByFound:
			self.comment = self.comment + "<b>" + data + "[CodePlex]</b>"
		if self.commentFound:
			self.comment = self.comment + data
		if self.submittedByFound:
			self.currentWorkItem.SetSubmittedBy(data)
		if self.itemStatusFound:
			if data == "closed":
				self.currentWorkItem.SetIsClosed(True)
			

	def handle_endtag(self, tag):
		if self.titleFound and tag == "span":
			self.titleFound = False
		if self.descriptionFound and tag == "div":
			self.descriptionFound = False
		if self.commentByFound and tag == "a":
			self.commentByFound = False
		if self.commentFound and tag == "div":
			self.commentFound = False
			self.currentWorkItem.AddComment(self.comment)
			self.comment = ''
		if self.submittedByFound:
			self.submittedByFound = False

	def handle_entityref(self, name):
		if self.descriptionFound:
			self.currentWorkItem.AppendDescription(name)
		if self.commentFound:
			self.comment = self.comment + data
		if self.titleFound:
			self.currentWorkItem.AppendHeading(name)
			

	def handle_charref(self, name):
		if self.descriptionFound:
			self.currentWorkItem.AppendDescription("&#" + name + ";")
		if self.commentFound:
			self.comment = self.comment + self.unescape("&#" + name + ";")
		if self.titleFound:
			self.currentWorkItem.AppendHeading(self.unescape("&#" + name + ";"))
			
	def handle_startendtag(self, tag, attrs):
		"""For self closing tags such as <img /> or <br />"""
		if tag == "br":
			if self.descriptionFound:
				self.currentWorkItem.AppendDescription("<br />")
			if self.commentFound:
				self.comment = self.comment + " <br />"
		


issuesUrlFormat = "http://" + CODEPLEX_PROJECT + "/workitem/list/basic?field=CreationDate&direction=Ascending&issuesToDisplay=All&keywords=&emailSubscribedItemsOnly=false&size=100&page={pn}"

continuePaging = True
pageNumber = -1
totalLinks = 0

#Extract links from the main issues page
while continuePaging:
	pageNumber += 1
	issuePageUrl = issuesUrlFormat.format(pn=str(pageNumber)) 
	print "Parsing page ", pageNumber, "(", issuePageUrl, ")"

	ilp = IssuesListParser(issuePageUrl)

	if len(ilp.itemLinks) == totalLinks:
		continuePaging = False
		print "Reached end of issue pages"
	else:
		totalLinks = len(ilp.itemLinks)
		continuePaging = True

print len(ilp.itemLinks), " work item links found"

parsedWorkItems = []

#Loop through, process each work item link
for itemUrl in ilp.itemLinks:
	wiParser = WorkItemParser(itemUrl)
	print wiParser.currentWorkItem.heading
	parsedWorkItems.append(wiParser.currentWorkItem)
	
print len(parsedWorkItems), " work items parsed from CodePlex"

#initialize github
gh = Github(username=GITHUB_USERNAME, api_token=GITHUB_APITOKEN,requests_per_second=0.5)

for wi in parsedWorkItems:
	newIssue = gh.issues.open(GITHUB_USERNAME + "/" + GITHUB_PROJECT, title=wi.heading, body=wi.description)
	gh.issues.add_label(GITHUB_USERNAME + "/" + GITHUB_PROJECT, newIssue.number, GITHUB_ISSUELABEL)
	for c in wi.comments:
		gh.issues.comment(GITHUB_USERNAME + "/" + GITHUB_PROJECT, newIssue.number, c)
	if wi.isClosed:
		gh.issues.close(GITHUB_USERNAME + "/" + GITHUB_PROJECT, newIssue.number)
	print "Created Github issue", newIssue.number, "for", "[" + wi.heading + "]"
	
print "End of script"



# STANDARD LIBRARIES
import os, sys, time, datetime
# from commons import sleep
from jira import JIRA
import getopt

# from MasterConfig import *
import csv

jiraserver = 'https://devsecopscollab.atlassian.net'
jiraun = 'devsecopscollab@gmail.com'
jirapwd = 'L1l2l3l4l5!'

reportfilename = sys.argv[1]

# reportfilename = reportfilename.encode('string-escape')

print ("value of report file name is: " + reportfilename)

def jirabuglogging(_reportfilename):
	try:
		f = open(_reportfilename)
		reader = csv.reader(f)

		data = list(reader)
		length = len(data)
		i = 1
		counter = 0
		f.close()

		while i < length:
			priority = ''
			test = str(data[i][4].lower()).strip()

		# Modifying the priorities as per JIRA standard
			if test == "informational" or "low":
				if str(data[i][4]).lower().strip() == 'high':
					priority = 'High'
				elif str(data[i][4]).lower().strip() == 'medium':
					priority = 'Low'
				elif str(data[i][4]).lower().strip() == 'low':
					priority = 'Lowest'
				description = 'Vulnerability: ' + str(data[i][0]).lower() + '\n Issue Details: ' + str(
                        data[i][1]).lower() + '\n Severity: ' + str(data[i][4]).lower() + '\n Vector URL: ' + str(
                        data[i][15]).lower() + '\n Vector Actor: ' + str(data[i][16]).lower()
				summary = data[i][0]

				print (summary)
				print (priority)
				print (description)

				status, _issuekey = obj.create_bug('DEV', summary, description, 'Bug', priority)
				if status:
					print ("Jira bug raised successfully. Ticket id: " + str(_issuekey))
				else:
					print ("Fail")

			print (len(data[i]))

			if len(data[i]) < 65:
				data[i].append(_issuekey)
			else:
				data[i].extend(['', _issuekey])
				print ('printing else')
			counter += 1
			i += 1
			if counter == 0:
				print ('No issues created in Jira for project ' + 'DEV')

			with open(_reportfilename, 'wb') as fp:
				a = csv.writer(fp, delimiter=',')
				a.writerows(data)

	except Exception as e:
		print (str(e))

class JiraApi(object):

	"""
		Jira Api Class
	"""

	def __init__(self):
		"""
			Constructor
		"""
		self.server = jiraserver
		self.username = jiraun
		self.password = jirapwd


	def connect(self):
		"""
			Establish connection
		"""
		try:
			self.jiraconnect = JIRA(self.server, basic_auth=(self.username, self.password))
			return True
		except:
			return False
			# Refer server as self.server, username as self.username and password as self.password and establish a connection


	def create_bug(self, project, summary, description, issue_type, priority):
		"""
			Create a bug
			Returns True on Success, False otherwise
			"""
		_issuetype = {'name':issue_type}
		_priority = {'name': priority}
		JiraIssue = self.jiraconnect.create_issue(project='DEV', summary=summary, description=description,issuetype='Bug', priority=_priority)
		issue_dict = JiraIssue.raw
		print (issue_dict)
		if issue_dict['key']:
			return (True, issue_dict['key'])
		else:
			return (False, None)
			# Create a bug using the parameters accepted...

##Sample Code to generate bug for testing

obj = JiraApi()

if obj.connect():
	jirabuglogging(reportfilename)

else:
	print ("Fail")
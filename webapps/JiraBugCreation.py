from jira import JIRA
import os
from MasterConfig import *
import csv
import requests
import sys
import http.client

http.client.HTTPConnection.debuglevel = 2

class JiraMS_URL:
    pass


def createbug(reportfilename):  # Utilizing excel file generated to input mandatory details for Jira bug logging

    try:
        f = open(reportfilename)
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
                    priority = 'Critical'
                elif str(data[i][4]).lower().strip() == 'medium':
                    priority = 'Minor'
                description = 'Vulnerability: ' + str(data[i][0]).lower() + '\n Issue Details: ' + str(
                        data[i][1]).lower() + '\n Severity: ' + str(data[i][4]).lower() + '\n Vector URL: ' + str(
                        data[i][15]).lower() + '\n Vector Actor: ' + str(data[i][16]).lower() + '\n Request: ' + str(
                        data[i][30]).lower() + '\n Response: ' + str(data[i][37]).lower()

            jsondata = {'priority': {'name': priority}, 'project': project, 'summary': 'Summary',
                        'description': description, 'issuetype': {'name': IssueType}}

            headers = {'Content-Type': 'application/json'}

            print(str(JiraMS_URL) + ',' + str(headers) + ',' + str(jsondata))

            response = requests.post(JiraMS_URL, headers=headers, json=jsondata)

            auth_jira = JIRA(server=server, basic_auth=(username, password))  # Authentication to JIRA
            issuekey = str(response.content)  # Capturing issue key returned by JIRA in a variable
            issue = JIRA.issue(auth_jira, issuekey)
            issue.update(fields={'customfield_12701': [{'value': 'Security'}]})
            print('Issue created for project ' + project + ' in Jira. You can track issue by issue key: ' + issuekey)

            # Appending issuekey to CSV for further custom reporting
            if len(data[i]) == 65:
                data[i].append(issuekey)
            else:
                data[i].extend(['', issuekey])
                print('printing else')
            counter += 1
            i += 1
            if counter == 0:
                print('No issues created in Jira for project ' + project)

            with open(reportfilename, 'wb') as fp:
                a = csv.writer(fp, delimiter=',')
                a.writerows(data)

    except Exception as e:
        print(str(e))

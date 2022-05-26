#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 26 11:31:40 2022

@author: ubuntu
"""

import urllib3
import sys
import json
import base64
import os
import datetime
import requests

# Jira settings
JIRA_URL = "https://devsecopscollab.atlassian.net"

#JIRA_USERNAME = "devsecopscollab@gmail.com"
#JIRA_PASSWORD = "L1l2l3l4l5!" # For Jira Cloud use a token generated here: https://id.atlassian.com/manage/api-tokens

JIRA_PROJECT_KEY = "DASTBUGS"
JIRA_ISSUE_TYPE = "Bug"


def jira_rest_call(data):

    # Set the root JIRA URL, and encode the username and password
    url = JIRA_URL + '/rest/api/2/issue'
    #userpass = JIRA_USERNAME + ':' + JIRA_PASSWORD
    #base64string = str(base64.b64encode(userpass.encode('UTF-8')))

    # Build the request
    #restreq = urllib3.request(url)
    #restreq.add_header('Content-Type', 'application/json')
   # restreq.add_header("Authorization", "Basic %s" % base64string)
    headers={
    "Accept": "application/json",
    "Content-Type": "application/json"
    }

    # Send the request and grab JSON response
    #response = urllib3.request.urlopen(restreq, data)
    
    #response = requests.post(url, data, headers = "{Content-Type:application/json}", auth = base64string)
    response=requests.post(url,headers=headers,data=data,auth=("devsecopscollab@gmail.com","OhxG4da92QdFAW8whzoT8EEC"))

    # Load into a JSON object and return that to the calling function
    #return json.loads(response.read())
    return response.json()


def generate_issue_data(summary, description, priority):
    # Build the JSON to post to JIRA
    json_data = '''
        {
            "fields":{
                "project":{
                    "key":"%s"
                },
                "summary": "%s",
                "issuetype":{
                    "name":"%s"
                },
                "description": "%s",
                "priority":{
                    "name":"%s"
                }
            } 
        } ''' % (JIRA_PROJECT_KEY, summary, JIRA_ISSUE_TYPE, description, priority.title())
    return json_data

def formulateData(summary, desc, priority):
    json_response = jira_rest_call(generate_issue_data(summary, desc, priority))
    print("JSON IS----------" + str(json_response))
    issue_key = json_response['key']
    print ("Created issue ", issue_key)
    return issue_key

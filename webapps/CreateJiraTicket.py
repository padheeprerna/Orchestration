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
import traceback
import re

# Jira settings
JIRA_URL = "https://devsecopscollab.atlassian.net"

# JIRA_USERNAME = "devsecopscollab@gmail.com"
# JIRA_PASSWORD = "PAwmo2mBLbj0rMc5RNzcA81B"  # For Jira Cloud use a token generated here: https://id.atlassian.com/manage/api-tokens

# JIRA_PROJECT_KEY = "DASTBUGS"
JIRA_ISSUE_TYPE = "Bug"


def jira_rest_call(JIRA_USERNAME, JIRA_PASSWORD,data):
    # Set the root JIRA URL, and encode the username and password
    url = JIRA_URL + '/rest/api/2/issue'
    userpass = JIRA_USERNAME + ':' + JIRA_PASSWORD
    userpass = userpass.encode("ascii")
    encUserPass = base64.b64encode(userpass)
    encUserPassStr = encUserPass.decode("ascii")
    # base64string = str(base64.b64encode(userpass.encode('UTF-8')))

    # Build the request
    # restreq = urllib3.request(url)
    # restreq.add_header('Content-Type', 'application/json')
    # restreq.add_header("Authorization", "Basic %s" % base64string)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Basic " + encUserPassStr
    }

    # Send the request and grab JSON response
    # response = urllib3.request.urlopen(restreq, data)

    # response = requests.post(url, data, headers = "{Content-Type:application/json}", auth = base64string)
    response = requests.post(url, headers=headers, data=data)

    # Load into a JSON object and return that to the calling function
    # return json.loads(response.read())
    return response.json()


def generate_issue_data(summary, description, priority, pkey):
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
        } ''' % (pkey, summary, JIRA_ISSUE_TYPE, description, priority.title())
    return json_data


def formulateData(JIRA_USERNAME, JIRA_PASSWORD,summary, desc, priority, pkey):
    try:
        summary = re.sub('\W+', ' ', summary)
        desc = re.sub('\W+', ' ', desc)
        priority = re.sub('\W+', ' ', priority)
        json_response = jira_rest_call(JIRA_USERNAME, JIRA_PASSWORD, generate_issue_data(summary, desc, priority, pkey))
        issue_key = json_response['key']
        return issue_key
    except Exception as e:
        print(summary)
        print(desc)
        print(priority)
        print(pkey)
        print(e)
        traceback.print_exc()

# def main():
#    formulateData("summary", "desc", "High", "DASTBUGS")

# main()

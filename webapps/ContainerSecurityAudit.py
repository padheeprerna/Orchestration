#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 11:40:15 2022

@author: ubuntu
"""
import os
import json
import time
from shutil import *
from MasterConfig import *
from lib.commons import *
from lib.commons import get_debugger
from lib.logger import Logger
from CreateJiraTicket import *
from Email import *

time = get_timenow()
myFileName = str(time.day) + '_' + str(time.month) + '_' + str(time.year) + '_' + str(time.hour) + '_' + str(
    time.minute) + '_' + str(time.second)
benchPath = "/home/ubuntu/Tools/DockerBench/docker-bench-security"
benchLog = benchPath + "/log/docker-bench-security.log.json"
auditPath = get_report_path(REPORT_PATH, "Docker_Audit_Reports")
inspecPath = auditPath + "/InSpecReport.json"
log = Logger(get_debugger(auditPath))
idList = []
idURLPart = "https://devsecopscollab.atlassian.net/browse/"
def main():
    runAudit()
    copycssForReport()
    generateAuditReport()


def runAudit():
    log.record("***Starting INSPEC Scan**")
    os.system("inspec exec /home/ubuntu/Tools/InSpecProfile/cis-docker-benchmark --reporter=json:" + inspecPath)
    log.record("***INSPEC Scan Finished***")
    log.record("***Starting DOCKER BENCH Scan***")
    os.chdir(benchPath)
    os.system("sudo sh ./docker-bench-security.sh")
    copyfile(benchLog, auditPath + '/docker-bench-security.log.json')
    log.record("***DOCKER BENCH Scan Finished***")


def generateAuditReport():
    htmlfile = open(auditPath + "/Docker-Audit-Report-" + myFileName + ".html", "w")
    htmlfile.write(
        '<report xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/Arachni/arachni/v1.4/components/reporters/xml/schema.xsd">')
    htmlfile.write('<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />')
    htmlfile.write('<title>Security Assessment Report</title>')
    htmlfile.write('<link rel="stylesheet" href="css/style.css" type="text/css" media="screen" />')
    htmlfile.write('</head>')
    htmlfile.write('<body>')
    htmlfile.write(
        '<div id="art-main"><div class="art-header"><div class="art-header-clip"><div class="art-header-center"><div class="art-header-png"></div>');
    htmlfile.write('<div class="art-header-jpeg"></div></div></div>')
    htmlfile.write('<div class="art-header-wrapper"><div class="art-header-inner"><div class="art-logo">')
    htmlfile.write(
        '<center><img src="css/images/ey-white-logo.png" width = "75" height = "75"></center><h1 class="art-logo-name">Container Security Assessment Report</h1></div>')
    htmlfile.write('</div></div></div><div class="cleared reset-box"></div>')
    htmlfile.write('<div class="art-nav"><div class="art-nav-outer"><div class="art-nav-wrapper"></div></div></div>')
    htmlfile.write('<div class="cleared reset-box"></div>')
    htmlfile.write(
        '<div class="art-sheet"><div class="art-sheet-tl"></div><div class="art-sheet-tr"></div><div class="art-sheet-bl"></div><div class="art-sheet-br"></div>')
    htmlfile.write(
        '<div class="art-sheet-tc"></div><div class="art-sheet-bc"></div><div class="art-sheet-cl"></div><div class="art-sheet-cr"></div><div class="art-sheet-cc"></div>')
    htmlfile.write(
        '<div class="art-sheet-body"><div class="art-content-layout"><div class="art-content-layout-row"><div class="art-layout-cell art-content">')
    htmlfile.write(
        '<div class="art-post"><div class="art-post-tl"></div><div class="art-post-tr"></div><div class="art-post-bl"></div><div class="art-post-br"></div>')
    htmlfile.write(
        '<div class="art-post-tc"></div><div class="art-post-bc"></div><div class="art-post-cl"></div><div class="art-post-cr"></div><div class="art-post-cc"></div>    <div class="art-post-body">')
    htmlfile.write(
        '<div class="art-post-inner art-article"><h2 class="art-postheader">  </h2><div class="cleared"></div><div class="art-postcontent">')

    # REPORT FOR DOCKER BENCH
    htmlfile.write(
        '<p styple=fon-weight:1000;"><left><b><h3 style="color:blue;"> 1. Docker Bench Report </h3></b></left></p>')
    htmlfile.write(
        "<style>table, th, td {font-family: arial, sans-serif;border: 1px solid black;border-collapse: collapse;}tr:nth-child(even) {background-color: #E8E6E5;}</style>")
    htmlfile.write('<table>')
    htmlfile.write('<tr bgcolor="#9FA68F">')  # write <tr> tag
    htmlfile.write('<th>ID</th>')
    htmlfile.write('<th>Description</th>')
    htmlfile.write('<th>Jira Bug ID</th>')
    htmlfile.write('</tr>')
    # Iterating through the json
    # list
    f1 = open(benchLog)
    data1 = json.load(f1)
    for i in data1['tests']:
        for j in i['results']:
            summary1 = ''
            desc1 = ''
            sev1 = ''
            if (j['result'] == 'WARN'):
                summary1 = "BENCH_" + str(i['id']) + "_" + str(j['id']) + "_" + i['desc']
                desc1 = j['result'] + "_" + j['desc']
                sev1 = 'Medium'
                # id1 = formulateData(summary1, desc1, sev1, "AUDBUGS")
                # idURL1 = idURLPart + id1
                htmlfile.write('<tr>')
                htmlfile.write('<td>''<center>' + j['id'] + '</center>''</td>')
                htmlfile.write('<td>' + j['desc'] + '</center>''</td>')
                # htmlfile.write('<td>''<center>''<a href = ' + idURL1 + '>' + id1 + '</a>''</center>''</td>')
                htmlfile.write('</tr>')
    htmlfile.write('</table>')

    # REPORT FOR INSPEC
    htmlfile.write(
        '<p styple=fon-weight:1000;"><left><b><h3 style="color:blue;"> 2. InSpec Host+Container Profile Report </h3></b></left></p>')
    htmlfile.write(
        "<style>table, th, td {font-family: arial, sans-serif;border: 1px solid black;border-collapse: collapse;}tr:nth-child(even) {background-color: #E8E6E5;}</style>")
    htmlfile.write('<table>')
    htmlfile.write('<tr bgcolor="#9FA68F">')  # write <tr> tag
    htmlfile.write('<th>ID</th>')
    htmlfile.write('<th>Title</th>')
    htmlfile.write('<th>Test Status</th>')
    htmlfile.write('<th>Jira Bug ID</th>')
    htmlfile.write('</tr>')
    f2 = open(inspecPath, encoding='utf-8')
    data2 = json.load(f2)
    for i in data2['profiles']:
        for j in i['controls']:
            for k in j['results']:
                summary2 = ''
                desc2 = ''
                sev2 = ''
                if (k['status'] == 'failed'):
                    if (j['id'] not in idList):
                        summary2 = "INSPEC_" + j['id'] + "_" + j['title']
                        desc2 = j['desc']
                        sev2 = 'Medium'
                        # id2 = formulateData(summary2, desc2, sev2, "AUDBUGS")
                        # idURL2 = idURLPart + id2
                        htmlfile.write('<tr>')
                        idList.append(j['id'])
                        htmlfile.write('<td>' + j['id'] + '</td>')
                        htmlfile.write('<td>' + j['title'] + '</td>')
                        htmlfile.write('<td>''<center>' + k['status'] + '</center>''</td>')
                        # htmlfile.write('<td>''<center>''<a href = ' + idURL2 + '>' + id2 + '</a>''</center>''</td>')
                        htmlfile.write('</tr>')
    htmlfile.write('</table>')
    # Closing file
    htmlfile.close()
    f1.close()
    # sendEmail(auditPath + "/Dummy", "AUDIT", "devsecopscollab@gmail.com")


def copycssForReport():
    try:
        if CSSFilePath:
            copytree(CSSFilePath, auditPath + '//css')
            log.record('debug', "Successfully copied CSS to target location")
        else:
            log.record('debug', "Issue copying CSS file to target location")
    except Exception as e:
        log.record('debug', str(e))


main()

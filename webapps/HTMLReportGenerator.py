import csv
import pandas as pd
from datetime import datetime
from urllib.request import urlopen
from urllib3.util import url
import urllib
from CustomReporting import *
from MasterConfig import *
from shutil import copyfile
from shutil import copytree
import os
import shutil
import codecs
import html
#from bs4 import BeautifulSoup
from CreateJiraTicket import *

# from WebAutomation import log
#
# inputfile = "C:\\security_automation\\reports\\WebApplication\\19-02-2018\\1519014892\\Report_19_2_2018_4_34_52.csv"
# inputfile = r"{}".format(inputfile)
# appname = "test"
# url = "url"
# print inputfile

# START - Adding the below piece of code for OWASP Dependency Check
#odcCSVPath = "C:\\Users\\Public\\Desktop\\code\\Orchestration\\webapps\\OWASP\\dependency-check-report.csv"
#htmlTable = ""
# END - Adding the below piece of code for OWASP Dependency Check

webContent = ''

def main(inputfile=None, appname=None):
    generateHtml(inputfile,appname, url, reportPathZAP, dir)


def generateHtml(inputfile, appname, url,reportPathZAP, dir):
    
    outputfile = inputfile
    outputfile = outputfile.replace('csv', 'html')
    # outputfile = r"{}".format(outputfile)
    htmlfile = open(outputfile, "w")
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
        '<center><img src="css/images/ey-white-logo.png" width = "75" height = "75"></center><h1 class="art-logo-name">Web Application Security Assessment Report</h1></div>')
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
    htmlfile.write('<table class="Fixed" >')
    htmlfile.write('<col width = "250" />')
    htmlfile.write('<col width = "80" />')
    htmlfile.write('<col width = "420" />')
    htmlfile.write('<col width = "120" />')
    htmlfile.write(
        '<p styple=fon-weight:1000;"><left><b><h3 style="color:blue;"> 1. Observation Summary </h3></b></left></p>')

    htmlfile.write('<tr bgcolor="#9FA68F">')  # write <tr> tag
    htmlfile.write('<th>Vulnerability Name</th>')
    htmlfile.write('<th>Severity</th>')
    htmlfile.write('<th>Affected URL</th>')
    htmlfile.write('<th>Jira BUG ID</th>')
    htmlfile.write('</tr>')

    with open(inputfile, 'r'):
        reader = csv.reader(open(inputfile))
        a = next(reader)
        rownum = 0

        if a == []:
            htmlfile.write('<td>''<center>' + "No Issues Reported" + '</center>''</td>')
            htmlfile.write('<td>''<center>' + "NA" + '</center>''</td>')
            htmlfile.write('<td>''<center>' + "NA" + '</center>''</td>')
            htmlfile.write('<td>''<center>' + "NA" + '</center>''</td>')
        else:

            for row in reader:
                summary = ""
                description = ""
                severity = ""
                htmlfile.write('<tr>')
                columnnum = 0
                i = 1

                if str(row[0]).lower() == 'interesting response':
                    rownum += 1
                else:
                    for column in row:
                        if str(column).lower() == 'interesting response':
                            columnnum += 1
                        else:
                            if columnnum == 0:
                            # if column == 'Null':
                            #     htmlfile.writable('<td>' + "No Issues reported" + '</td>')
                            # else:
                                htmlfile.write('<td>' + column + '</td>')
                                summary = str(column)
                            elif columnnum == 1:
                                description = str(column)
                            elif columnnum == 4:
                                if (column == 'critical'):
                                    htmlfile.write('<td style="background:#ff0000;color:white;weight:bold">''<center>' + column + '</center>''</td>')
                                elif (column == 'high'):
                                    htmlfile.write('<td style="background:#ff6600;color:white;weight:bold">''<center>' + column + '</center>''</td>')
                                elif (column == 'medium'):
                                    htmlfile.write('<td style="background:#ff9933;color:white;weight:bold">''<center>' + column + '</center>''</td>')
                                elif (column == 'low'):
                                    htmlfile.write('<td  style="background:#ffff00;color:black;weight:bold">''<center>' + column + '</center>''</td>')
                                else:
                                    htmlfile.write('<td  style="background:#0066ff;color:white;weight:bold">''<center>' + column + '</center>''</td>')
                                severity = str(column)
                            elif columnnum == 15:
                                htmlfile.write('<td style="overflow-x:auto; overflow-y:auto; max-width:420px;">' + str(html.escape(column)) + '</td>')
                                if ((len(summary) !=0) & (len(description) !=0) & (len(severity) !=0)):
                                    if (severity in ['low', 'medium', 'high', 'critical']):
                                        id = formulateData(summary, description, severity, "DASTBUGS")
                                        link = "https://devsecopscollab.atlassian.net/browse/" + id
                                        htmlfile.write('<td> <a href = ' + link + '>''<center>' + id + '</center>''</a> </td>')
                                        summary = ""
                                        description = ""
                                        severity = ""
                                    else:
                                        htmlfile.write('<td>''<center>' + '-' + '</center>''</td>')
                            elif columnnum >= 40:
                                value = str(row[-1:])
                                #htmlfile.write('<td>''<center>' + str(row[-1]) + '</center>''</td>')
                                break;

                            columnnum += 1

                #while i < 1:
                 #  htmlfile.write('<td></td>')
                  # i += 1

    htmlfile.write('</table>')

    htmlfile.write(
        '<p style=fon-weight:1000;"><left><b><h3 style="color:blue;"> 2. List of URLs Scanned for <u>' + url + '</u></h3></b></left></p>')

    #file = APP_DIR + '\sitemap.txt'
    file = APP_DIR + '//sitemap.txt'

    with open(file) as f:
        content = str(f.readlines())
        content = content.split('[')
        content = content[1].split(']')
        content = content[0].split(', ')
        conlength = len(content)
        i = 0
        while i < conlength:
            htmlfile.write('<p style="overflow-x:auto; overflow-y:auto;">')
            value = str(content[i])
            value = value.replace("\\n", "")
            htmlfile.write(value)
            htmlfile.write('</p>')
            i += 1

    htmlfile.write(
        '<p styple=fon-weight:2000;"><left><b><h3 style="color:blue;"> 3. Third Party Tools Security Assessment Results </h3></b></left></p>')
    htmlfile.write('<p styple=fon-weight:2000;"><left><b><h4 style="color:blue;"> i) Nmap </h4></b></left></p>')
    htmlfile.write(
        '<p styple=fon-weight:2000;"><left><b><h4 style="color:blue;"> ii) SSLScan </h4></b></left></p>')
    htmlfile.write('<iframe src="ThirdParty.txt"' + '" width="842" height="300"> </iframe>')

    # START - Adding the below piece of code for OWASP Dependency Check
    #htmlfile.write(
    #    '<p styple=fon-weight:2000;"><left><b><h4 style="color:blue;"> iii) OWASP Dependency Check </h4></b></left></p>')
    #dataFrame = pd.read_csv(odcCSVPath, usecols = [3, 10, 11, 17, 20])
    #htmlTable = dataFrame.to_html(index = False, na_rep = 'NA', classes = 'table table-stripped')
    #htmlfile.write(htmlTable)
    # END - Adding the below piece of code for OWASP Dependency Check
    
    
    #Added for mering ZAP RESULTS
    f = codecs.open(reportPathZAP+dir+".html", "r", "utf-8")
    #f = open(reportPathZAP+dir+".html", encoding="utf8")
    webContent = str(f.read())
    #webContent = html.tostring(tree)
    #response =urlopen(reportPathZAP+"//"+dir+".html").read()
    #webContent = response.decode('UTF-8')
    htmlfile.write(webContent)
    f.close()
    htmlfile.close()
    #Added for merging zap results

    reportname = outputfile.split('//')
    try:
        reportname = str(reportname[-1])

        finalreportdirectory = os.path.join(APP_DIR, 'WebApplicationSecurityResults')
        if os.path.isdir(finalreportdirectory):
            for the_file in os.listdir(finalreportdirectory):
                file_path = os.path.join(finalreportdirectory, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    # elif os.path.isdir(file_path):
                    #     shutil.rmtree(file_path)
                except Exception as e:
                    print (e)
            print( "Old Final Report Directory was present and successfully deleted")
            # log.record('debug', "Old Final Report Directory was present and successfully deleted")
        else:
            print ("No Old Final Report Directory was present")
            # log.record('debug', "No Old Final Report Directory was present")

        finalzipfile = os.path.join(APP_DIR, 'WebApplicationSecurityResults.zip.txt')
        if os.path.isfile(finalzipfile):

            os.remove(finalzipfile)
            print("Old Final ZIP File was present and successfully deleted")
            # log.record('debug', "Old Final ZIP File was present and successfully deleted")
        else:
            print ("No Old Final ZIP File was present")
            # log.record('debug', "No Old Final ZIP File was present")

        if os.path.isdir(finalreportdirectory):
            NewDIR = finalreportdirectory
            print ("Final Report Directory already exists")
            # log.record('debug', "Final Report Directory already exists")
        else:
            NewDIR = os.path.join(APP_DIR, 'WebApplicationSecurityResults')
            os.makedirs(NewDIR)

        targetlocation = str(NewDIR)
        targetlocation2 = os.path.join(targetlocation, str(reportname))
        cssTargetLocation = os.path.join(targetlocation, CSSFilePath)
        thirdpartypath = os.path.join(APP_DIR, 'ThirdParty.txt')
        thirdpartypath = thirdpartypath.replace("\\", "/")
        thirdpartytargetlocation = os.path.join(targetlocation, 'ThirdParty.txt')
        thirdpartytargetlocation = thirdpartytargetlocation.replace("\\", "/")

        if outputfile:
            # copyfile(outputfile, targetlocation2)
            shutil.copy(outputfile, targetlocation2)
        else:
            print ("Issue copying HTML file to destination")
            # log.record('debug', "Issue copying HTML file to destination")

        if thirdpartypath:
            # copyfile(thirdpartypath, thirdpartytargetlocation)
            shutil.copy(thirdpartypath, thirdpartytargetlocation)
            print( "ThirdParty file Copied Successfully")
        else:
            print ("Issue copying ThirdParty path to destination")
            # log.record('debug',  "Issue copying ThirdParty path to destination")

        if os.path.isdir(cssTargetLocation):
            print ("CSS files already exists")
            # log.record('debug', "CSS files already exists")
        else:
            copytree(CSSFilePath, cssTargetLocation)

        # foldertozip = APP_DIR + "\\" + "WebApplicationSecurityResults"
        foldertozip = os.path.join(APP_DIR, 'WebApplicationSecurityResults')
        if foldertozip:
            zippedfile = shutil.make_archive(foldertozip, 'zip', foldertozip)
            print ("ZIP report file created successfully")
            # log.record('debug', "ZIP report file created successfully")
            os.rename(zippedfile, zippedfile + '.txt')
        else:
            print( "Issue creating Zip report file")
            # log.record('debug', "Issue creating Zip report file")

        print ("----------------------------------------------")
        print ("                 SCAN Report                 ")
        print ("----------------------------------------------")

        print ("HTML Report: " + outputfile)
    except Exception as e:
        #print (e.message)
        print (e)
        # log.record('debug', e.message)




# main ()
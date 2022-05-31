import csv
import pandas as pd
import os
import shutil
import glob
import html
from jproperties import Properties
from datetime import datetime
from urllib3.util import url
from MasterConfig import *
from shutil import copyfile
from shutil import copytree
from lib.commons import *

htmlTable = ""
projectKey = ''

#xlSrc = "C:\\Program Files\\SonarQube\\sonarqube-9.3.0.51899\\extensions\\plugins"
#sonarProperties = 'C:\\Users\\Public\\\Desktop\\code\\Orchestration\\sonar-project.properties'
#pluginsPath = "C:\\Program Files\\SonarQube\\sonarqube-9.3.0.51899\\extensions\\plugins"
pluginsPath = '//home//ubuntu//Tools//sonarqube-8.9.8.54436//extensions//plugins'
sonarProperties = '/home/ubuntu/Tools/ClientScans/sonar-project.properties'

time = get_timenow()
myFileName = str(time.day) + '_' + str(time.month) + '_' + str(time.year) + '_' + str(time.hour) + '_' + str(
    time.minute) + '_' + str(time.second)

def not_xlsx(path, names):
    return {name for name in names if os.path.isfile(name) and not name.endswith('.xlsx')}

def generateSASTReport(inputfile, reportPath):
    outNewPath = reportPath + "//SAST-Analysis-Report-" + myFileName + ".html"
    htmlfile = open(outNewPath, "w")
    htmlfile.write(
        '<report xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/Arachni/arachni/v1.4/components/reporters/xml/schema.xsd">')
    htmlfile.write('<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />')
    htmlfile.write('<title>SAST Security Assessment Report</title>')
    htmlfile.write('<link rel="stylesheet" href="css/style.css" type="text/css" media="screen" />')
    htmlfile.write('</head>')
    htmlfile.write('<body>')
    htmlfile.write(
        '<div id="art-main"><div class="art-header"><div class="art-header-clip"><div class="art-header-center"><div class="art-header-png"></div>');
    htmlfile.write('<div class="art-header-jpeg"></div></div></div>')
    htmlfile.write('<div class="art-header-wrapper"><div class="art-header-inner"><div class="art-logo">')
    htmlfile.write(
        '<center><img src="css/images/ey-white-logo.png" width = "75" height = "75"></center><h1 class="art-logo-name">SAST Security Assessment Report</h1></div>')
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
        '<div class="art-post-inner art-article"><h2 class="art-postheader">  </h2><div class="cleared"></div>')
    htmlfile.write(
        '<p style="font-weight:bold;"><left><b><h5 style="color:blue;"> SAST Tools Assessment Results </h5></b></left></p>')

    # START - Write results of OWASP Dependency Check scan
    htmlfile.write('<br><p style="font-weight:bold;color:blue;"><left><b> i) OWASP Dependency Check Results</b></left></p>')
    dataFrame = pd.read_csv(inputfile, usecols=[3, 10, 11, 17, 20])
    dataFrame1 = dataFrame.style.set_table_styles([dict(selector='table', props=[('font-family', 'arial, sans-serif'), ('border', '1px solid black'), ('border-collapse', 'collapse')]), dict(selector='th', props=[('background-color', '#9FA68F'), ('text-align', 'center'), ('weight', 'bold'), ('font-family', 'arial, sans-serif'), ('border', '1px solid black'), ('border-collapse', 'collapse')]), dict(selector='td', props=[('font-family', 'arial, sans-serif'), ('border', '1px solid black'), ('border-collapse', 'collapse'), ('width', '100%')]), dict(selector='tr:nth-child(even)', props=[('background-color', ' #E8E6E5')])]).hide(axis = 'index')
    htmlTable = dataFrame1.to_html()
    htmlfile.write(htmlTable)
    # END - Write results of OWASP Dependency Check scan

    # START - Write results of SonarQube scan
    htmlfile.write(
        '<br><p style="font-weight:bold;color:blue;"><left><b> ii) Sonar Scan Results</b></left></p>')
    configs = Properties()
    with open(sonarProperties, 'rb') as config_file:
        configs.load(config_file)
    projectKey = configs.get('sonar.projectKey')
    os.chdir(pluginsPath)
    os.system("java -jar sonar-cnes-report-4.1.1.jar -p " + str(projectKey.data) +" -o " + reportPath + " -t 5206d2a5c6ff32de4a9052e5881651beb160505f")
    excelReport = list(glob.glob(os.path.join(reportPath, '*.xlsx')))
    df = pd.read_excel(str(excelReport[0]), sheet_name ='Issues', usecols = [1, 2, 3, 5, 6])
    #df = df[df['Severity'] == 'CRITICAL' | df['Severity'] == 'MAJOR']
    df = df[(df['Severity'] == 'CRITICAL') | (df['Severity'] == 'MAJOR')]
    for i in range(df.shape[0]): #iterate over rows
        for j in range(df.shape[1]): #iterate over columns
            df.iloc[i, j] = html.escape(str(df.iloc[i, j])) #get cell value
            #print(str(value) + ":" + str(type(value)))
    df1 = df.style.set_table_styles([dict(selector='table', props=[('font-family', 'arial, sans-serif'), ('border', '1px solid black'), ('border-collapse', 'collapse'), ('width', '100%')]), dict(selector='th', props=[('background-color', '#9FA68F'), ('text-align', 'center'), ('weight', 'bold'), ('font-family', 'arial, sans-serif'), ('border', '1px solid black'), ('border-collapse', 'collapse')]), dict(selector='td', props=[('font-family', 'arial, sans-serif'), ('border', '1px solid black'), ('border-collapse', 'collapse')]), dict(selector='tr:nth-child(even)', props=[('background-color', ' #E8E6E5')])]).hide(axis = 'index')
    #htmlTable = df.style.set_properties(**{'font-size': '11pt', 'font-family': 'Calibri','border-collapse': 'collapse','border': '1px solid black'}).render()
    htmlTable = df1.to_html()
    htmlfile.write(htmlTable)
    # END - Write results of SonarQube scan

    htmlfile.close()

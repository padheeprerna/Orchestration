from HTMLReportGenerator import *
from CustomReporting import *
from Email import *
from mail import *
from lib.logger import Logger

report_path = get_report_path(REPORT_PATH, app_type)
reportPath = get_report_path(REPORT_PATH, "WebApplication")  # path on the server to save the EY reports
reportPathZAP = 'C:/Users/MS156TY/OneDrive - EY/Documents/DevSecOps/'
myFileName = str(time.day) + '_' + str(time.month) + '_' + str(time.year) + '_' + str(time.hour) + '_' + str(
    time.minute) + '_' + str(time.second)
log = Logger(get_debugger(report_path))

def generateHtml(reportPathZAP):
    out_new_path = reportPath + "/DAST-Analysis-Report-" + myFileName + ".html"
    htmlfile = open(out_new_path, "w")
    htmlfile.write(
        '<report xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/Arachni/arachni/v1.4/components/reporters'
        '/xml/schema.xsd">')
    htmlfile.write('<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />')
    htmlfile.write('<title>Security Assessment Report</title>')
    htmlfile.write('<link rel="stylesheet" href="./css/style.css" type="text/css" media="screen" />')
    htmlfile.write('</head>')
    htmlfile.write('<body>')
    htmlfile.write(
        '<div id="art-main"><div class="art-header"><div class="art-header-clip"><div class="art-header-center"><div '
        'class="art-header-png"></div>');
    htmlfile.write('<div class="art-header-jpeg"></div></div></div>')
    htmlfile.write('<div class="art-header-wrapper"><div class="art-header-inner"><div class="art-logo">')
    htmlfile.write(
        '<center><img src="./css/images/ey-white-logo.png" width = "75" height = "75"></center><h1 '
        'class="art-logo-name">Web Application Security Assessment Report</h1></div>')
    htmlfile.write('</div></div></div><div class="cleared reset-box"></div>')
    htmlfile.write('<div class="art-nav"><div class="art-nav-outer"><div class="art-nav-wrapper"></div></div></div>')
    htmlfile.write('<div class="cleared reset-box"></div>')
    htmlfile.write(
        '<div class="art-sheet"><div class="art-sheet-tl"></div><div class="art-sheet-tr"></div><div '
        'class="art-sheet-bl"></div><div class="art-sheet-br"></div>')
    htmlfile.write(
        '<div class="art-sheet-tc"></div><div class="art-sheet-bc"></div><div class="art-sheet-cl"></div><div '
        'class="art-sheet-cr"></div><div class="art-sheet-cc"></div>')
    htmlfile.write(
        '<div class="art-sheet-body"><div class="art-content-layout"><div class="art-content-layout-row"><div '
        'class="art-layout-cell art-content">')
    htmlfile.write(
        '<div class="art-post"><div class="art-post-tl"></div><div class="art-post-tr"></div><div '
        'class="art-post-bl"></div><div class="art-post-br"></div>')
    htmlfile.write(
        '<div class="art-post-tc"></div><div class="art-post-bc"></div><div class="art-post-cl"></div><div '
        'class="art-post-cr"></div><div class="art-post-cc"></div>    <div class="art-post-body">')
    htmlfile.write(
        '<div class="art-post-inner art-article"><h2 class="art-postheader">  </h2><div class="cleared"></div><div '
        'class="art-postcontent">')
    htmlfile.write('<table class="Fixed" >')
    htmlfile.write('<col width = "250" />')
    htmlfile.write('<col width = "80" />')
    htmlfile.write('<col width = "420" />')
    htmlfile.write('<col width = "120" />')
    f = codecs.open(reportPathZAP + "/dvwa.html", "r", "utf-8")
    # f = open(reportPathZAP+dir+".html", encoding="utf8")
    webContent = str(f.read())
    # webContent = html.tostring(tree)
    # response =urlopen(reportPathZAP+"//"+dir+".html").read()
    # webContent = response.decode('UTF-8')
    htmlfile.write(webContent)
    f.close()
    htmlfile.close()
    # Added for merging zap results

def main():
    try:
        copycss()
        generateHtml(reportPathZAP)
    except Exception as e:
        # print("MY ERROR --->>>>>" + str(e))
        # print("MY ERROR 2--->>>>>" + str(traceback.print_exc()))
        log.record('debug', str(e))


def copycss():
    try:
        csstargetloaction = os.path.join(report_path, 'css')
        if CSSFilePath:
            copytree(CSSFilePath, csstargetloaction)
            log.record('debug', "Successfully copied CSS to target location")
        else:
            log.record('debug', "Issue copying CSS file to target location")

    except Exception as e:
        log.record('debug', str(e))
# --------------------------------------------------------------------------
# Program Starts
# --------------------------------------------------------------------------
main()

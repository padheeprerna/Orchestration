import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
APP_DIR = os.path.dirname(os.path.abspath(__file__))

# newpath = os.path.join(APP_DIR, 'Reports')
# print newpath

REPORT_PATH = os.path.dirname(APP_DIR)
print (REPORT_PATH)

REPORT_PATH = os.path.join(REPORT_PATH, 'reports')
print (REPORT_PATH)

externaltoolpath = os.path.join(APP_DIR, 'ThirdPartyTools.py')
print (externaltoolpath)

username = 'jashutosh'
password = 'VMJira@0401'
project = 'CS'
server = 'https://vmware-it.atlassian.net'
IssueType = 'Bug'
# JenkinsWorkspace = "D:\WebAppSecurityAutomation"
CSSFilePath = os.path.join(APP_DIR, 'css')
print (CSSFilePath)

jiraflag = False
JiraMS_URL = "http://10.127.235.84:5000/jiramicroservice"
from_ = "pankaja@vmware.com"
to = ["pankaja@vmware.com"]  # coma seperated email list
subject = "Web Application Security Assessment Result"
# Successbody = "Please find the attachment for Web Application Security Assessment Results"
Failedbody = "Scan invoked was fail. Please contact pankaja@vmware.com"
Successattachments = 'D:\security_automation\main\webapps\WebApplicationSecurityResults.zip.txt' # ABsolute path of file
FailedAttachments = ""
cc = ["pankaja@vmware.com"]
app_type = "WebApplication"


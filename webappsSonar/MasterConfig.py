import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
APP_DIR = os.path.dirname(os.path.abspath(__file__))

newpath = os.path.join(APP_DIR, 'Reports')
# print newpath

REPORT_PATH = os.path.dirname(APP_DIR)
# print REPORT_PATH

REPORT_PATH = os.path.join(REPORT_PATH, 'reports')
# print REPORT_PATH

externaltoolpath = os.path.join(APP_DIR, 'ThirdPartyTools.py')
# print externaltoolpath

username = 'devsecopscollab@gmail.com'
password = 'L1l2l3l4l5!'
project = 'DevSecOps'
server = 'https://devsecopscollab.atlassian.net'
IssueType = 'Bug'

CSSFilePath = os.path.join(APP_DIR, 'css')
# print CSSFilePath

jiraflag = True
#JiraMS_URL = "http://10.127.235.84:5000/jiramicroservice"
JiraMS_URL = "http://172.31.33.131:5000/jiramicroservice"
from_ = "devsecopscollab@gmail.com"
to = ["devsecopscollab@gmail.com"]  # coma seperated email list
subject = "Web Application Security Assessment Result"
# Successbody = "Please find the attachment for Web Application Security Assessment Results"
Failedbody = "Scan invoked was fail. Please contact devsecopscollab@gmail.com"
Successattachments = 'C:\\Users\\Public\\Desktop\\code\\Orchestration\\webapps\\*.html' # ABsolute path of file
FailedAttachments = ""
cc = ["devsecopscollab@gmail.com"]
app_type = "WebApplication"


import os
import uuid
import getopt
import traceback
import time
import stat
from subprocess import call
from MasterConfig import *
from SASTHTMLReporter import *
from lib.commons import get_report_path
from lib.commons import get_debugger
from lib.logger import Logger

time = datetime.now()
dir = str(time.day) + '_' + str(time.month) + '_' + str(time.year) + '_' + str(time.hour) + '_' + str(
    time.minute) + '_' + str(time.second)

reportPath ='//home//ubuntu//Orchestration//webapps//zap_Reports//'

log = Logger(get_debugger(reportPath))
time = datetime.now()
log.record('debug', "DAST Scan Started at: " + str(time))
log.record('debug', "Value of report path is: " + reportPath)
log_path = os.path.join(reportPath, "Debug")
log.record('debug', "Value of log_path is: " + log_path)

def main():
    try:
        startzap()
    except Exception as e:
        log.record('debug', str(e))



def startzap():
    try:
        log.record('debug', 'Initiating ZAP Scan')
        #START - OWASP zap scan
        log.record('debug', 'Starting ZAP Scan')
        os.chdir('//home//ubuntu//Tools//ZAP//ZAP_2.11.1')
        os.system('java -jar zap-2.11.1.jar -quickurl http://127.0.0.1/DVWA/login.php -quickout ' + reportPath +dir+ '.html -cmd')
        log.record('debug', 'ZAP Scan Complete')


    except Exception as e:
        log.record('debug', str(e))


main()
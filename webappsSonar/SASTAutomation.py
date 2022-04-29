import os
import uuid
import getopt
import traceback
import time
import stat
#from ..mail import *
from MasterConfig import *
from SASTHTMLReporter import *
from lib.commons import get_report_path
from lib.commons import get_debugger
from lib.logger import Logger

dir = str(uuid.uuid4().hex)

orchPath = str(os.path.dirname(os.path.realpath(sys.argv[0])))
scanPath = orchPath
#reportPath = orchPath + "\\SAST_Reports\\"+dir
#odcCSVPath = reportPath + "\\dependency-check-report.csv"
#OWASPBinPath = '\\..\\dependency-check-7.0.4-release\\dependency-check\\bin'
reportPath = orchPath + "//SAST_Reports//"+dir
odcCSVPath = reportPath + "//dependency-check-report.csv"
OWASPBinPath = '//home//ubuntu//Tools//dependency-check//bin'


log = Logger(get_debugger(reportPath))
time = datetime.now()
log.record('debug', "SAST Scan Started at: " + str(time))
log.record('debug', "Value of report path is: " + reportPath)
log_path = os.path.join(reportPath, "Debug")
log.record('debug', "Value of log_path is: " + log_path)

def main():
    try:
        startSAST()
    except Exception as e:
        log.record('debug', str(e))

def copycssForReport():
    try:
        if CSSFilePath:
            #copytree(CSSFilePath, reportPath+'\\css')
            copytree(CSSFilePath, reportPath+'//css')
            log.record('debug', "Successfully copied CSS to target location")
        else:
            log.record('debug', "Issue copying CSS file to target location")
    except Exception as e:
        log.record('debug', str(e))

def startSAST():
    try:
        log.record('debug', 'Initiating SAST Scan')
        #START - OWASP Dependency Check
        log.record('debug', 'Starting OWASP Dependency Scan')
        #os.chdir(orchPath + OWASPBinPath)
        os.chdir(OWASPBinPath)
        # os.system(
        #     'dependency-check.bat --enableExperimental --scan ' + scanPath + ' --out ' + reportPath + ' --format CSV')
        os.system(
            './dependency-check.sh --enableExperimental --scan ' + scanPath + ' --out ' + reportPath + ' --format CSV')
        log.record('debug', 'OWASP Dependency Scan Complete')
        #END - OWASP Dependency Check

        # START - SonarQube
        log.record('debug', 'Starting SonarQube Scan')
        configs = Properties()
        with open(sonarProperties, 'rb') as config_file:
            configs.load(config_file)
        projectBaseDir = configs.get('sonar.projectBaseDir')
        os.chdir(str(projectBaseDir.data))
        #os.system('sonar-scanner')
        os.system('./sonar-scanner')
        log.record('debug', 'SonarQube Complete')
        # END - SonarQube
        log.record('debug', 'SAST Scan Ended')

        if os.path.exists(odcCSVPath):
            copycssForReport()
            generateReport(odcCSVPath, reportPath)
        else:
            log.record('debug', 'SAST Scan might not have run properly! Please check.')

    except Exception as e:
        log.record('debug', str(e))


main()
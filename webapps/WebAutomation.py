import getopt
import time
from HTMLReportGenerator import *
from CustomReporting import *
from JiraBugCreation import *
import stat
from mail import *
from lib.commons import get_report_path
from lib.commons import get_debugger
from lib.logger import Logger


hostname = ''
xmlreportname = ''
csvfilepath = ''
time = datetime.now()
dir = str(time.day) + '_' + str(time.month) + '_' + str(time.year) + '_' + str(time.hour) + '_' + str(
    time.minute) + '_' + str(time.second)

finalreportpath = os.path.join(APP_DIR, 'WebApplicationSecurityResults.zip.txt')

thirdpartypath = os.path.join(APP_DIR, 'ThirdParty.txt')

# customoptions = "--http-request-concurrency=20 --http-response-max-size=10000 --http-request-timeout=5000 --http-request-queue-size=200 --scope-auto-redundant=1 --scope-directory-depth-limit=3 --browser-cluster-pool-size=10 --browser-cluster-ignore-images --scope-dom-depth-limit=2 --scope-include-pattern=www-stage.vmware.com --scope-exclude-file-extensions=css,png "
customoptions = "--http-request-concurrency=10 --http-response-max-size=10000 --http-request-timeout=5000 --http-request-queue-size=200 --scope-auto-redundant=1 --scope-directory-depth-limit=3 --browser-cluster-pool-size=10 --browser-cluster-ignore-images --scope-dom-depth-limit=2 --scope-exclude-file-extensions=css,png "

report_path = get_report_path(REPORT_PATH, app_type)
log = Logger(get_debugger(report_path))
log.record('debug', "Value of report_path is: " + report_path)
log_path = os.path.join(report_path, "Debug")
log.record('debug', "Value of log_path is: " + log_path)

afrreportname = report_path + "//" + 'Report_' + dir + '.afr'
logfilename = log_path + dir + '.log'

# --------------------------------------------------------------------------
# Function: Defining Usage
# --------------------------------------------------------------------------

def usage():
    print ('\n*************************************************************')
    print ('\n******* VMware Web Application Security Scanner Usage *******')
    print ('\n*************************************************************')
    print ('\nFor Non-Authenticated Scan')
    print ('--------------------------')
    print ('\nWebAutomation.py -u <Loginlurl>')
    print ('\nFor Authenticated Scan')
    print ('----------------------')
    print ('\nWebAutomation.py -u <Loginlurl> -n <UserName> -p <Password> -l <Platform>')
    print ('\n\nMandatory Parameters:')
    print ('---------')
    print ('\n-u Application lurl')
    print ('\n\nOptional Parameters:')
    print ('--------')
    print ('\nUsername and Password are optional. But required for authenticated scan.')
    print ('-n UserName')
    print ('-p Password')


# --------------------------------------------------------------------------
# Defining Main
# --------------------------------------------------------------------------

def main():
    deleteoldfiles()
    deleteolddirectory()
    try:

        startscan(sys.argv[1:])
    except Exception as e:
        log.record('debug', e.message)


# --------------------------------------------------------------------------
# Defining StartScan
# --------------------------------------------------------------------------

def startscan(argv):
    lurl = ''
    username = ''
    password = ''
    platform = ''

    try:
        opts, args = getopt.getopt(argv, "hu:n:p:l:", ["lurl=", "username=", "password=", "platform="])
        if len(opts) == 0:
            print ('Please check usage:')
            usage()

    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-u"):
            lurl = arg
            if lurl != '':
                splitedURL = lurl.split('/')
                hostname = splitedURL[2]
        elif opt in ("-n"):
            username = arg
        elif opt in ("-p"):
            password = arg
        elif opt in ("-l"):
            platform = arg

    try:
        if lurl != '' and username == '' or password == '':
            normalscan(sys.argv[1:])
        elif lurl != '' and username != '' and password == '':
            print ('Check Usage:')
            usage()
        elif lurl == '' and username == '' and password != '':
            print ('Check Usage:')
            usage()
        elif lurl == '' and username != '' and password == '':
            print ('Check Usage')
            usage()
        elif lurl != '' and username != '' and password != '':
            execplugin = "--plugin=exec:during=" + '"' 'python ' + externaltoolpath + ' ' + hostname
            # print "Initiating Authenticated Scan"
            log.record('debug', "Initializing Authenticated Scan")

            platformoption = "--platform=" + platform

            htmlreportname = os.path.join(report_path, 'Report_' + dir + '.html.zip')
            htmlreport = os.path.join(report_path, 'Report_' + dir + '.html')
            xmlreportname = os.path.join(report_path, 'Report_' + dir + '.xml')
            csvfilepath = os.path.join(report_path, 'Report_' + dir + '.csv')
            workingdirectory = os.path.join(report_path, 'ThirdParty.txt')

            # print(
            #     '/opt/arachni/bin/arachni ' + execplugin + '" ' + lurl + ' --plugin=login_script:script="D:\security_automation\main\webapps\loginscript.rb" ' + "--scope-exclude-pattern=logout " + platformoption + ' ' + customoptions + '--scope-include-pattern=' + hostname + ' --output-debug 1> ' + logfilename + ' --report-save-path=' + afrreportname)

            os.system('/opt/arachni/bin/arachni ' + execplugin + '" ' + lurl + ' --plugin=login_script:script="D:\security_automation\main\webapps\loginscript.rb"' + ' ' + platformoption + ' ' + customoptions + '--scope-include-pattern=' + hostname + ' --output-debug 2> ' + logfilename + ' --report-save-path=' + afrreportname)

            log.record('debug', "arachni Command Triggered is: " + 'arachni ' + execplugin + '" ' + lurl + ' --plugin=login_script:script="D:\security_automation\main\webapps\loginscript.rb"' + ' ' + platformoption + ' ' + customoptions + '--scope-include-pattern=' + hostname + ' --output-debug 2> ' + logfilename + ' --report-save-path=' + afrreportname)

            if os.path.isfile(afrreportname):
                os.system('/opt/arachni/bin/arachni_reporter ' + afrreportname + ' --reporter=html:outfile=' + htmlreportname)
                os.system('/opt/arachni/bin/arachni_reporter ' + afrreportname + ' --reporter=xml:outfile=' + xmlreportname)
            else:
                log.record('debug', "APR Report does not exist")

            if xmlreportname:
                os.system('xml2csv --input ' + xmlreportname + ' --output ' + csvfilepath + ' --tag' ' "issue"')
            else:
                log.record('debug', "XML Report not found")

            if csvfilepath:
                log.record('debug', "CSV_REPORT: " + csvfilepath)
            else:
                log.record('debug', "CSV report not present")

            if htmlreportname:
                log.record('debug', "HTML_REPORT: " + htmlreport)
            else:
                log.record('debug', "HTML report not present")

            print ("PDF_REPORT: NA")

            if csvfilepath:
                log.record('debug', csvfilepath)
                createbug(csvfilepath)
                generateHtml(csvfilepath, hostname, lurl)
            else:
                log.record('debug', "CSV Report not found")

            if xmlreportname:
                customreporting(xmlreportname)
            else:
                log.record('debug', "XML not found")

            if thirdpartypath:
                copyfile(thirdpartypath, workingdirectory)
            else:
                log.record('debug', "Issue copying Third party files to working directory")

            copycss()

            # SATT = [Successattachments];
            #
            # Successbody = "Please find the attachment for Web Application Security Results for authenticated scan of " + lurl + " application. Follow the link to access the html report directly."

            # if finalreportpath:
            #     send_email(from_, to, subject, Successbody, SATT[0], cc)
            #     print("Email sent successful")
            # else:
            #     send_email(from_, to, subject, Failedbody, FailedAttachments, cc)
            #     print("Email trigger failed")


    except Exception as e:
        log.record('debug', e.message)


# --------------------------------------------------------------------------
# Defining Non - Authenticated Scan
# --------------------------------------------------------------------------

def normalscan(argv):
    lurl = ''
    platform = ''
    try:
        opts, args = getopt.getopt(argv, "hu:l:", ["lurl=", "platform="])

        if len(opts) == 0:
            usage()
            sys.exit(2)
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-u"):
            lurl = arg
            if lurl != '':
                splitedURL = lurl.split('/')
                splitedURL = str(splitedURL[2]).split(':')
                hostname = splitedURL[0]
        elif opt in ("-l"):
            platform = arg
        else:
            print ("Please provide mandatory values")
            usage()

    try:
        execplugin = "--plugin=exec:during=" + '"' 'python ' + externaltoolpath + ' ' + hostname
        # print "Initiating Non-Authenticated Scan"
        log.record('debug', "Initiating Non-Authenticated Scan")

        platformoption = "--platform=" + platform

        htmlreportname = os.path.join(report_path, 'Report_' + dir + '.html.zip')
        htmlreport = os.path.join(report_path, 'Report_' + dir + '.html')
        xmlreportname = os.path.join(report_path, 'Report_' + dir + '.xml')
        csvfilepath = os.path.join(report_path, 'Report_' + dir + '.csv')
        workingdirectory = os.path.join(report_path, 'ThirdParty.txt')

        # print (
        # '/opt/arachni/bin/arachni ' + execplugin + '" ' + lurl + ' ' + platformoption + ' ' + '--check=xss ' + customoptions + ' --report-save-path=' + afrreportname)
        #
        # os.system(
        #     '/opt/arachni/bin/arachni ' + execplugin + '" ' + lurl + ' ' + platformoption + ' ' + '--check=xss ' + customoptions + ' --report-save-path=' + afrreportname)

        log.record('debug', "arachni Command Triggered is: " + 'Arachni ' + execplugin + '" ' + lurl + ' ' + platformoption + ' ' + customoptions + '--scope-include-pattern=' + hostname + ' --output-debug 1> ' + logfilename + ' --report-save-path=' + afrreportname)
        os.system('/opt/arachni/bin/arachni ' + execplugin + '" ' + lurl + ' ' + platformoption + ' ' + customoptions + '--scope-include-pattern=' + hostname + ' --output-debug 1> ' + logfilename + ' --report-save-path=' + afrreportname)



        os.path.isfile(afrreportname)
        os.system('/opt/arachni/bin/arachni_reporter ' + afrreportname + ' --reporter=html:outfile=' + htmlreportname)
        os.system('/opt/arachni/bin/arachni_reporter ' + afrreportname + ' --reporter=xml:outfile=' + xmlreportname)

        if xmlreportname:
            os.system('xml2csv --input ' + xmlreportname + ' --output ' + csvfilepath + ' --tag' ' "issue"')
            log.record('debug', "Value of csvfilepath: " + csvfilepath)
        else:
            log.record('debug', "XML Report Not Found")


        if csvfilepath:
            log.record('debug', "CSV_REPORT: " + csvfilepath)
        else:
            log.record('debug', "CSV report not present")

        if htmlreportname:
            log.record('debug', "HTML_REPORT: " + htmlreport)
        else:
            log.record('debug', "HTML report not present")

        log.record('debug', "PDF_REPORT: " + 'NA')

        if xmlreportname:
            customreporting(xmlreportname)
        else:
            log.record('debug', "XML Report Not Found")

        if csvfilepath:
            log.record('debug', "Calling GenerateHTML Function")
            generateHtml(csvfilepath, hostname, lurl)
        else:
            log.record('debug', "CSV Report not Found")


        if jiraflag:
            createbug(csvfilepath)
        else:
            log.record('debug', "JIRA Flag is set to 0")

        if thirdpartypath:
            copyfile(thirdpartypath, workingdirectory)
        else:
            log.record('debug', "Issue copying Third party files to working directory")

        copycss()

        # SATT = [Successattachments];
        #
        # Successbody = "Please find the attachment for Web Application Security Results for Non-Authenticated scan of " + lurl + " application. Follow the link to access the html report directly." + htmlreport

        # if finalreportpath:
        #     send_email(from_, to, subject, Successbody, SATT, cc)
        #     print("Success")
        # log.record('debug', "Success")
        # else:
        #     send_email(from_, to, subject, Failedbody, FailedAttachments, cc)
        #     print("Failed")
        # log.record('debug', "Failed")

    except Exception as e:
        log.record('debug', e.message)


# -------------------------------------------------------------------------
# Clearing old Files
# -------------------------------------------------------------------------

def deleteoldfiles():
    try:
        htmlfiletoremove = os.path.join(APP_DIR, 'WebApplicationSecurityResults.zip')
        if htmlfiletoremove:
            os.remove(htmlfiletoremove)
            log.record('debug', "Old zip reports got deleted successfully")
        else:
            log.record('debug', "Issue deleting old zip report files")
    except Exception as e:
        log.record('debug', e.message)

    try:
        txtfiletoremove = os.path.join(APP_DIR, 'WebApplicationSecurityResults.zip.txt')
        if txtfiletoremove:
            os.remove(txtfiletoremove)
            log.record('debug', "Old txt reports got deleted successfully")
        else:
            log.record('debug', "Issue deleting old txt report files")



    except Exception as e:
        log.record('debug', e.message)
# -------------------------------------------------------------------------
# Clearing old Directory
# -------------------------------------------------------------------------

def deleteolddirectory():
    try:
        dirtodelete = os.path.join(APP_DIR, 'WebApplictaionSecurityResults')
        if os.path.isdir(dirtodelete):
            for root, dirs, files in os.walk(dirtodelete, topdown=False):
                for name in files:
                    filename = os.path.join(root, name)
                    os.chmod(filename, stat.S_IWUSR)
                    os.remove(filename)
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(dirtodelete)
            log.record('debug', "Successfully deleted WebApplicationSecurityResults directory")
        else:
            log.record('debug', "WebApplicationSecurityResults does not exist")
    except Exception as e:
        log.record('debug', e.message)

def copycss():
    try:
        csstargetloaction = os.path.join(report_path, 'css')
        if CSSFilePath:
            copytree(CSSFilePath, csstargetloaction)
            log.record('debug', "Successfully copied CSS to target location")
        else:
            log.record('debug', "Issue copying CSS file to target location")

    except Exception as e:
        log.record('debug', e.message)


# --------------------------------------------------------------------------
# Program Starts
# --------------------------------------------------------------------------
main()

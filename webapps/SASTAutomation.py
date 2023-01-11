from SASTHTMLReporter import *
from lib.logger import Logger
from Email import *

# Get environment variables
odcCSVPath = os.environ.get('odcCSVPath') + "//dependency-check-report.csv"
rEmail = os.environ.get('rEmail')
reportPath = get_report_path(REPORT_PATH, "SAST_Reports")
flag = False
log = Logger(get_debugger(reportPath))
# orchPath = str(os.path.dirname(os.path.realpath(sys.argv[0])))
# scanPath = "//home//ubuntu//Tools//ClientScans"
# odcCSVPath = reportPath + "//dependency-check-report.csv"
# OWASPBinPath = '//home//ubuntu//Tools//dependeny-check//bin'
# # time = datetime.now()
# log.record('debug', "SAST Scan Started at: " + str(time))
# log.record('debug', "Value of report path is: " + reportPath)
# log_path = os.path.join(reportPath, "Debug")
# log.record('debug', "Value of log_path is: " + log_path)


def main():
    try:
        startSAST(sys.argv[1:])
    except Exception as e:
        log.record('debug', str(e))


def copycssForReport():
    try:
        if CSSFilePath:
            copytree(CSSFilePath, reportPath + '//css')
            log.record('debug', "Successfully copied CSS to target location")
        else:
            log.record('debug', "Issue copying CSS file to target location")
    except Exception as e:
        log.record('debug', str(e))


def startSAST(argv):
    try:
        if os.path.exists(odcCSVPath):
            copycssForReport()
            flag = generateSASTReport(odcCSVPath, reportPath)
            sendEmail(reportPath + "/Dummy", "SAST", rEmail)
        else:
            log.record('debug', 'SAST Scan might not have run properly! Please check.')

        return flag

    except Exception as e:
        log.record('debug', str(e))

def generateSASTReport(inputfile, reportPath):
    outNewPath = reportPath + "//SAST-Analysis-Report-" + myFileName + ".html"
    htmlfile = open(outNewPath, "w")
    htmlfile.write(
        '<report xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/Arachni/arachni/v1.4/components/reporters'
        '/xml/schema.xsd">')
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
        '<p style="font-weight:bold;"><left><b><h1 style="color:blue;"> SAST Tools Assessment Results </h1></b></left></p>')

    # START - Write results of OWASP Dependency Check scan
    htmlfile.write(
        '<br><p style="font-weight:bold;color:blue;font-size:20px"><left><b>i) OWASP Dependency Check Results </b></left></p><br>')
    dataFrame = pd.read_csv(inputfile, usecols=[3, 10, 11, 12, 14])
    if dataFrame.empty:
        htmlfile.write(
            '<br><p style="font-size:18px"><left><b> No Components/Dependencies with Known Vulnerabilities found! </left></p>')
    else:
        for i in range(dataFrame.shape[0]):
            summary1 = ''
            desc1 = ''
            severity1 = ''
            cveid = ''
            depath = ''
            vul = ''
            for j in range(dataFrame.shape[1]):
                if (dataFrame.columns[j] == 'CWE'):
                    summary1 = "OWASP_" + str(dataFrame.iloc[i, j])
                elif (dataFrame.columns[j] == 'CVSSv2_Severity'):
                    severity1 = str(dataFrame.iloc[i, j])
                    if severity1 == 'CRITICAL':
                        flag = True
                elif (dataFrame.columns[j] == 'CVE'):
                    cveid = str(dataFrame.iloc[i, j])
                elif (dataFrame.columns[j] == 'DependencyPath'):
                    depath = str(dataFrame.iloc[i, j])
                elif (dataFrame.columns[j] == 'Vulnerability'):
                    vul = str(dataFrame.iloc[i, j])
            if ((len(cveid) != 0) & (len(depath) != 0) & (len(summary1) != 0) & (len(vul) != 0) & (
                    severity1 in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'])):
                desc1 = "CVE ID: " + cveid + ". File where the bug was found: " + depath + ". Vulnerability Desc: " + vul
                # id1 = formulateData(summary1, desc1, severity1, "SASTBUGS")
                # idURL1 = idURLPart + id1
                # bugIdList1.append(idURL1)
        dataFrame['Jira Bug ID'] = bugIdList1
        bugIdList1.clear()
        dataFrame = dataFrame.drop('Vulnerability', axis=1)
        dataFrame = dataFrame.drop('DependencyPath', axis=1)
        dataFrame = dataFrame.drop('CVSSv2_Severity', axis=1)
        dataFrame1 = dataFrame.style.set_table_styles([dict(selector='table',
                                                            props=[('table-layout', 'fixed'), ('font-size', '15px'),
                                                                   ('font-family', 'arial, sans-serif'),
                                                                   ('border', '1px solid black'),
                                                                   ('border-collapse', 'collapse'), ('width', '100%')]),
                                                       dict(selector='th', props=[('font-size', '15px'),
                                                                                  ('background-color', '#9FA68F'),
                                                                                  ('text-align', 'center'),
                                                                                  ('weight', 'bold'),
                                                                                  ('font-family', 'arial, sans-serif'),
                                                                                  ('border', '1px solid black'),
                                                                                  ('border-collapse', 'collapse')]),
                                                       dict(selector='tr', props=[('font-family', 'arial, sans-serif'),
                                                                                  ('border', '1px solid black'),
                                                                                  ('border-collapse', 'collapse')]),
                                                       dict(selector='td', props=[('overflow', 'hidden'),
                                                                                  ('text-overflow', 'ellipsis'),
                                                                                  ('word-wrap', 'break-word'),
                                                                                  ('font-family', 'arial, sans-serif'),
                                                                                  ('border', '1px solid black'),
                                                                                  ('border-collapse', 'collapse'),
                                                                                  ('font-size', '15px')]),
                                                       dict(selector='tr:nth-child(even)',
                                                            props=[('background-color', ' #E8E6E5')])]).hide(
            axis='index')
        htmlTable = dataFrame1.to_html()
        htmlfile.write(htmlTable)
    # END - Write results of OWASP Dependency Check scan

    # # START - Write results of SonarQube scan
    # htmlfile.write(
    #     '<br><p style="font-weight:bold;color:blue;font-size:20px"><left><b> ii) Sonar Scan Results </b></left></p><br>')
    # configs = Properties()
    # with open(sonarProperties, 'rb') as config_file:
    #     configs.load(config_file)
    # projectKey = configs.get('sonar.projectKey')
    # os.chdir(pluginsPath)
    # os.system("java -jar sonar-cnes-report-4.1.1.jar -p " + str(
    #     projectKey.data) + " -o " + reportPath + " -t 5206d2a5c6ff32de4a9052e5881651beb160505f")
    # excelReport = list(glob.glob(os.path.join(reportPath, '*.xlsx')))
    # df = pd.read_excel(str(excelReport[0]), sheet_name='Issues', usecols=[1, 2, 3, 5, 6])
    # if df.empty:
    #     htmlfile.write('<br><p style="font-size:18px"><left><b> No vulnerabilities found in code! </left></p>')
    # else:
    #     # df = df[df['Severity'] == 'CRITICAL' | df['Severity'] == 'MAJOR']
    #     df = df[(df['Severity'] == 'CRITICAL') | (df['Severity'] == 'MAJOR') | (df['Severity'] == 'BLOCKER')]
    #     for i in range(df.shape[0]):
    #         summary2 = ''
    #         desc2 = ''
    #         severity2 = ''
    #         type2 = ''
    #         file2 = ''
    #         line2 = ''
    #         for j in range(df.shape[1]):
    #             df.iloc[i, j] = html.escape(str(df.iloc[i, j]))
    #             if df.columns[j] == 'Message':
    #                 summary2 = "SONAR_" + str(df.iloc[i, j])
    #             elif df.columns[j] == 'Severity':
    #                 if df.iloc[i, j] == "MAJOR":
    #                     severity2 = "HIGH"
    #                 else:
    #                     severity2 = str(df.iloc[i, j])
    #                 if severity2 == 'CRITICAL':
    #                     flag = True
    #             elif df.columns[j] == 'Type':
    #                 type2 = str(df.iloc[i, j])
    #             elif df.columns[j] == 'File':
    #                 file2 = str(df.iloc[i, j])
    #             elif df.columns[j] == 'Line':
    #                 line2 = str(df.iloc[i, j])
    #         if ((len(type2) != 0) & (len(file2) != 0) & (len(summary2) != 0) & (len(line2) != 0) & (
    #                 severity2 in ['HIGH', 'CRITICAL', 'BLOCKER'])):
    #             desc2 = "Type of bug is: " + type2 + ". File where the bug was found: " + file2 + ". Line no. in file: " + line2
    #             id2 = formulateData(summary2, desc2, severity2, "SASTBUGS")
    #             idURL2 = idURLPart + id2
    #             bugIdList2.append(idURL2)
    #     df['Jira Bug ID'] = bugIdList2
    #     bugIdList2.clear()
    #     df = df.drop('File', axis=1)
    #     df = df.drop('Line', axis=1)
    #     df1 = df.style.set_table_styles([dict(selector='table', props=[('table-layout', 'fixed'), ('font-size', '15px'),
    #                                                                    ('font-family', 'arial, sans-serif'),
    #                                                                    ('border', '1px solid black'),
    #                                                                    ('border-collapse', 'collapse'),
    #                                                                    ('width', '100%')]), dict(selector='th', props=[
    #         ('font-size', '15px'), ('background-color', '#9FA68F'), ('text-align', 'center'), ('weight', 'bold'),
    #         ('font-family', 'arial, sans-serif'), ('border', '1px solid black'), ('border-collapse', 'collapse')]),
    #                                      dict(selector='tr', props=[('font-family', 'arial, sans-serif'),
    #                                                                 ('border', '1px solid black'),
    #                                                                 ('border-collapse', 'collapse')]),
    #                                      dict(selector='td',
    #                                           props=[('overflow', 'hidden'), ('text-overflow', 'ellipsis'),
    #                                                  ('word-wrap', 'break-word'), ('font-family', 'arial, sans-serif'),
    #                                                  ('border', '1px solid black'), ('border-collapse', 'collapse'),
    #                                                  ('font-size', '15px')]), dict(selector='tr:nth-child(even)',
    #                                                                                props=[('background-color',
    #                                                                                        ' #E8E6E5')])]).hide(
    #         axis='index')
    #     # htmlTable = df.style.set_properties(**{'font-size': '11pt', 'font-family': 'Calibri','border-collapse': 'collapse','border': '1px solid black'}).render()
    #     htmlTable = df1.to_html()
    #     htmlfile.write(htmlTable)
    #     # END - Write results of SonarQube scan

    htmlfile.write('</div>')
    htmlfile.close()
    return flag

# def cleanDir():
#     for root, dirs, files in os.walk(scanPath):
#         for f in files:
#             os.unlink(os.path.join(root, f))
#         for d in dirs:
#             shutil.rmtree(os.path.join(root, d))
#

main()

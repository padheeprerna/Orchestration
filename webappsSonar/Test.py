import os


csvfilepath = r"C:\security_automation\reports\WebApplication\15-02-2018\1518682569\Report_15_2_2018_8_16_9.csv"

csvfilepath = r"{}".format(csvfilepath)

print( csvfilepath)
print ('Python ' + 'HTMLReportGenerator.py' + ' ' + csvfilepath)
os.system('Python ' + 'HTMLReportGenerator.py' + ' ' + csvfilepath)
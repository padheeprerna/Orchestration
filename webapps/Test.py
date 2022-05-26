#import os


#csvfilepath = r"C:\security_automation\reports\WebApplication\15-02-2018\1518682569\Report_15_2_2018_8_16_9.csv"

#csvfilepath = r"{}".format(csvfilepath)

#print( csvfilepath)
#print ('Python ' + 'HTMLReportGenerator.py' + ' ' + csvfilepath)
#os.system('Python ' + 'HTMLReportGenerator.py' + ' ' + csvfilepath)

import json
f = open("/home/ubuntu/Orchestration/InSpecReport.json")
data = json.load(f)
for i in data['profiles']:
    for j in i['controls']:
        for k in j['results']:
            if (k['status'] == 'failed'):
                print("ID-------" + j['id'])
                print("TITLE-------" + j['title'])
                print('STATUS--------'+k['status'])
                if (('Hashie' not in str(k['code_desc']))):
                    print('DESC------'+k['code_desc'])

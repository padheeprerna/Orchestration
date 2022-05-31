#import os


#csvfilepath = r"C:\security_automation\reports\WebApplication\15-02-2018\1518682569\Report_15_2_2018_8_16_9.csv"

#csvfilepath = r"{}".format(csvfilepath)

#print( csvfilepath)
#print ('Python ' + 'HTMLReportGenerator.py' + ' ' + csvfilepath)
#os.system('Python ' + 'HTMLReportGenerator.py' + ' ' + csvfilepath)

#import json
#f = open("/home/ubuntu/Orchestration/InSpecReport.json")
#data = json.load(f)
#for i in data['profiles']:
 #   for j in i['controls']:
  #      for k in j['results']:
   #         if (k['status'] == 'failed'):
    #            print("ID-------" + j['id'])
     #           print("TITLE-------" + j['title'])
      #          print('STATUS--------'+k['status'])
       #         if (('Hashie' not in str(k['code_desc']))):
        #            print('DESC------'+k['code_desc'])

import pandas as pd

data = {'Name': ['Ankit', 'Amit', 'Aishwarya', 'Priyanka'],
                'Age': [21, 19, 20, 18],
                'Stream': ['Math', 'Commerce', 'Arts', 'Biology'],
                'Percentage': [88, 92, 95, 70]}

df = pd.DataFrame(data, columns = ['Name', 'Age', 'Stream', 'Percentage'])

for i in range(df.shape[0]): #iterate over rows
    for j in range(df.shape[1]): #iterate over columns
        df.iloc[i, j] = str(df.iloc[i, j]) #get cell value
print(df)

#import html 
#str1 = "Define a constant instead of duplicating this literal '</center>' 6 times."
#print(str1)
#str1 = html.escape(str1)
#print(str1)
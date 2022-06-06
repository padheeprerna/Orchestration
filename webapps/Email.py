#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 30 04:44:14 2022

@author: ubuntu
"""
from __future__ import print_function

import os
import shutil
import smtplib
import glob
import json
import requests
import json
import httplib2
from lib.commons import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from apiclient import errors
from googleapiclient.discovery import build
from oauth2client import file

secFile = "/home/ubuntu/Orchestration/webapps/client_secrets.json"
credFile = "/home/ubuntu/Orchestration/webapps/mycreds.txt"

time = get_timenow()
name = str(time.day) + '_' + str(time.month) + '_' + str(time.year) + '_' + str(time.hour) + '_' + str(
    time.minute) + '_' + str(time.second)
mailDir = "ForEmail-" + name


def zipDir(reportPath):
    os.chdir(reportPath)
    if (not os.path.isdir(mailDir)):
        os.mkdir(mailDir)
    shutil.copytree(reportPath + "/css", reportPath + "/" + mailDir + "/css")
    files = glob.iglob(os.path.join(reportPath, "*.html"))
    for file in files:
        if os.path.isfile(file):
            shutil.copy2(file, reportPath + "/" + mailDir)
    files = glob.iglob(os.path.join(reportPath, "*.zip"))
    for file in files:
        if os.path.isfile(file):
            shutil.copy2(file, reportPath + "/" + mailDir)
    shutil.make_archive("Report-" + name, "zip", reportPath + "/" + mailDir)
    
def copyReqFiles(reportPath):
    shutil.copy2(secFile, reportPath)
    shutil.copy2(credFile, reportPath)
    
#def retrieve_permissions(service, file_id):
#    try:
#        permissions = service.permissions().list(fileId=file_id).execute()
#        print(str(permissions.get('items', [])[0]['id']))
#        return str(permissions.get('items', [])[0]['id'])
#    except Exception as e:
#        print ('An error occurred: ' + str(e))
#        return None
    
def insert_permission(service, file_id, perm_type, role):
  new_permission = {
      'type': perm_type,
      'role': role
  }
  try:
    return service.permissions().insert(
        fileId=file_id, body=new_permission).execute()
  except errors.HttpError:
    print ('An error occurred: ' + errors.HttpError)
  return None
    
def uploadToDrive(reportPath):
    #Following code needs token revision every 1 hour
    #headers = {"Authorization": "Bearer ya29.a0ARrdaM8Tkzj7sPpiJgIfYSyj4PWFLHi-XXeXUlto34ndkxUnPOBoXQbzNLWcm66Y9AoBTHB5uVR1UhG2ljs8K-2cehOhxzfLvfxnI1AnUAYcaU7NYHNc9k66UO6DyH8pdxIz6EEzR2Pb6S3uMPdUspSYlB68"}
    #para = {
    #    "name": "Report-" + name,
    #} 
    #files = {
    #    'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
    #    'file': ('application/zip',open(reportPath + "/Report-" + name + ".zip", "rb"))
    #} 
    #r = requests.post(
    #    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
    #    headers=headers,
    #    files=files
    #)
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("mycreds.txt")

    drive = GoogleDrive(gauth)
    file1 = drive.CreateFile()
    file1.SetContentFile(reportPath + "/Report-" + name + ".zip")
    file1.Upload()
    
    http = httplib2.Http()
    store = file.Storage('mycreds.txt')
    creds = store.get()
    http = creds.authorize(http)
    service = build('drive', 'v2', http=http)
    #print(str(file1))
    #permission_id = retrieve_permissions(service, file1['id'])
    #print("PERM ID-----------" + permission_id)
    insert_permission(service, file1['id'], 'anyone', 'reader')
    return file1['id']
    
def sendEmail(reportPath, subject):
    reportPath = reportPath[:reportPath.rfind('/')]
    zipDir(reportPath)
    copyReqFiles(reportPath)
    did = uploadToDrive(reportPath)
    driveLink = "https://drive.google.com/open?id="+did
    mail_content = '''
    Hi there,
    
    Security Reports have been uploaded to %s .
    Please do not reply to this email as this is sent using Python SMTP library.
    
    Thanks & Best Regards,
    DevSecOps Team
    
    ''' % driveLink
    sender_address = 'devsecopscollab@gmail.com'
    sender_pass = 'L1l2l3l4l5!'
    receiver_address = 'devsecopscollab@gmail.com'
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject + ' Security Report'
    message.attach(MIMEText(mail_content, 'plain'))
    #attach_file_name = reportPath + "/Report-" + name + ".zip"
    #attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
    #payload = MIMEBase('application', 'octate-stream')
    #payload.set_payload((attach_file).read())
    #encoders.encode_base64(payload) #encode the attachment
    #payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    #message.attach(payload)
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
    

    
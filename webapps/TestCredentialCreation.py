#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 04:03:23 2022

@author: ubuntu
"""

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
driveFolderID = "1Bj1fUP_9IqxQcpnDBs4WGijxx98JF7Uf"

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

file1 = drive.CreateFile({'parents' : [{'id' : driveFolderID}], 'title' : 'Automation Report.txt'})
file1.SetContentString("TEST FILE")
file1.Upload()
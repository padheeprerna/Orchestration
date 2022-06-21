#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 20 06:48:12 2022

@author: ubuntu
"""
import socket
import os
import sys
import getopt
import yaml
from yaml.loader import SafeLoader
    
def find_files(filename, search_path):
   result = []

   for root, dir, files in os.walk(search_path):
      if filename in files:
         result.append(os.path.join(root, filename))
   return result[0]

def formURL(argv):
# Open the file and load the file
    composeFilePath = find_files("docker-compose.yml","/home/ubuntu/Tools/ClientScans")
    with open(composeFilePath) as f:
        data = yaml.load(f, Loader=SafeLoader)
        portList = data['services']['ctf-web']['ports']
        port = str(portList)
        port = port.replace("\'", "")
        port = port.replace("[", "")
        port = port.replace("]", "")
        port = port.split(":")
        port = str(port[0])
        
    hostname=socket.gethostname()   
    IPAddr=socket.gethostbyname(hostname) 
    url = "http://" + str(IPAddr) + ":" + port + "/"
    cmd = "sudo -H -u ubuntu bash -c '/usr/bin/python3.10 /home/ubuntu/Orchestration/webapps/WebAutomation.py -u " + url
    username = ''
    password = ''
    platform = ''
    rEmail = ''

    opts, args = getopt.getopt(argv, "n:p:l:e:", ["username=", "password=", "platform=", "rEmail="])
    for opt, arg in opts:
        if opt in ("-n"):
            username = arg
        elif opt in ("-p"):
            password = arg
        elif opt in ("-l"):
            platform = arg
        elif opt in ("-e"):
            rEmail = arg
    
    if (platform):
        cmd = cmd + " -l " + platform
    if (username):
        if (password):
            cmd = cmd + " -n " + username + " -p " + password
    if (rEmail):
        cmd = cmd + " -e " + rEmail
    cmd = cmd + "'"
    os.system(cmd)
    
def main():
    formURL(sys.argv[1:])
        
main()


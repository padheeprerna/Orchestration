#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 16 05:30:29 2022

@author: ubuntu
"""
from requests import Session
from bs4 import BeautifulSoup as bs
from pprint import pprint

def main():
    with Session() as s:
        site = s.get("https://172.31.3.192:5000/login", verify=False)
        bs_content = bs(site.content, "html.parser")
        login_data = {"username": "admin", "password": "admin#123"}
        response = s.post("https://172.31.3.192:5000/login",login_data)
        home_page = s.get("https://172.31.3.192:5000/api/report/attack")
        print("CONTENT IS------" + str(home_page.content))
        print("JSON is-------" + str(home_page.json()))
        
        
        
main()
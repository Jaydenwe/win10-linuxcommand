# -*- coding: UTF-8 -*-
 
import  Image,ImageDraw,ImageFont  
import win32api,win32con,win32gui  
import re,os,sys
import urllib2
from bs4 import BeautifulSoup
from random import choice
import time
import ConfigParser
import tkinter as tk
import thread
import threading
m = 1
def btnHelloClicked():
    cd = float(entryCd.get())
    global m
    m = cd
    #labelHello.config(text = "%.2f°C = %.2f°F" %(cd, cd*1.8+32))
    
def print_x(x, y):
    while True:
        print m
        time.sleep(3)
    
               
url = "http://man.linuxde.net/ls"
response = urllib2.urlopen(url)
html = response.read()
#print html
soup = BeautifulSoup(html)

soup.find_all(id ="content-index")[0].string = ""


txt =  soup.find_all('div', "post_bd post")[0].text
print  txt



    



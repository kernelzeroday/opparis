#"""
#Created on Sat Feb 19 07:36:49 2011
#
#@author: - TheHitchhiker
#@options: -o  - save working proxies to alives.txt (appending)
#@license: MIT
#@file-format: each proxy one line like '212.59.105.18:3128'
#"""

import sys
import urllib
import socket
import time

socket.setdefaulttimeout(5)

def time_d(start, end):
    out = end - start
    gm = time.gmtime(out)
    out = time.strftime("%S", gm)
    return out
    
def get_list_from_file(file_path):
    f = open(file_path).read()
    f = f.split("\n")
    
    return f

def save_alive_proxy(proxy):
    try:
        SAVE_ALIVE_PROXY_F.write(proxy + "\n")
    except:
        pass
    
def check_proxy(proxy):
    try:
        proxies = {"http": "http://" + str(proxy)}
        opener = urllib.FancyURLopener(proxies)
        opener.open("http://www.google.com")
        
        save_alive_proxy(proxy)
        
        print "\tAlive"
    except(IOError), msg:
        print "\t[-] Dead: ", msg

def check_args():
    SAVE_ALIVE = False
    file_path = "alives.txt"
    
    for arg in sys.argv:
        if arg.lower() == "-o":
            SAVE_ALIVE = True
        if not arg.startswith("-"):
            file_path = arg
    
    return SAVE_ALIVE, file_path
        
SAVE_ALIVE, file_path = check_args()

if SAVE_ALIVE:
    SAVE_ALIVE_PROXY_F = open("alives.txt", "a")
        
for proxy in get_list_from_file(file_path):
    if proxy != "" or proxy != "\n":
        start = time.time()
        print "##### Testing: ", proxy
        check_proxy(proxy)
        end = time.time()
        print "\tSpeed: " + str(time_d(start, end)) + "s\n"
        
print "Saved: ", SAVE_ALIVE

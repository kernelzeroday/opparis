#!/usr/bin/env python
"""
Find Open Webservers

You need a list of subnets to scan

For example, all possible syrian networks:

http://pastebin.com/raw.php?i=9BpEdhLb

Save it as 'ips.txt' in the same directory as this script

"""

import socket
import subprocess
import sys
from datetime import datetime
import re
from ipaddress import *



# Clear the screen
subprocess.call('clear', shell=True)

# Get list of syrian IPS:



# open the list of ips
f=open('ips.txt')
lines=f.readlines()

#iterate over them

for line in lines:
    #remoteServerIP  = socket.gethostbyname(line)
    line = line.strip('\n')
    for addr in IPv4Network(line):
        addr = str(addr)
# Print a nice banner with information on which host we are about to scan
        print ("-" * 60)
        print ("Please wait, scanning remote host %s" % addr)
        print ("-" * 60)

# Check what time the scan started
        t1 = datetime.now()
        try:
            for port in (80,443):  
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((addr,port))
                if result == 0:
                    print ("Port {}: \t Open".format(port))
                    sock.close()

        except KeyboardInterrupt:
            print ("You pressed Ctrl+C")
            sys.exit()

        except socket.gaierror:
            print ('Hostname could not be resolved. Exiting')
            sys.exit()

        except socket.error:
            print ("Couldn't connect to server")
            sys.exit()

# Checking the time again
t2 = datetime.now()

# Calculates the difference of time, to see how long it took to run the script
total =  t2 - t1

# Printing the information to screen
print ('Scanning Completed in: %s ' % total)

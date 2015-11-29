#!/usr/bin/env python
# snoeper.py

#import ipaddress
# use pip install netaddr to install the following dependency.
from netaddr import *
import socket
import sys
import os
import getopt

networks = [ '5.0.0.0/16'
            ,'5.104.128.0/21' 
            ,'5.134.200.0/21' 
            ,'5.134.224.0/19' 
            ,'31.9.0.0/16' 
            ,'31.193.64.0/20' 
            ,'37.48.128.0/18' 
            ,'37.48.192.0/19' 
            ,'46.53.0.0/17' 
            ,'46.57.128.0/17' 
            ,'46.58.128.0/17' 
            ,'46.161.192.0/18' 
            ,'46.213.0.0/16' 
            ,'77.44.128.0/17' 
            ,'78.110.96.0/20' 
            ,'78.155.64.0/19' 
            ,'82.137.192.0/18' 
            ,'88.86.0.0/19' 
            ,'90.153.128.0/17' 
            ,'91.144.0.0/18' 
            ,'94.141.192.0/19' 
            ,'94.252.128.0/17' 
            ,'95.87.112.0/21' 
            ,'95.140.96.0/20' 
            ,'95.159.0.0/18' 
            ,'109.238.144.0/20' 
            ,'130.0.240.0/20']

# for testing
#networks = ['192.168.1.0/24']
#networks = ['5.0.0.217','5.0.0.218']


if __name__ == "__main__":
    lower = 1
    upper = 65535
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"h:l:u:",["lower=","upper="])
    except getopt.GetoptError:
        print 'Usage: python snoeper.py -l <lower port> -u <upper port>'
        sys.exit(2)
 
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: python snoeper.py -l <lower port> -u <upper port>'
            sys.exit()
        if opt in ("-l", "--lower"):
            lower = int(arg)
        if opt in ("-u", "--upper"):
            upper = int(arg)

    
    try:
        for n in networks:
            network = IPNetwork(n)
            for ip in network:
                print ip
                remoteServerIP  = socket.gethostbyname(str(ip))
                for port in range(lower,upper):  
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(10)
                    result = sock.connect_ex((remoteServerIP, port))                        
                    
                    # if the following error is returned then i assume that is not usefull to scan any further
                    # on the give ip address.
                    if os.strerror(result)=="No route to host" or os.strerror(result)=="Resource temporarily unavailable":
                        #print os.strerror(result)
                        break
                    if result == 0:    
                        print remoteServerIP, port
                        chunk = "" 
                        try:                                   
                            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                        
                            s.connect((remoteServerIP, port))
                            s.settimeout(5)
                           
                            message = "GET / HTTP/1.1\r\n\r\n"
                            chunk = ""
                        
                        
                            #Send the whole string(sendall() handles the looping for you)
                            s.sendall(message.encode('utf8') )
                                                    
                            chunk = s.recv(4096)                                                
                        except socket.error:
                            pass
                        except:
                            pass
                        response = chunk
                        
                        if "content-type: text/html" in response.lower():                        
                            print "web server found on ",remoteServerIP, port                    
                        s.close()
                    sock.close()
     
    except KeyboardInterrupt:
        print "You pressed Ctrl+C"
        sys.exit()
     
    except socket.gaierror:
        print 'Hostname could not be resolved. Exiting'
        sys.exit()
     
    except socket.error:
        print "Couldn't connect to server"
        sys.exit()

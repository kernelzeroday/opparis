#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Name: FacebookReport (v.0.1.0)
# About: The script is an adaptation for Facebook of the TwitterReport.
#	 It accepts targets as a full url (e.g., https://facebook.com/username or https://facebook.com/profile.php?id=idNumber), a username or an idNumber
#
# Requirements:
# - Python 2.7
# - Python Requests Module (http://stackoverflow.com/questions/17309288/importerror-no-module-named-requests)
# - Splinter (http://splinter.readthedocs.org/en/latest/install.html)
# 
# Usage:  python FBReport.py -u YOUR_USER_NAME
#
# Linux/Unix:
# - Linux Pip install instructions: http://pip.readthedocs.org/en/stable/installing/
# - Requests module instructions: http://stackoverflow.com/questions/17309288/importerror-no-module-named-requests
# - Splinter module instructions : http://splinter.readthedocs.org/en/latest/install.html
# 
# Windows:
# - Make sure pip is installed: http://pip.readthedocs.org/en/stable/installing/
# - Open up cmd and run c:\python27\scripts\easy_install.exe request
# - Get the zip : https://github.com/cobrateam/splinter/archive/master.zip unzip on your disk, 
# open a terminal (start menu -> type cmd -> launch cmd.exe) 
# go in the folder you unzip splinter (cd XXXX) launch 'python setup.py install'
# - You may also need to open up cmd and run the following command: c:\python27\scripts\easy_install.exe request
# if the requests module is not installed
# 
# Need Help or Find a Bug?
# - /join #OpParis - https://webchat.anonops.com/?channels=OpParis
# Want to contribute?
# - /join #OpParis-Dev - https://webchat.anonops.com/?channels=OpParis-Dev


# TODO:
# - define a server-side function to retrieve the next target
# - detect exception conditions
# - improve performances
# - testing

import sys
try:
    from splinter import Browser
except:
    print "Please install Splinter."
    print "* Unix/Linux Use: sudo pip install splinter"
    print "* Windows: See script's comments"
    print "* More Info: http://splinter.readthedocs.org/en/latest/install.html"
    sys.exit()
try:
    import requests
except:
    print "Please install the requests module."
    print "* Unix/Linux Use: pip install requests"
    print "* Windows in CMD: c:\python27\scripts\easy_install.exe request"
    print "* More Info: http://stackoverflow.com/questions/17309288/importerror-no-module-named-requests"
    sys.exit()
    
import getopt, re, time
from splinter.request_handler.status_code import HttpResponseError
import getpass

# TODO Bot Variables
#o="opparis"
#op_srv="optools.anonops.com"

# TODO: Notifies target is offline
# def updateTarget(o,t)

def main(argv):

    username = None
    try:
        opts, args = getopt.getopt(argv,"h:u:",["user="])
    except getopt.GetoptError:
        print 'Usage: python FBReport.py -u <Facebook username>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: python FBReport.py -u <Facebook username>'
            sys.exit()
        elif opt in ("-u", "--user"):
            username = arg
            n = username

    if not username:
        print 'Usage: python FBReport.py -u <Facebook username>'
        sys.exit()

    password = getpass.getpass()

# comment this line if you want to use privoxy + tor:
    with Browser() as browser:
# uncomment this section if you want to use privoxy + tor:
#    proxyIP = '127.0.0.1'
#    proxyPort = 8118
#
#    proxy_settings = {'network.proxy.type': 1,
#            'network.proxy.http': proxyIP,
#            'network.proxy.http_port': proxyPort,
#            'network.proxy.ssl': proxyIP,
#            'network.proxy.ssl_port':proxyPort,
#            'network.proxy.socks': proxyIP,
#            'network.proxy.socks_port':proxyPort,
#            'network.proxy.ftp': proxyIP,
#            'network.proxy.ftp_port':proxyPort 
#            }
#
#    with Browser('firefox',profile_preferences=proxy_settings) as browser:
        try:
	    #Login
            browser.visit("https://facebook.com/login.php")
            time.sleep(1)
            browser.execute_script('document.getElementById("email").value="'+username+'"')
            browser.execute_script('document.getElementById("pass").value="'+password+'"')
            browser.find_by_name("login").first.click()
            #time.sleep(1)

            if "https://www.facebook.com/login.php?login_attempt=" in browser.url:
                print "Facebook Login Failed!"
                sys.exit()

        except Exception, e:
	    print e
            print "Unexpected error occured while trying the Facebook login. Please try running the script again."
            sys.exit()

        while True:
            try:
                #TODO Get target from target queue
                #t = requests.get(SERVICE URL)
                #tg = t.content
                if tg == "" or tg == "noassignment" or ("error" in tg) or ("What happened?" in tg) or ("CloudFlare" in tg) or ("Cloudflare" in tg) or ("Checking your browser" in tg):
                    print "No current assignment"
                    time.sleep(3)
                else:
		    #Prepare the user URL
		    if ("facebook.com" in tg): 
		    	url=tg
		    else:
		    	url="https://facebook.com/"+tg

		    browser.visit(url)
		    time.sleep(1)
		    msg=""
                    if not browser.is_element_present_by_id('standard_error'):
                        browser.execute_script('document.getElementsByClassName("_42ft _4jy0 _1yzl _p _4jy4 _517h _51sy")[0].click()')
			time.sleep(1)

			browser.click_link_by_partial_href('/ajax/nfx/start_dialog?story_location=profile_someone_else&reportable_ent_token')
			time.sleep(1)

			browser.find_by_name('answer')[1].click()
			browser.execute_script('document.getElementsByClassName("_42ft _4jy0 layerConfirm _5xcs _5ipw uiOverlayButton _4jy3 _4jy1 selected _51sy")[0].click()')
			time.sleep(1)			

			browser.find_by_name('answer')[2].click()
			browser.execute_script('document.getElementsByClassName("_42ft _4jy0 layerConfirm _5xcs _5ipw uiOverlayButton _4jy3 _4jy1 selected _51sy")[0].click()')
			time.sleep(1)

			browser.find_by_name('answer')[2].click()
			browser.execute_script('document.getElementsByClassName("_42ft _4jy0 layerConfirm _5xcs _5ipw uiOverlayButton _4jy3 _4jy1 selected _51sy")[0].click()')
			time.sleep(1)

			#Check if already reported, 
			if(len(browser.find_by_css("div._5dg3"))>0):
				msg = tg+'- Already reported'			
			#Report!
			elif(len(browser.find_by_css('a._16gh[ajaxify^="/ajax/feed/filter_action/nfx_action_execute?action_name=REPORT_CONTENT"]'))>0):			
				browser.execute_script('document.getElementsByClassName("_16gh")[0].click()')
				time.sleep(1)
				msg = tg+' - Reported'

                    elif browser.is_element_present_by_css('DETECT IF IT IS SUSPENDED'):
                        msg =  tg+' - Suspended'
                        #updatetarget(o,tg)
                    elif browser.is_element_present_by_id('standard_error'):
                        msg =  tg+' - Does not exist'
                        #updatetarget(o,tg)
                    else:
                        msg = tg+' - Unknown'
                        #updatetarget(o,tg)

                    print msg
            except KeyboardInterrupt:
                print 'Quit by keyboard interrupt sequence!'
                break
            except HttpResponseError, e:
                msg = 'HttpResponseError'
                print msg
                with open("log_Error.txt", "a") as log:
                    log.write(msg+"\n")
            except Exception, e:
                msg = 'CatchAllError'
                print msg
		print e
                with open("log_Error.txt", "a") as log:
                    log.write(msg+"\n")

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.stdout.write('\nQuit by keyboard interrupt sequence!')


#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Name: TwitterReport (v.1.0.3)
# About: Uses anon op queue system to report twitter accounts.
# Credit: Based on script from @anonymous247742
#
# Requirements:
# - Python 2.7
# - Python Requests Module (http://stackoverflow.com/questions/17309288/importerror-no-module-named-requests)
# - Splinter (http://splinter.readthedocs.org/en/latest/install.html)
# 
# Usage:  python twitterReport.py -u YOUR_USER_NAME
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
#

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
from datetime import datetime
from splinter.request_handler.status_code import HttpResponseError
import getpass

# Bot Variables
o="opparis"
op_srv="optools.anonops.com"

# Notifies target is offline
def updatetarget(o,t):
    try:
        r = requests.get('http://'+op_srv+'/twUpdateTarget.php?o='+o+'&t='+t)
        r.raise_for_status()
    except HttpResponseError:
        print "OP Server Error"

def main(argv):
    d = datetime.now()
    date = str(d.year) + '' + str(d.month) + '' + str(d.day) + '' + str(d.hour) + '' + str(d.minute) + '' + str(d.second)
    username = None
    try:
        opts, args = getopt.getopt(argv,"h:u:",["user="])
    except getopt.GetoptError:
        print 'Usage: python twitterReport.py -u <Twitter username>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: python twitterReport.py -u <Twitter username>'
            sys.exit()
        elif opt in ("-u", "--user"):
            username = arg
            n = username

    if not username:
        print 'Usage: python twitterReport.py -u <Twitter username>'
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
            browser.visit("https://twitter.com/login/")
            time.sleep(1)
            browser.execute_script("$('.js-username-field').val('%s');"  % (username))
            browser.execute_script("$('.js-password-field').val('%s');" % (password))
            browser.find_by_css("button[type='submit'].submit.btn.primary-btn").click()
            time.sleep(1)

            if "https://twitter.com/login/error" in browser.url:
                print "Twitter Login Failed!"
                sys.exit()

        except:
            print "Unexpected error occured while trying the Twitter login. Please try running the script again."
            sys.exit()

        while True:
            try:
                time.sleep(1)
                # Get target from target queue
                tg = ""
                t = requests.get('http://'+op_srv+'/twGetTarget.php?o='+o+'&n='+n)
                tg = t.content
                if tg == "" or tg == "noassignment" or ("error" in tg) or ("What happened?" in tg) or ("CloudFlare" in tg) or ("Cloudflare" in tg) or ("Checking your browser" in tg):
                    print "No current assignment"
                    time.sleep(3)
                else:
                    browser.visit("https://twitter.com/"+tg)
                    if not browser.is_element_present_by_css('.route-account_suspended') and not browser.is_element_present_by_css('.search-404'):
                        browser.find_by_css('.user-dropdown').click()
                        browser.find_by_css('li.report-text button[type="button"]').click()
                        with browser.get_iframe('new-report-flow-frame') as iframe:
                            iframe.find_by_css("input[type='radio'][value='abuse']").check()
                        browser.find_by_css('.new-report-flow-next-button').click()
                        with browser.get_iframe('new-report-flow-frame') as iframe:
                            iframe.find_by_css("input[type='radio'][value='harassment']").check()
                        browser.find_by_css('.new-report-flow-next-button').click()
                        with browser.get_iframe('new-report-flow-frame') as iframe:
                            iframe.find_by_css("input[type='radio'][value='Someone_else']").check()
                        browser.find_by_css('.new-report-flow-next-button').click()
                        with browser.get_iframe('new-report-flow-frame') as iframe:
                            iframe.find_by_css("input[type='radio'][value='violence']").check()
                        browser.find_by_css('.new-report-flow-next-button').click()
                        try:
                            followers = browser.find_by_css('a[data-nav="followers"] .ProfileNav-value').value;
                        except:
                            followers = ""
                        msg = tg+' - ' + followers + ' Followers'
                    elif browser.is_element_present_by_css('.route-account_suspended'):
                        msg =  tg+' - Suspended'
                        updatetarget(o,tg)
                    elif browser.is_element_present_by_css('.search-404'):
                        msg =  tg+' - Does not exist'
                        updatetarget(o,tg)
                    else:
                        msg = tg+' - Unknown'
                        updatetarget(o,tg)

                    print msg
            except KeyboardInterrupt:
                print 'Quit by keyboard interrupt sequence!'
                break
            except HttpResponseError, e:
                msg = 'HttpResponseError'
                print msg
                with open("log_Error.txt", "a") as log:
                    log.write(msg+"\n")
            except:
                msg = 'CatchAllError'
                print msg
                with open("log_Error.txt", "a") as log:
                    log.write(msg+"\n")

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.stdout.write('\nQuit by keyboard interrupt sequence!')

#!/usr/bin/env python
#-*- coding: utf-8 -*-
#############################################################
#NAME: TR6	// TWITTER AUTOREPORTER 6.0	REBUILD				#
#############################################################

from splinter import Browser
import sys, getopt, re, shutil,os, codecs
from splinter.request_handler.status_code import HttpResponseError
from splinter.element_list import ElementList
import time, datetime

# uncomment if you want to use privoxy + tor        
proxyIP = '127.0.0.1'
proxyPort = 8118

proxy_settings = {'network.proxy.type': 1,
		'network.proxy.http': proxyIP,
		'network.proxy.http_port': proxyPort,
		'network.proxy.ssl': proxyIP,
		'network.proxy.ssl_port':proxyPort,
		'network.proxy.socks': proxyIP,
		'network.proxy.socks_port':proxyPort,
		'network.proxy.ftp': proxyIP,
		'network.proxy.ftp_port':proxyPort 
		}

LOGFILENAME="twitter_report.log"

def logintw(browser, aloginb, username, password ):
	
	time.sleep(5)
	browser.execute_script('document.getElementsByName("session[username_or_email]")[1].value = "'+username+'"')
	browser.execute_script('document.getElementsByName("session[password]")[1].value = "'+password+'"')
	aloginb.click()

def help():
	print 'tr6.py -u <Twitter username> -i <file> -f <y|n> -w <y|n> -r <y|n>'
	print " -f -> harvest followers "
	print " -w -> harvest following "
	print " -t -> harvest twitters "
	print " -r -> report user "
	sys.exit(2)

def report(browser):
	
	try:	
	    browser.find_by_css('.user-dropdown').click()
	    browser.find_by_css('li.report-text button[type="button"]').click()
	except:
	    pass
	time.sleep(2)
	browser.choose('input[type="radio"][value="spam"]').click(1)

def getTwitterData(browser):
	
	contain=[]
	browser.execute_script("$(document).scrollTop($(document).scrollTop()+$(document).height());")
	time.sleep(0.5)
	tweets=browser.find_by_css('.TweetTextSize.TweetTextSize--16px.js-tweet-text.tweet-text')
	tweets+=browser.find_by_css('.TweetTextSize.TweetTextSize--26px.js-tweet-text.tweet-text')
	for tweet in tweets:
	    contain.append(tweet.value)	

	return contain

def goGetTwitters(id, browser):

	browser.visit("https://twitter.com/%s" % (id))
	time.sleep(1)
	last=""
	contents=getTwitterData(browser)
	if len(contents)==0:
	    return False
	while last!=contents[-1][0]:
	    last=contents[-1][0]	
	    contents=getTwitterData(browser)
	
	file=codecs.open("tweets_%s.txt" % id, "wb+", "utf-8")
	for value in contents:
	    file.write('"%s"\n' % (value)  )
	file.close()
	return True
	    

def getProfileData(browser, ldups):
	names=browser.find_by_css('.ProfileNameTruncated-link.u-textInheritColor.js-nav.js-action-profile-name')
	descs=browser.find_by_css('.ProfileCard-bio.u-dir')
	alinks=browser.find_by_css('.ProfileCard-screennameLink.u-linkComplex.js-nav')
	profiles=[]
	for x, y, z in zip(alinks, names, descs):
	    if x["href"] not in ldups:
		profiles.append([x["href"], y.value, z.value])
	    
	return profiles   
	
def goharvest(id, browser, op):
	
	browser.visit("https://twitter.com/%s/%s" % (id, op))
	harvestfname="%s_%s.txt" % (op, id)
	fpath= "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-1])	
	ldups=open("allurls.txt", "rb").readlines()
	browser.execute_script("$(document).scrollTop($(document).scrollTop()+$(document).height());")
	ldups=map(lambda ldup: ldup.strip(), ldups)
	lastfollower=" "	

	links=[]
	try:
   	    time.sleep(2.8)	
	    links+=getProfileData(browser, ldups+map(lambda x: x[0], links))	
	    if len(links)==0:
	        return False
	except:	
	    return False
	else:
	    while lastfollower!=links[-1][0]:	
	        lastfollower=links[-1][0]
	        browser.execute_script("$(document).scrollTop($(document).scrollTop()+$(document).height());")
	        time.sleep(1.4)
	        try:						
		    links+=getProfileData(browser, ldups+map(lambda x: x[0], links))	
		except: 	
		    break
				
	links+=getProfileData(browser, ldups+map(lambda x: x[0], links))
	harvest = codecs.open(harvestfname, "wb+", "utf-8")	
	for link, name, desc in links:
	    harvest.write('"%s","%s","%s"\n' % (link, name, desc))
	harvest.close()
	#os.system("cat %s/followers/%s | unique  %s/analisys/%s  " % (fpath, harvestfname, fpath, harvestfname))
	return True

def getTimestamp():

	return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def logger(msg):

	open(LOGFILENAME, "a+").write("+[%s] %s\n" % ( getTimestamp() , msg))
	print msg
	
def main(argv):
    
    if len(argv)==0:
	help()

    report=hvf=hvw=tuits=False

    try:
        opts, args = getopt.getopt(argv,"hi:u:i:f:w:t:r",["file=","user=","followers=","following=", "tuits=","report="])
    except getopt.GetoptError:
	help()

    for opt, arg in opts:

	if opt == '-h':
	    help()
	elif opt in ("-i", "--file"):
	    txt = arg
	elif opt in ("-u", "--user"):
	    username = arg
	elif opt in ("-f", "--followers") and arg=="y":
	    hvf=True
	elif opt in ("-w", "--following") and arg=="y":
	    hvw=True
	elif opt in ("-t", "--tuits") and arg=="y":
	    tuits=True
	elif opt in ("-r", "--report") and arg=="y":
	    report=True

    try:
	ufile = open(txt, 'rb').readlines()
    except:
	print "Cant open %s" % txt
	sys.exit(0)

    password = raw_input("Enter your twitter password : ")

    browser = Browser( 'firefox' , profile_preferences=proxy_settings )
    browser.visit("https://twitter.com/login/")
	
    if browser.is_element_present_by_value("Log in", wait_time=8):
	aloginb=browser.find_by_xpath('.//button[@type="submit"]')[0]
	logintw(browser, aloginb, username, password)		   
    else:
	print "timeout loading page"
	sys.exit(5)

    for line in ufile:

	try:
	    if re.search("intent", line):	
	        url = re.match(r"https?://(www\.)?twitter\.com/intent/(#!/)?@?([^/\s]*)",line.strip())
	        url = url.group()
		urltypeid=True
	    else:	
	        url = line.strip()
		urltypeid=False	
	    browser.visit(url)
	    time.sleep(1)	
	    if not re.search('suspended', browser.url):
		if urltypeid:
	            browser.find_by_css('a.fn.url.alternate-context').click()
	    else:
		msg =  line.strip() + ' - Suspended'
		logger(msg)
		continue

	    # report user
			
	    msg="  "
			
	    if report:	
	        report(browser)
		msg="RP"

	    id = browser.find_by_css('a.ProfileHeaderCard-screennameLink.u-linkComplex.js-nav')["href"][1:]
	    id = id.split("/")[-1]
	    followers = browser.find_by_css('a[data-nav="followers"] .ProfileNav-value')
	    following = browser.find_by_css('a[data-nav="following"] .ProfileNav-value')	

	    try:
		msg = "%s %s %s %s" % (followers.value, following.value, url.strip(), msg)
	    except:
		msg = " %s %s " % (url.strip(), msg) 	

	    # harvest twitters

	    if tuits:	
		if goGetTwitters(id, browser):
		    msg+=" TW"

	    # harvest followers

	    if hvf:
		if goharvest(id, browser, "followers"):
		    msg+=" FO"
	
	    # harvest following
				
	    if hvw:
		if goharvest(id, browser, "following"):
		    msg+=" FI"

	except KeyboardInterrupt:
	    break
	except HttpResponseError:
	    msg = line.strip()+' - HttpResponseError'
	except:
	    if line:
		msg = line.strip()+' - CatchAllError'
	else:
	    logger(msg)

if __name__ == "__main__":

    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.stdout.write('\n Program stopped!')

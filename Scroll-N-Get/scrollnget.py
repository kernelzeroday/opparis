#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Title: 		Scroll-N-Get
# Description: 	Get following Twitter accounts from input file containing Twitter accounts
# Author: 		Spire <https://github.com/SpireFR>
# Date: 		2015-11-24
# Version: 		0.1
# Notes			I didn't used a lot of exceptions,
#				try to improve the script as you want (tired).
#				Authentication based on: https://github.com/rainthundermoon/opparis/blob/master/twitterreporter.py
# Usage: 		python scrollnget.py -u <TWITTER_USERNAME>

#=================================================================

import sys
import time
import getpass
import argparse
import requests
from splinter import Browser
from bs4 import BeautifulSoup
from urlparse import urlparse

IFILE				    = "./accounts.txt"
OFOLDER					= "./output/"
URI_TWITTER 	  		= "https://twitter.com/"
URI_TWITTER_LOGIN 		= URI_TWITTER + "login/"
URI_TWITTER_LOGIN_ERROR = URI_TWITTER_LOGIN + "error"

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="Twitter username", required=True)
parser.add_argument("-f", "--input-file", help="Input file with Twitter accounts (Default: accounts.txt)")
parser.add_argument("-b", "--browser", help="Choose your browser \"Chrome\" or \"Firefox\" (Default: Firefox)")
args = parser.parse_args()

class User:
	def __init__(self, username, password):
		self.username = username
		self.password = password

	def auth(self):
		with Browser() as browser:
			browser.visit(URI_TWITTER_LOGIN)

			time.sleep(3)

			print "Authenticating..."

			browser.execute_script("$('.js-username-field').val('" + self.username + "');")
			browser.execute_script("$('.js-password-field').val('" + self.password + "');")
			browser.find_by_css("button[type=submit].submit.btn.primary-btn").click()

			if URI_TWITTER_LOGIN_ERROR in browser.url:
				print "[FAIL] Check your Twitter credentials"
			else:
				print "[OK] You are connected!"
				if args.input_file:
					following = Following(browser, args.input_file)
				else:
					following = Following(browser)
				following.run()

class Following:
	def __init__(self, browser, iFile = IFILE):
		self.browser = browser
		self.iFile = str(iFile)
		self.username = ""
		self.followingNumber = 0

	def run(self):
		print "[OK] Getting accounts from " + self.iFile + " file..."

		with open(self.iFile) as accountsFile:
			urls = accountsFile.read().splitlines()

		i = 1
		for url in urls:
			try:
				r = requests.get(url.lower().rstrip())
			except requests.exceptions.RequestException as e:
				print "[FAIL] " + str(e)
				print "Please check " + self.iFile
				sys.exit(1)
			else:
				self.setUsername(url)

				print "[OK] Getting " + self.username + "'s list..."
				self.browser.visit(URI_TWITTER + self.username + "/following")
				time.sleep(1)

				print "[OK] Counting following..."
				self.setFollowingNumber()
				time.sleep(1)

				print "[OK] " + str(self.followingNumber) + " following to read"
				followingFile = open(OFOLDER + self.username + ".txt", "w")

				print "[OK] Reading " + self.username + "'s following..."
				followingReminding = self.followingNumber
				for scrollingNumber in range(0, (self.followingNumber / 18) + 1):
					time.sleep(2.5)
					self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
					followingReminding -= 18
					if followingReminding <= 0:
						followingReminding = 0
					print str(followingReminding) + " following left"

					if followingReminding == 0:
						soup = BeautifulSoup(self.browser.html)
						for a in soup.findAll("a", {"class" : "ProfileCard-screennameLink"}):
							username = a.get("href")[1:]
							followingFile.write(URI_TWITTER + username + "\n")

				followingFile.close()
				print "[OK] Following saved into " + OFOLDER + self.username + ".txt!"

			i += 1

		accountsFile.close()

		time.sleep(2)
		sys.exit(1)

	def setUsername(self, url):
		self.username = urlparse(url).path[1:]

	def setFollowingNumber(self):
		self.followingNumber = int(self.browser.find_by_css(".ProfileNav-item--following .ProfileNav-value").text)

def main():
	user = User(args.username, getpass.getpass())

	user.auth()

if __name__ == "__main__":
	main()
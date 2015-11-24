#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#whiteVillain

#Requires Python 2 with tweepy module installed 
#Try pip install tweepy if not installed OR apt-get install python-tweepy

#####!!H O W  T O  U S E !!#####                  

#1: Obtain Twitter dev keys (https://dev.twitter.com/oauth/overview/application-owner-access-tokens) and enter them into script

#2: Scroll down and enter your keywords at the bottom of the script (Be sure to use correct formatting for unicode)

#3: Save the script once keys and keywords have been added

#4: Populate a target list by running: python twitterSnatch.py > twitterData.json

#5: You can quit the script by closing it at any time. The longer it runs, the more targets it will acquire

#6: After this script has been terminated you will have a target file named twitterData.json

#7: Simply run the userScrape.py script and it will scrape the targets into a text file named screenNames.txt to check for nefarious activity later on


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


#################################################################
#You need to have a twitter account and enter your dev keys here#
#################################################################
access_token = "Obtain keys @ https://dev.twitter.com/oauth/overview/application-owner-access-tokens"
access_token_secret = "Obtain keys @ https://dev.twitter.com/oauth/overview/application-owner-access-tokens"
consumer_key = "Obtain keys @ https://dev.twitter.com/oauth/overview/application-owner-access-tokens"
consumer_secret = "Obtain keys @ https://dev.twitter.com/oauth/overview/application-owner-access-tokens"

class StdOutListener(StreamListener):

	def on_data(self, data):
		print (data)
		return True

	def on_error(self, status):
		print (status)


#Authentication
listener = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, listener)

#Keywords to search for (The letter u before the term keeps it from throwing errors)
#You may add more keywords with slight modification Ex. keyword4 = u'whatever' then add keyword4 into the last line of the script

keyword1 = u'jeszcze'
keyword2 = u'koty'
keyword3 = u'Prosz?'

stream.filter(track=[keyword1, keyword2, keyword3])

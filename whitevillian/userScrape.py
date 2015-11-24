#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#whiteVillain

import json

def main():

	#Reading Tweets
	print '******************************************'
	print '*Check ScreenNames.txt for username links*'
	print '******************************************'
	tweetsDataPath = 'twitterData.json'

	tweetsData = []
	tweetsFile = open(tweetsDataPath, "r")
	for line in tweetsFile:
		try:
			tweet = json.loads(line)
			tweetsData.append(tweet)
		except:
			continue

	output = open("screenNames.txt", "w")

	for tweet in tweetsData:
		dropLevel = tweet[u'user']
		output.write (("http://www.twitter.com/")+(dropLevel[u'screen_name']))
		output.write ('\n')


	

if __name__=='__main__':
	main()

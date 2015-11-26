#python script that takes in a list of urls and prints out if they are behind cloud flare 

#file name: detect-cf.py
#useage: python detect-cf.py list_of_urls.txt
#notes: one url per line in the text file

import requests
import sys
f = sys.argv[1]
urls = open(f, 'r')
print "(url): CloudFlare?"
for u in urls.readlines():
	u = u.rstrip()
	try:
		r = requests.get(u, verify=False)
	except:
		print "("+u+"): error"
	try:
		if("<title>Attention Required! | CloudFlare</title>" in str(r.text)):
			print "("+u+"): yes"
		else:
			print "("+u+"): no"
	except:
		print "("+u+"): error"

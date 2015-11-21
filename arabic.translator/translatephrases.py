#!/usr/bin/python
import phrases2 as phr
import requests
import json, codecs, sys, urllib

k=0
f=codecs.open("phrasesis.py", "wb+", "utf-8")
for word in phr.a:
	url="http://api.mymemory.translated.net/get?q=%s&langpair=en|ara" %  urllib.quote(word)
	r=requests.get(url)
	if r.status_code == 200:
		a=json.loads(r.content)
		code= "a.append(u'%s\n')" % a["responseData"]["translatedText"]   	
		f.write(code)
		k+=1
		print "\r%d\r" % k,
		sys.stdout.flush()
f.close()
print "done."


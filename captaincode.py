#Written by https://twitter.com/captainc0de
#Licence: You are not allowed to ... FUCK OFF, Do what ya want with it
#For those who cant script Python: you need a file in same dictionary like this python named "list.txt". In this file should be some thousands of twitteruserlinks
#Here you can get some accounts. http://pastebin.com/836HPrnn   http://pastebin.com/6WXhFh00     http://pastebin.com/j0RYNvDq
#OpISIS

import urllib2
f = open('list.txt')
exist = open('exist.txt','a+')
sus = open('suspendet.txt','a+')
deleted = open('deleted.txt','a+')

def checkonline(url):
    url = url.replace("\n", "")
    response = urllib2.urlopen(url)
    html = response.read()
    if "Account suspended" in html:
        print "Suspendet: " + url
        sus.write(url + "\n")
    if "Sorry, that page" in html:
        print "Deleted: " + url
        deleted.write(url + "\n")
    if not "Account suspended" in html and not "Sorry, that page " in html:
        print "Exist: " + url
        exist.write(url + "\n")

for line in iter(f):
    try:
        checkonline(line)
    except:
        print "Ups"
        sus.write(line)
        pass
f.close()

exist.close()
sus.close()
deleted.close()

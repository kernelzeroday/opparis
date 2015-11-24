#Fuck ISIS
 
#We are Anonymous. We are Legion. We do not forgive. We do not forget. Expect us
#Title: Twitter follower scanner
#Details:It is a script to generate a list of the targets followers
#Author: codezero
#Version: 0.02 BETA

import requests
from bs4 import BeautifulSoup
i=0

followers = 'followers.txt'

ffollowers = open(followers,'w')



user = "myconfusedface";

def getlink(username,pageid):

    if pageid == "null":
        page = requests.get("https://mobile.twitter.com/"+username+"/followers")
    else:
	page = requests.get("https://mobile.twitter.com/"+username+"/followers?cursor="+pageid)

    soup = BeautifulSoup(page.content, 'html.parser')
    getfollowers(soup)
    link = soup.find("a", string="Show more people")
    if not link:
        return "End"
    link = str(link)
    link = link.split('r=')
    link = link[1].split('\">')
    return link[0]

def getfollowers(soup):
    #print(soup)
    username = soup.find_all("span", class_="username")
    for username in username:
        username = str(username)
        username = username.split('</span>')
        username = username[1]
        #print(username)
        ffollowers.write(username+"\n")
    return 0


pid = getlink(user,"null")
try:
    while 1:
        i +=1
        print("Page " + str(i))
        pid = getlink(user,pid)
        if pid == "End":
            ffollowers.close()
            break
except KeyboardInterrupt:
    print 'interrupted!'

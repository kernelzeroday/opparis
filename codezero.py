#Fuck ISIS
 
#We are Anonymous. We are Legion. We do not forgive. We do not forget. Expect us
#Details:It is a script to scan a list for for banned and active twitter accounts
#Author: codezero
#Version: 0.07
import urllib2
import httplib

#The string-key to look for banned account page
stringbanned = "<title>Twitter / Account Suspended</title>"
#The string-key to look for active account page
stringactive = "<meta name=\"description\" content=\"The latest Tweets from"

#The list with the twitter accounts one per line
inlist = "list.txt"
#The file where the banned account are saved
listbanned = "banned.txt"
#The file where the active account are saved
listactive = "active.txt"
#The file where error logs are saved
listerror = "errorlog.txt"

i = 0
iban = 0
iactive = 0
ierror = 0

fban = open(listbanned,'w')
factive = open(listactive,'w')
ferror = open(listerror,'w')

with open(inlist, "r") as ins:
    array = []
    for line in ins:
	i += 1
	print(i)
        url = line
	#Some error handling
	try: 
   	    html = urllib2.urlopen(url).read()
	except urllib2.HTTPError, e:
    	    print('HTTPError = ' + str(e.code) +" "+url)
	    ferror.write('HTTPError = ' + str(e.code) +" "+url)
	    ierror += 1
	except urllib2.URLError, e:
    	    print('URLError = ' + str(e.reason) +" "+url)
	    ferror.write('URLError = ' + str(e.reason) +" "+url)
	    ierror += 1
	except httplib.HTTPException, e:
    	    print('HTTPException' +" "+url)
	    ferror.write('HTTPException' +" "+url)
	    ierror += 1
	except (KeyboardInterrupt, SystemExit):
            raise
	except:
 	    print("Something weird happened" +" "+url)
	    ferror.write("Something weird happened" +" "+url)
	    ierror += 1


	if stringbanned in html:
	    fban.write(url)
            iban += 1
        elif stringactive in html:
	    factive.write(url)
	    iactive += 1
	else:
	    ferror.write('Error = doesnt looks like a twitter profile '+ url)
	    ierror += 1



print("Scanned "+str(i)+" link(s) "+str(iban)+" banned profile(s) "+str(iactive)+" active profile(s) and got "+str(ierror)+" error(s)")

fban.close()
factive.close()
ferror.close()

###############################################################################
# Twitter Hashtag Scanner
#
# Project: #OpParis
#
# Author: synxe
# Start Date: 11/22/2015
# Last Updates: 11/22/2015
#
# Version: 0.2
#
# Requirements:
#     Python 2.7
#
# Usage:
#     python TwitterHashtagScanner.py <name of list of hashtags>
#
# Given a list of common hashtags, will scan and store handles using each.
###############################################################################

import sys
import urllib2
import re

def main(argv):
    baseURL = 'https://www.twitter.com/search?q=%23'

    try:
        hashtagList = open(argv[0], 'r')
    except IOError:
        print("%s is not a valid file...closing." % argv[0])
        exit(1)
        
    hashtags = hashtagList.read().split('\n')
    handlePattern = re.compile(r'@<\/s><b>\w+')
    reductionPattern = re.compile(r'<\/?[^>]>')

    for tag in hashtags:
        searchURL = baseURL + tag[1:]
        page = urllib2.urlopen(searchURL)
        source = page.read()
        for result in re.findall(handlePattern, source):
            if result not in handles:
                print(re.sub(reductionPattern, '', result))
                
        page.close()

    hashtagList.close()



if __name__ == "__main__":
    main(sys.argv[1:])


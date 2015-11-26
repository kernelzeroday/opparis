#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Isis Web Spider does a scan of websites and check if the given strings exists on
#
# Example: ./isiswebspider.py -t targets.txt -s strings.txt -o output.txt -p 1
# Options:
#  -t the file where are written the targets's URL (one url by line)
#  -s the file where are written the strings to search on the websites
#  -o [optional] The output file to write the results. If not given, results
#     will be written in the Terminal
#  -p [optional] To use propagation. By default, during a website scan only the
#     links in the same website are checked. With the propagation, other websites
#     can be added. In order to the program do not works infinitely, the propagation
#     is a number. It means the number of times where isiswebspider will add others
#     websites if it find it.

# Note than Isis Web Spider DO NOT HIDE YOUR IP ADRESS. If you want to hide it,
# use Tor or a VPN
#To execute a search throught Tor you need Tor installed on your PC, with
# torify command. Example:
# torify ./isiswebspider.py -t target.txt -s strings.txt -o output.txt
#
# To use cv2 install openCV: sudo apt-get install python-opencv
# Tu use bs4 install BeautifulSoup: sudo apt-get install python-bs4
# Developped with Python 2.7
# See on Github: https://github.com/passnger/isis-web-spider

import requests
import sys
#import flagfinder
import re
from bs4 import BeautifulSoup





def explain ():
    """Explain how to use the program"""

    print("""
    Isis Web Spider\n

    Isis Web Spider take some parameters:
    ./isis-web-spider -t targets.txt -s strings.txt [-o output.txt]
    Note that each file must contain one information by line
     """)

def getArg (argv, option):
    """Get an argument according to its option

    The program is executed with arguments, the option is specified,
    followed by its value

    argv -- A list that contains every arguments
    option -- The wanted option
    """
    i = 0
    ret = ""
    #Look over every arguments in order to find the option's value
    while i < len(argv):
        #If the option is find, try to return its value
        if (argv[i] == option):
            try:
                ret = argv[i+1]
            except Exception as e:
                print("I think you have not said the value after " + value)
                explain()
        i+=1
    if ret == "":
        raise Exception("Option " + option + " not found")
    return ret



def getFileContent(fileName):
    """Open a file and return a list that contains every line
    fileName -- The file's name
    return a list that contains every line
    """
    with open(fileName, "r") as targets:
        lines = targets.readlines()
        i = 0
        #Remove the \n
        for line in lines:
            lines[i] = line.rstrip()
            i += 1
        return lines

def export(fileName, result):
    """Export the result into a file
    result -- The result string
    fileName -- The output file
    """
    with open(fileName, 'a') as output:
        output.write(result)




def listToDict(listElem):
    """Take a list and return a dict with every value at 0
    listElem -- a list to convert to dict
    return a dict that contains every listElem's element as key and with value
    set to 0
    """
    res = dict()
    for elem in listElem:
        res[elem] = 0
    return res

def getExtension(link):
    """Get the link extension
    link -- the link
    return The extension (e.g: ".jpg")
    """
    if re.match('.*(?P<e>\..*)/?$', link) is not None:
        e = re.search('.*(?P<e>\..*)/?$', link).group('e')
        return e.replace('/', '')
    return ""


def getDomainName(string):
    """Get the domain name from a URL
    string -- the URL
    return the website's domain
    """
    if re.match('(?P<d>^http(s)?://([a-z0-9\-.]+)\.[a-z0-9]+)', string) is not None:
        d = re.search('(?P<d>^http(s)?://([a-z0-9\-.]+)\.[a-z0-9]+)', string).group('d')
        d += "/"
        return d
    return ""

def createCompleteLink(link, domain):
    """Take a link and create the full link
    link -- The link
    domain -- The website's domain
    return the full link
    Example: link = mylink.html and domain = http://mywebsite.com/
    The return will be http://mywebsite.com/mylink.html
    """
    if link is not None and len(link) > 0:
        if re.match('^http', link) is not None:
            return link
        else:
            #Remove the first / to avoid //
            if link[0] == '/':
                link = link[1:]
            return domain + link
    return domain

def checkPage(url, strings):
    """Check if some strings exists in a web page and get the links and imgs
    url -- the page's URL
    strings -- a list that contains the strings to research
    return tuple that contains :
      - a dict string => count of view
      - a set of link found of the page
      - a set of pictures found of the page
    """
    domain = getDomainName(url)
    f = requests.get(url)
    html = ""
    links = list()
    imgs = list()
    dStrings = listToDict(strings)
    #Look over every line, add text into html var
    #and search strings
    for line in f:
        #...Check each string
        for string in strings:
            #Ignoring the lower or uppercase
            if string.lower() in line.lower():
                dStrings[string] += 1
        html += line

    soup = BeautifulSoup(html)

    for a in soup.find_all("a"):
        links.append(createCompleteLink(a.get('href'), domain))

    for img in soup.find_all('img'):
        imgs.append(createCompleteLink(img.get('src'), domain))

    return (dStrings, set(links), set(imgs))


def checkSite(url, strings, output):
    """Check every page of a given site
    url -- The website's URL
    strings -- The list of strings to research
    output -- The output file, can be ""
    return a tuple that contains:
      - A text that explains the website's statistics
      - A set that contains the links that are on an other domain
      - A set that contains all the viewed links
    """

    domain = getDomainName(url)
    otherLinks = list()
    txt = "\n=================================\n"
    txt += "Domain: " + domain + "\n"
    txt += "=================================\n"
    linksViewed = set()
    dStrings = dict()
    imgs = set([])
    links = set([url])
    forbidden = [".ogg", ".tex", ".pdf", ".mp3", "mp4", ".ods", ".xls", ".xlsx",\
     ".doc", ".docx", ".zip", ".tar", ".gz", ".ggb", ".cls", ".sty", ".avi", ".flv"\
     ".mkv", ".srt"]
    #While we have not check all URL
    while links - linksViewed != set([]):
        #Check all links (not already viewed) for this page
        for link in links - linksViewed:
            #If the domains are the same, the extension is not forbidden
            if getDomainName(link) == domain and getExtension(link) not in forbidden:
                print "Checking on " + link + "...\n"
                dStringst, linkst, imgst = checkPage(link, strings)
                txt += link + ":\n"
                for key, value in dStringst.items():
                    txt += "\t" + key + " -> " + str(value) + "\n"
                txt += "\n"
                #Clear list of forbidden extentions
                tmp = list()
                for l in linkst:
                    if getDomainName(l) == domain and getExtension(l) not in forbidden:
                        tmp.append(l)
                    #If the extension is allowed but the link is on an other domain
                    elif getDomainName(l) != domain and getExtension(l) not in forbidden:
                        otherLinks.append(l)
                linkst = set(tmp)
                links = links | linkst
                imgs = imgs | imgst
                #Update link count
                for key, value in dStringst.items():
                    dStrings[key] = dStrings[key] + value if key in dStrings.keys() else 0

                linksViewed = linksViewed | set([link])

        links = set(links)
        imgs = set(imgs)

    #Export/print after each website, in order to do not lost all if user
    #stops the program with Ctrl+C
    if len(output) > 0:
        export(output, txt)
    else:
        print txt
    return txt, set(otherLinks), linksViewed




def checkTargets(targets, strings, propagation, output):
    """Check every target to find given strings
    targets -- The URLs list
    strings -- The list of strings
    output -- The output file, can be ""
    """
    result = ""
    #Do not check an URL twice
    #Here, two different pages on the same target can be checked
    #This is because a page can be "alone" on a website
    targetViewed = set([])
    for url in targets:
        if url not in targetViewed:
            string, otherLinks, linksViewed = checkSite(url, strings, output)
            result += string
            result += "\n"
            targetViewed = targetViewed | set([url])

            #If user want use propagation, add other links to the targets
            if propagation > 0:
                targets += list(otherLinks)
                propagation -= 1
            #Add all viewed links in targetViewed in order to do not check
            #twice the same URL
            targetViewed = targetViewed | linksViewed
    return result





def main():
    """The main method"""

    output = ""
    propagation = 0

    try:
        output = getArg(sys.argv, '-o')
    except Exception as e:
        output = ""

    try:
        propagation =int(getArg(sys.argv, '-p'))
    except Exception as e:
        propagation = 0

    try:
        stringsFileName = getArg(sys.argv, '-s')
        targetFileName = getArg(sys.argv, '-t')
        targets = getFileContent(targetFileName)
        strings = getFileContent(stringsFileName)
        checkTargets(targets, strings, propagation, output)

    except Exception as e:
        message = e.args[0]
        print(message)
        explain()
    except KeyboardInterrupt:
        if len(output) > 0:
            r = 'The current website has been lost, but the previous (if there '
            r += 'is at least one previous) are saved in ' + output
            print r
        print "Bye"
main()

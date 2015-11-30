#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Isis Web Spider does a scan of websites and check if the given strings exists on
#
# Example: ./isiswebspider.py -t targets.txt -s strings.txt -o output.txt -p 1 -i images/
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
#  -i [optional] The folder where the pictures will be downloaded to checked them
#     This folder has to exist

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

from bs4 import BeautifulSoup
import flagfinder
import os
import re
import requests
import sys
import urllib




def explain ():
    """Explain how to use the program"""

    print("""
    Isis Web Spider\n

    Isis Web Spider take some parameters:
    ./isis-web-spider -t targets.txt -s strings.txt [-o output.txt]
    Note that each file must contain one information by line
     """)

def get_arg (argv, option):
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



def get_file_content(file_name):
    """Open a file and return a list that contains every line
    file_name -- The file's name
    return a list that contains every line
    """
    with open(file_name, "r") as targets:
        lines = targets.readlines()
        i = 0
        #Remove the \n
        for line in lines:
            lines[i] = line.rstrip()
            i += 1
        return lines

def export(file_name, result):
    """Export the result into a file
    result -- The result string
    file_name -- The output file
    """
    with open(file_name, 'a') as output:
        output.write(result)


def download_img(img_url, out_folder=""):
    """Download an image and return its outpath"""
    file_name = img_url.split("/")[-1]
    outpath = os.path.join(out_folder, file_name)
    urllib.urlretrieve(img_url, outpath)
    return outpath


def list_to_dict(list_elem):
    """Take a list and return a dict with every value at 0
    list_elem -- a list to convert to dict
    return a dict that contains every list_elem's element as key and with value
    set to 0
    """
    res = dict()
    for elem in list_elem:
        res[elem] = 0
    return res

def get_extension(link):
    """Get the link extension
    link -- the link
    return The extension (e.g: ".jpg")
    """
    if re.match('.*(?P<e>\..*)/?$', link) is not None:
        e = re.search('.*(?P<e>\..*)/?$', link).group('e')
        return e.replace('/', '')
    return ""


def get_domain_name(string):
    """Get the domain name from a URL
    string -- the URL
    return the website's domain
    """
    if re.match('(?P<d>^http(s)?://([a-z0-9\-.]+)\.[a-z0-9]+)', string) is not None:
        d = re.search('(?P<d>^http(s)?://([a-z0-9\-.]+)\.[a-z0-9]+)', string).group('d')
        d += "/"
        return d
    return ""

def create_complete_link(link, domain):
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

def check_page(url, strings):
    """Check if some strings exists in a web page and get the links and imgs
    url -- the page's URL
    strings -- a list that contains the strings to research
    return tuple that contains :
      - a dict string => count of view
      - a set of link found of the page
      - a set of pictures found of the page
    """
    try:
        domain = get_domain_name(url)
        f = requests.get(url)
        html = ""
        links = list()
        imgs = list()
        dstrings = list_to_dict(strings)
        #Look over every line, add text into html var
        #and search strings
        for line in f:
            #...Check each string
            for string in strings:
                #Ignoring the lower or uppercase
                if string.lower() in line.lower():
                    dstrings[string] += 1
            html += line

        soup = BeautifulSoup(html)

        for a in soup.find_all("a"):
            links.append(create_complete_link(a.get('href'), domain))

        for img in soup.find_all('img'):
            full_url = create_complete_link(img.get('src'), domain)
            imgs.append(full_url)

        return (dstrings, set(links), set(imgs))
    except Exception as e:
        print "Failed to load " + url + "\n"
        return (dict(), set([]), set([]))


def check_site(url, strings, output, cascade, images_folder):
    """Check every page of a given site
    url -- The website's URL
    strings -- The list of strings to research
    output -- The output file, can be ""
    images_folder -- The folder where will be downloaded the pictures
    return a tuple that contains:
      - A text that explains the website's statistics
      - A set that contains the links that are on an other domain
      - A set that contains all the viewed links
    """
    allowed_imgs = ['.png', '.jpg', '.jpeg']
    domain = get_domain_name(url)
    otherLinks = list()
    txt = "\n=================================\n"
    txt += "Domain: " + domain + "\n"
    txt += "=================================\n"
    viewed_links = set()
    dstrings = dict()
    imgs = set([])
    links = set([url])
    forbidden = [".ogg", ".tex", ".pdf", ".mp3", "mp4", ".ods", ".xls", ".xlsx",\
     ".doc", ".docx", ".zip", ".tar", ".gz", ".ggb", ".cls", ".sty", ".avi", ".flv"\
     ".mkv", ".srt", ".css", '.rar', '.png', '.jpg', '.gif', '.ttf', '.jpeg', ".sh", '.exe'\
     '.msi', '.wmw']
    #While we have not check all URL
    while links - viewed_links != set([]):
        #Check all links (not already viewed) for this page
        for link in links - viewed_links:
            #If the domains are the same, the extension is not forbidden
            if get_domain_name(link) == domain and get_extension(link) not in forbidden:
                print "Checking on " + link + "...\n"
                dstringst, linkst, imgst = check_page(link, strings)
                txt += link + ":\n"
                for key, value in dstringst.items():
                    txt += "\t" + key + " -> " + str(value) + "\n"
                txt += "\n"
                #Clear list of forbidden extentions
                tmp = list()
                for l in linkst:
                    if get_domain_name(l) == domain and get_extension(l) not in forbidden:
                        tmp.append(l)
                    #If the extension is allowed but the link is on an other domain
                    elif get_domain_name(l) != domain and get_extension(l) not in forbidden:
                        otherLinks.append(l)
                #Update link count
                for key, value in dstringst.items():
                    dstrings[key] = dstrings[key] + value if key in dstrings.keys() else 0
                #Download and check imgs to find isis flag
                for img in imgst - imgs:
                    if get_extension(img) in allowed_imgs:
                        try:
                            img_path = download_img(img, images_folder)
                            if flagfinder.find_flag(img_path, cascade):
                                txt += "AN ISIS FLAG MIGHT BE ON THIS PAGE\n"
                            os.remove(img_path)
                        except Exception as e:
                            print "An image ("+ img +") can't be downloaded\n"
                linkst = set(tmp)
                links = links | linkst
                imgs = imgs | imgst
                viewed_links = viewed_links | set([link])

        links = set(links)
        imgs = set(imgs)

    #Export/print after each website, in order to do not lost all if user
    #stops the program with Ctrl+C
    if len(output) > 0:
        export(output, txt)
    else:
        print txt
    return txt, set(otherLinks), viewed_links




def check_targets(targets, strings, propagation, output,images_folder):
    """Check every target to find given strings
    targets -- The URLs list
    strings -- The list of strings
    output -- The output file, can be ""
    images_folder -- The folder where will be downloaded the pictures
    """
    cascade = flagfinder.loadCascadeFile()
    result = ""
    #Do not check an URL twice
    #Here, two different pages on the same target can be checked
    #This is because a page can be "alone" on a website
    viewed_target = set([])
    for url in targets:
        if url not in viewed_target:
            string, otherLinks, viewed_links = check_site(url, strings, output, cascade, images_folder)
            result += string
            result += "\n"
            viewed_target = viewed_target | set([url])

            #If user want use propagation, add other links to the targets
            if propagation > 0:
                targets += list(otherLinks)
                propagation -= 1
            #Add all viewed links in viewed_target in order to do not check
            #twice the same URL
            viewed_target = viewed_target | viewed_links
    return result





def main():
    """The main method"""

    output = ""
    propagation = 0
    images_folder = ""

    try:
        output = get_arg(sys.argv, '-o')
    except Exception as e:
        output = ""

    try:
        images_folder = get_arg(sys.argv, '-i')
    except Exception as e:
        images_folder = ""

    try:
        propagation =int(get_arg(sys.argv, '-p'))
    except Exception as e:
        propagation = 0

    try:
        stringsfile_name = get_arg(sys.argv, '-s')
        targetfile_name = get_arg(sys.argv, '-t')
        targets = get_file_content(targetfile_name)
        strings = get_file_content(stringsfile_name)
        check_targets(targets, strings, propagation, output, images_folder)

    except Exception as e:
        message = e.args[0]
        print(message)
        explain()
    except KeyboardInterrupt:
        if len(output) > 0:
            r = 'The current website has been lost, but the previous (if there '
            r += 'is at least one previous) are saved in ' + output + "\n"
            r += 'Some pictures may stay in ' + images_folder + ", you should delete them"
            print r
        print "Bye"
main()

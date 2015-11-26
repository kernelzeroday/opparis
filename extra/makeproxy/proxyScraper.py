
import urllib2,threading,re
from bs4 import BeautifulSoup

class URLOpener(threading.Thread):
    responsePage = ''
    proxyList = ''
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
    def run(self):
        # Open the page, find the needed span, and perform manipulations
        # to extract only the paragraph with the proxies
        self.responsePage = BeautifulSoup(urllib2.urlopen(self.url).read(), 'lxml')
        temp = self.responsePage.find('div', 'entry-content').find_all('span')
        proxies = ''
        for span in temp:
            spanStr = str(span)
            match = re.search("(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])", spanStr)
            if match:
                end = spanStr.find('</span>');
                spanStr = spanStr[match.start():end]
                proxies += spanStr
        self.proxyList = proxies
    def returnResponse(self):
        return self.proxyList
    
class ProxyScraper():
    #Scrapes SOCKS5 proxy from the given URLS

    _URLS = ('http://www.socks5list.com/', 'http://www.socks24.org/')
    _responsePages = []
    _proxies = { 'socks5' : [], 'socks4' : [], 'mixedSocks' : [] }
    def __init__(self):
        self.scrapePages()
        self.handleSocks5()
        self.handleSocks24()
    def scrapePages(self):
        # scrape the pages and put it through parsers
        self._responsePages.append(urllib2.urlopen(self._URLS[0]).read())
        self._responsePages.append(urllib2.urlopen(self._URLS[1]).read())
        self._responsePages[0] = BeautifulSoup(self._responsePages[0], 'lxml')
        self._responsePages[1] = BeautifulSoup(self._responsePages[1], 'lxml')
    def handleSocks5(self):
        textarea = []
        textareas = self._responsePages[0].find_all('textarea')
        for text in textareas:
            textarea.append(text.get_text())
        self.separateProxies(textarea)
    def handleSocks24(self):
        links = self.getLinks()
        threads = []
        content = []
        for link in links:
            thread = URLOpener(link)
            thread.daemon = True
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
            content.append(thread.returnResponse())
        for proxyList in content:
            self._proxies['mixedSocks'].append(self.extractProxies(proxyList))
            
    def getLinks(self):
        links = self._responsePages[1].find_all('a')
        temp = []
        for item in links:
            string =  str(item)
            if string.find('Read more') != -1:
                firstQ = string.find('"') +1
                secQ = string[firstQ:].find('"')
                string = string[firstQ:secQ + firstQ]
                temp.append(string)
        return temp
    def extractProxies(self,text, begin = False, end = False):  
        if begin:
            # For _socks5 handling  
            temp = text[begin:end] # extract JUST the proxy list
        else:
            temp = text
        temp = temp.split('\n') # split proxies into array
        i = 0
        while i < len(temp):
            if len(temp[i]) < 2:
                del temp[i]
                continue
            spacePos = temp[i].find(' ')
            if spacePos != -1:
                temp[i] = temp[i][:spacePos]
            temp[i] = temp[i].split(':')
            i+=1
        return temp
    def getProxies(self):
        return self._proxies
    def separateProxies(self, textareas):
        for text in textareas:
            beginPosition = text.find(']') + 1
            endPosition = text.find('Published by')
            if text.find('Socks 5 List') != -1:
                # socks 5 proxy
                self._proxies['socks5'].append(self.extractProxies(text, beginPosition, endPosition))
            else:
                self._proxies['socks4'].append(self.extractProxies(text, beginPosition, endPosition))

class ListHandler():
    
    _proxies = { 'socks5' : [], 'socks4' : [], 'mixedSocks' : [], 'http' : [], 
                'unknown': [] }
    
    def __init__(self, lst, pType):
        self._LIST = lst
        self._TYPE = pType
        self.readFile()
    def readFile(self):
        filedesc = open(self._LIST, 'r')
        for line in filedesc.readlines():
            if line.find(':') != -1:
                self._proxies[self._TYPE].append(line.strip().split(':'))
    def getProxies(self):
        return self._proxies
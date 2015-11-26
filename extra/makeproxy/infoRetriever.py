
import mechanize
from bs4 import BeautifulSoup
class InfoRetriever():
    # Retrieves info about the proxy
    
    _URL = 'http://www.iplocation.net'
    _parsedPage = ''
    _info = ''
    def __init__(self, IP):
        self._IP = IP
        self.getPage()
        self.submitRequest()
        self.extractInfo()
    def getPage(self):
        self._browser = mechanize.Browser()
        try:
            self._browser.open(self._URL)
        except:
            raise Exception('The locator is down')
    def submitRequest(self):
        self._browser.select_form(name = 'lookup')
        self._browser.form['query'] = self._IP
        self._browser.submit()
        self._parsedPage = BeautifulSoup(self._browser.response().read(), 'lxml')
        
        # Done with the browser, can close it and delete the variable
        self._browser.close()
        del self._browser
    def extractInfo(self):
        table =  self._parsedPage.find_all('table')[5].find_all('div')[0]
        table = table.find_all('div')[2].find('a')
        strTable = str(table.contents)
        begin = len("[u'Google Map for ")
        end = strTable.find(' (New window)')
        self._info = strTable[begin:end]
    def getInfo(self):
        return self._info

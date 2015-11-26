
import pycurl,threading,Queue,StringIO,time
from proxyScraper import ProxyScraper,ListHandler
from infoRetriever import InfoRetriever
from termcolor import colored
from setuptools.command import easy_install

class ImportsChecker():
    _MODULES = ('pycurl', 'threading', 'Queue', 'StringIO', 'time', 'termcolor', 'mechanize', 'bs4', 're',
                'urllib2')
    def __init__(self):
        self.checkModules()
        print colored('[%s] [+] All necessary modules are installed' % time.strftime('%H:%M:%S'), 'green')
    def checkModules(self):
        for module in self._MODULES:
            try:
                __import__(module)
            except ImportError:
                print colored('[%s] %s module not found, trying to install it' % (time.strftime('%H:%M:%S'), module), 'yellow')
                self.installModule(module)
    def installModule(self, module):
        try:
            easy_install.main([module])
        except:
            print colored('''[%s] [-] Error installing %s module. Possibly setuptools module is not installed.
            Please visit https://pypi.python.org/pypi/setuptools to download setuptools, and try again.
            Exiting...''' % (time.strftime('%H:%M:%S'), module), 'red')
            exit()
        else:
            print colored('[%s] [+] %s module has been sucessfully installed' %(time.strftime('%H:%M:%S'), module), 'green')
class ProxyTestWorker(threading.Thread):
    # threads that will test a given proxy
        _TEST_URLS = ('http://www.socks5list.com/', 'https://www.google.com/search?q=hello+world&ie=utf-8&oe=utf-8')
        _FILEDESC = None
        def __init__(self, queue, proxyType, flag, fd, userGiven):
            threading.Thread.__init__(self)
            self.queue = queue
            self.proxyType = proxyType
            self._FLAG = flag
            self._FILEDESC = fd
            self._uG = userGiven
        def run(self):
            curl = pycurl.Curl()
            # buffer makes the curl.perform() output not to get printed directly on the screen
            buffer = StringIO.StringIO()
            curl.setopt(pycurl.WRITEFUNCTION, buffer.write)
            if self.proxyType == 'socks4':
                curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS4)
            elif self.proxyType == 'socks5':
                curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
            elif self.proxyType == 'http':
                curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_HTTP)
            elif self.proxyType == 'mixedSocks':
                pass
            elif self.proxyType == 'unknown':
                pass
            else:
                print colored('[%s] [-] Unidentified proxy type' % time.strftime('%H:%M:%S'), 'red')
                
                # Weird but that's the only way I could get the Queue out of the
                # way in case proxy type is wrong
                proxy = self.queue.get()
                self.queue.task_done()
                exit()
            self.checkURL(curl)
            
        def checkURL(self, curl):
            while not self.queue.empty():
                proxy = self.queue.get()

                if not self._FLAG or self._FLAG == 'testOnly':

                    #check for regular URL
                    curl.setopt(pycurl.URL, self._TEST_URLS[0])
                    curl.setopt(pycurl.PROXY, str(proxy[0]))
                    curl.setopt(pycurl.PROXYPORT, int(proxy[1]))
                    curl.setopt(pycurl.HTTPHEADER, ["User-agent: Mozilla/5.0 (X11; Linux i686 on x86_64; rv:14.0) Gecko/20100101 Firefox/14.0.1"])
                    curl.setopt(pycurl.TIMEOUT, 30) # had to set default loading time to 30 seconds, because otherwise it takes forever
                    if self.proxyType == 'mixedSocks' or self.proxyType == 'unknown':
                        curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
                        
                    #retries 3 times, if fails the previous times
                    counter = 0
                    tryingHTTP = False;
                    while counter < 3:
                        counter+=1
                        try:
                            curl.perform()
                        except pycurl.error, error:
                            # Before going into that fucking maze, let's handle the case where user given 
                            # SOCKS proxies actually fail. (HTTP proxies and scraped proxies are 
                            # handled below
                                                        
                            if counter == 3 and self._uG and (self.proxyType == 'socks4' or self.proxyType == 'socks5'):                               
                                err = '%s:%s is not working...'%(str(proxy[0]), str(proxy[1]))
                                self.printOutput(err, 'red')
                                self.writeToFile(err)
                            
                            
                            # if the proxies are mixed and it failed 3 times with the SOCKS4 type,
                            # it will retry 3 times with the SOCKS5 type
                            
                            if counter == 3 and (self.proxyType == 'mixedSocks' or self.proxyType == 'unknown'):
                                # The way it works here, is that if a proxy type is mixedSocks, it tries
                                # SOCKS4 (since SOCKS5 already failed), and changes the type to SOCKS4, so the
                                # next time, it wouldn't set off the flag.
                                # If proxy is unknown, it will remain as unknown throughout the SOCKS checking,
                                # but if it doesn't show positive for SOCKS4, proxy type will be set to HTTP
                                
                                curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS4)
                                self.proxyType = 'socks4' if self.proxyType == 'mixedSocks' else 'unknown'
                                counter = 0
                                if tryingHTTP:
                                    self.proxyType = 'http'
                                    curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_HTTP)
                                # Flag that SOCKS types have already been checked
                                # This will be set when proxy being tried will be SOCKS5
                                # When trying HTTP proxy, this won't impact anything
                                tryingHTTP = True if self.proxyType == 'unknown' else False
                            elif counter == 3 and self.proxyType == 'http':
                                # If it gets here, that means USERGIVEN!!! proxy is not working
                                
                                err = '%s:%s is not working...'%(str(proxy[0]), str(proxy[1]))
                                self.printOutput(err, 'red')
                                self.writeToFile(err)
                            continue
                        else:
                            # if it succeeds as SOCKS5, it will rename the variable, to know which type it is
                            if self.proxyType == 'mixedSocks' or (self.proxyType == 'unknown' and not tryingHTTP):
                                # User given proxy is SOCKS5
                                self.proxyType = 'socks5'
                            elif self.proxyType == 'unknown' and tryingHTTP:
                                # User given proxy is actually of type SOCKS4
                                self.proxyType = 'socks4'
                            self.checkGoogle(curl, proxy)
                            break
                elif self._FLAG == 'locationOnly':
                    # Only checks the location of the proxies
                    self.retrieveLocation(proxy[0])
                    self.returnLocOnlyInfo(proxy)
                self.queue.task_done()
        def writeToFile(self, text):
            if self._FILEDESC:
                self._FILEDESC.write(text + "\n")
        def printOutput(self, text, color):
            if color == 'red' or color == 'yellow':
                text = '[' + time.strftime('%H:%M:%S') + ']' + " [-] " + text
            elif color == 'green':
                text = '[' + time.strftime('%H:%M:%S') + ']' + " [+] " + text
            else:
                color = 'black'
            print colored(text, color)
        def returnLocOnlyInfo(self, proxy):
            # Only checks the location of the proxies
            result = '%s:%s is a %s proxy, located at %s'%(str(proxy[0]), str(proxy[1]), self.proxyType.upper(), self._location)
            self.printOutput(result, 'green')
            self.writeToFile(result)
        def retrieveLocation(self, ip):
            # This is not needed in testOnly mode
            try:
                infoRetriever = InfoRetriever(ip)
                self._location = infoRetriever.getInfo()
            except:
                self._location = 'unknown'
                err = 'IP Locator seems to be down'
                self.printOutput(err, 'red')
                self.writeToFile(err)   
        def checkGoogle(self, curl, proxy):
            # try for google
            curl.setopt(pycurl.URL, self._TEST_URLS[1])
            
            # loop counter, retries 3 times
            counter = 0
            if not self._FLAG:
                self.retrieveLocation(proxy[0])
            # Performs whenever user wants to check whether the proxies are Google alive
            while counter < 3:
                counter+=1
                try:
                    curl.perform()
                except pycurl.error, error:
                    if counter == 3:
                        if not self._FLAG:
                            result = '%s:%s is a working %s proxy but it\'s not Google proxy; it\'s located at %s'%(str(proxy[0]), str(proxy[1]), self.proxyType.upper(), self._location)
                        else:
                            # Performs on testOnly mode
                            result = '%s:%s is a working %s proxy but it\'s not Google proxy'%(str(proxy[0]), str(proxy[1]), self.proxyType.upper())
                        self.printOutput(result, 'yellow')
                        self.writeToFile(result)
                else:
                    if not self._FLAG:
                        result = '%s:%s is a %s Google proxy! It\'s located at %s'%(str(proxy[0]), str(proxy[1]), self.proxyType.upper(), self._location)
                    else:
                        # Performs on testOnly mode
                        result = '%s:%s is a %s Google proxy!'%(str(proxy[0]), str(proxy[1]), self.proxyType.upper())
                    self.printOutput(result, 'green')
                    self.writeToFile(result)
                    break
                
class ProxyTester(object):
    # tests whether the give proxies are working
    _proxies = { 'socks5' : [], 'socks4' : [], 'mixedSocks' : [], 'http' : [], 
                'unknown': [] }
    # In case of user-given proxies 'mixedSocks' will handle all requests for either
    # HTTP proxies, or unknown proxy types
    _queues = {'socks5' : Queue.Queue(), 'socks4' : Queue.Queue(), 'mixedSocks' : Queue.Queue(), 
               'http' : Queue.Queue(), 'unknown' : Queue.Queue()}
    _THREADS_PER_TYPE = 10
    _FILEDESC = None
    def __init__(self, userGiven = False, flag = None, log = False, proxyType = None):
        self._FLAG = flag
        self._UG = userGiven
        if log:
                self._FILEDESC = open(log, 'w')
        if not self._UG:
            self.scraper = ProxyScraper()
            self._proxies = self.scraper.getProxies()
            for key in self._proxies.keys():
                self.handleIPs(key)
        else:
            if self._UG.find(':') != -1:
                # Single proxy mode
                self._proxy = tuple(self._UG.split(':'))
                self.checkSingle(proxyType)
            else:
                # Proxy list mode
                self.lhandler = ListHandler(self._UG, proxyType)
                self._proxies = self.lhandler.getProxies()
                self.handleIPs(proxyType)
        if log:
            self._FILEDESC.close()
    def checkSingle(self, proxyType):
        self._queues[proxyType].put(self._proxy)
        worker = ProxyTestWorker(self._queues[proxyType], proxyType, self._FLAG, self._FILEDESC, True)
        worker.daemon = True
        worker.start()
        self._queues[proxyType].join()
    def handleIPs(self, proxyType):
        isUserGiven = True if self._UG else False
        for lst in self._proxies[proxyType]:
            if isUserGiven:
                self._queues[proxyType].put((lst[0], lst[1]))
            else:
                for ip, port in lst:
                    self._queues[proxyType].put((ip, port))
        for i in range(self._THREADS_PER_TYPE):
            worker = ProxyTestWorker(self._queues[proxyType], proxyType, self._FLAG, self._FILEDESC, isUserGiven)
            worker.daemon = True
            worker.start()
        self._queues[proxyType].join()

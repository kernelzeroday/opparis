#!/usr/bin/python

from splinter import Browser
import sys, time, codecs, string
from PyQt4 import QtCore, QtGui

# uncomment if you want to use privoxy + tor
proxyIP = '127.0.0.1'
proxyPort = 8118

proxy_settings = {'network.proxy.type': 1,
                'network.proxy.http': proxyIP,
                'network.proxy.http_port': proxyPort,
                'network.proxy.ssl': proxyIP,
                'network.proxy.ssl_port':proxyPort,
                'network.proxy.socks': proxyIP,
                'network.proxy.socks_port':proxyPort,
                'network.proxy.ftp': proxyIP,
                'network.proxy.ftp_port':proxyPort
                }

###############################################

results_filename=""
browser=None

class ISISConfirmation(QtGui.QDialog):
    def __init__(self, url, parent=None ):
        super(ISISConfirmation, self).__init__(parent)

        msgBox = QtGui.QMessageBox()
        msgBox.setText('Are you sure its ISIS account?')
        msgBox.addButton(QtGui.QPushButton('Exit'), QtGui.QMessageBox.RejectRole)
        msgBox.addButton(QtGui.QPushButton('No, not sure'), QtGui.QMessageBox.NoRole)
        msgBox.addButton(QtGui.QPushButton('Yes, sure'), QtGui.QMessageBox.YesRole)
      	browser.visit(url)
	
	time.sleep(2)
	retvalue=msgBox.exec_()
        if retvalue ==  2:
	    print "Yes"
    	    codecs.open(results_filename, "ab+", "utf-8").write("%s\n" % url)
        elif retvalue == 1:
	    print "No"
	else:
	    print "\nexiting..."
	    sys.exit(0)
	
def main(argv):
    global browser, results_filename

    if len(argv)<3 or len(argv)>=4:
	print "syntax : %s <urls filename to check> <output filename>" % argv[0]
	print "program checks urls in filename and asks for confirmation (ISIS web or not)"
	sys.exit(0)

    
    results_filename=argv[2]
    browser = Browser( 'firefox' , profile_preferences=proxy_settings )

    try:	
        urls=map(string.strip, codecs.open(argv[1], "rb", "utf-8").readlines())
    except:
        print "error opening %s " % argv[1]
        sys.exit(0)

    app = QtGui.QApplication(argv)

    for url in urls:
	print url, " ", 
        ISISConfirmation(url)

    print "finished."	

if __name__ == "__main__":
    main(sys.argv)

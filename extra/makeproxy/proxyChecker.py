#!/usr/bin/python

import proxyTester,sys,getopt,signal
usage = {'regular': False, 'single': False, 'list': False, 'log': False,
         'testOnly' :False, 'locationOnly': False, 'proxyType': False, 'unknown': False}
def main(argv):
    global usage
    try:
        opts, args = getopt.getopt(argv,"hrs:L:l:p:UnN",
                                   ['regular', 'single=', 'list=', 'log=', 'proxyType=',
                                    'unknownType', 'noLocation', 'noTesting'])
    except getopt.GetoptError:
        print 'Type in \'./proxyChecker.py -h\' for help'
        exit()
    if not opts:
        print 'Type in \'./proxyChecker.py -h\' for help'
        exit()
    for opt, arg in opts:
        if opt == '-h':
            print '''usage: ./proxyChecker.py [options]
            Options:
            
            -r, --regular                     scrapes SOCKS proxies off the internet, checks
                                              whether it's working and retrieves its location
            -s [ip:port], --single=[ip:port]  tests whether user given proxy is working, and
                                              retrieves its location
            -L [listfile], --list=listfile    tests the proxies from the given list file, and
                                              retrieves their locations (proxies in format IP:Port)
            -l [logfile], --log=logfile       logs all the output into a log file (info will not be
                                              logged if you exit the program before it stops running
            -p [type], --proxyType=type       proxyType is required, when user provided proxy or
                                              list of proxies are tested (if proxies in the list are
                                              of different format, use option -U)
            -U, --unknownType                 must be enabled if not proxyType provided for user
                                              provide proxies (this might take quite a while)
            -n, --noLocation                  only tests the proxy(ies), but does not retrieve location
            -N, --noTesting                   only retrieves the location(s) of the proxy(ies),
                                              but does not test
             
            -h                                shows this help menu
            '''
            sys.exit()
        elif opt in ('-r', '--regular'):
            usage['regular'] = True
        elif opt in ('-s', '--single'):
            usage['single'] = arg
        elif opt in ('-L', '--list'):
            usage['list'] = arg
        elif opt in ('-l', '--log'):
            usage['log'] = arg
        elif opt in ('-n', '--noLocation'):
            usage['testOnly'] = True
        elif opt in ('-N', '--noTesting'):
            usage['locationOnly'] = True
        elif opt in ('-p', '--proxyType'):
            usage['proxyType'] = arg.lower()
        elif opt in ('-U', '--unknownType'):
            usage['unknown'] = True
        
def cleanExit(signum, frm):
    print colored("Exiting the program", 'red')
    exit()
    
if __name__ == '__main__':
    main(sys.argv[1:])
    ch = proxyTester.ImportsChecker()
    from termcolor import colored
    signal.signal(signal.SIGINT, cleanExit)
    if usage['regular']:
        if usage['testOnly']:
            #only testing, no location retrieval
            tester = proxyTester.ProxyTester(flag = 'testOnly', log = usage['log'])
        elif usage['locationOnly']:
            #only location retrieval, no testing
            tester = proxyTester.ProxyTester(flag = 'locationOnly', log = usage['log'])
        else:
            #regular
            tester = proxyTester.ProxyTester(log = usage['log'])
    elif usage['single'] or usage['list']:
        # Distinguishes whether a list or single proxy was provided
        method = usage['single'] if usage['single'] else usage['list']
        
        # Distinguishes proxy type
        try:
            if not usage['proxyType'] and not usage['unknown']:
                raise Exception('No proxy type identification given')
        except:
            print colored('Please enter either a proxy(-ies) type(s), or select an unknown option if you are unfamiliar with the proxy type', 'red')
            exit()
        else:
            pType = usage['proxyType'] if usage['proxyType'] else 'unknown'
            
        if usage['testOnly']:
            #only testing, no location retrieval
            tester = proxyTester.ProxyTester(userGiven = method, flag = 'testOnly', log = usage['log'], proxyType = pType)
        elif usage['locationOnly']:
            #only location retrieval, no testing
            tester = proxyTester.ProxyTester(userGiven = method, flag = 'locationOnly', log = usage['log'], proxyType = pType)
        else:
            #regular
            tester = proxyTester.ProxyTester(userGiven = method, log = usage['log'], proxyType = pType)
    else:
        print colored('One of the arguments -r, -u, or -L must be supplied', 'red')
        exit()
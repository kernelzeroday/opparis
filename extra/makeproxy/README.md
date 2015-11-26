proxy-checker
=============

DEPS: 'pip install termcolor; pip install mechanize;'


Scrapes SOCKS proxies of the Internet, checks whether they are working or not, and where they are located. It can also check user provided proxies.

Python `setuptools` module has to be installed, in order for the script to run.

Usage
=============
Before using the script, please run a command `chmod a+x proxyChecker.py`; otherwise, the script won't run. Or you can simply run the script by `python proxyChecker.py [options]`
            
            
	usage: ./proxyChecker.py [options]
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

Future
=============
I'd love to add proxies that require authentication to be supported to this tool. However, I don't have any proxies of that type. If anybody has them and would want me to add such thing, please email me.

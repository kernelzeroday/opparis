# tmap 0.1
# Coded by TheKingOf9x <AT> yandex . com
# Fast multi-threaded port scanner which tunnels through TOR.
# Depends on the PySocks library: https://github.com/Anorov/PySocks
# And of course TOR: apt-get install tor
#
# Do not use hostnames, may leak DNS info. only use IP addresses.
# 
# Not happy with the Privoxy + TOR (exit relay only) + nmap config. I made this.
#
# Usage:
# python tmap.py

import sys
import socks
import datetime
import threading
lock = threading.Semaphore(value = 1)

#Port of TOR server
TOR_PORT = 9050
#timeout. Experiment with this.
TIMEOUT = 20
#Port list to scan, ammend at will
ports = (21,22,23,80,443,1433,3306,8080)

def main():

	if len(sys.argv) < 3:
		print("\033[92m\n\t\t\ttmap 0.1\n\nFast multi-threaded port scanner which tunnels through TOR.\n\n\033[0m")
		print("Single host scan:\npython " + sys.argv[0] + " -s 192.168.0.1\n")
		print("/24 (Class C) range scan:\npython " + sys.argv[0] + " -r 192.168.0\n")
		print("List scan:\npython " + sys.argv[0] + " -l IPlist.txt\n")
		exit(0)

	scan_type = sys.argv[1]
	parameter = sys.argv[2]

	filename = datetime.datetime.now().strftime("%H:%M_%d-%m-%y.tmap")
	try:
		log = open(filename, "a")
	except:
		pass

	if scan_type == "-s":
		host_scan(parameter, log)
	elif scan_type == "-r":
		range_scan(parameter, log)
	elif scan_type == "-l":
		list_scan(parameter, log)
	else:
		exit(1)

#main connect function
def connect(ip, port, log):
	try:
		s = socks.socksocket()
		s.setproxy(socks.PROXY_TYPE_SOCKS5, 'localhost', TOR_PORT)
		s.settimeout(TIMEOUT)
		s.connect((ip, port))
		output = ip + ":" + str(port)
		lock.acquire() # Lock/unlock to clean up screen output.
		print(output)
		
		try:
			log.write(output + "\n")
		except:
			pass
			
	except:
		pass

	finally:
		lock.release()

def host_scan(ip, log):
	ip = ip.strip()
	for port in ports:
		try:
			t = threading.Thread(target=connect, args=(ip, port, log))
			t.start()
		except:
			pass

def range_scan(ip, log):
	ip = ip.strip()
	for i in range(1, 255):
		ip_addr = ip + "." + str(i)
		for port in ports:
			try:
				t = threading.Thread(target=connect, args=(ip_addr, port, log))
				t.start()
			except:
				pass

def list_scan(parameter, log):
	try:
		f = open(parameter, 'r')
	except:
		print("Could not open file: " + parameter)
		exit(1)

	for ip in f:
		ip = ip.strip()
		for port in ports:
			try:
				t = threading.Thread(target=connect, args=(ip, port, log))
				t.start()
			except:
				pass

if __name__ == '__main__':
	main()


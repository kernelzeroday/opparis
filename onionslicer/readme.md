# onionslicer
A reverse shell wrapper for tor servers. Get a shell over tor via socat.

# What the hell is this?
Onionslice is a shell script for exploiting linux systems running tor. It is essentially a bash wrapper to deploy a trojan using whatever is already on the system, with preference to python. It does the following things:
* Checks for the presence of socat. If it's not there, download the binary.
* Creates a wrapper script that inifinitely starts a reverse shell which connects to your .onion hidden service, where you receive your shell.
* Checks for python, ruby, or ncat or nc, or netcat perl, or telnet to use for the reverse shell. The target sytem likely has one of these on it.
* Checks for root, and if we have root, installs the wrapper as a boot service (via ./etc/rc.local) to make it persistent.
* Finally, excutes your shellcode.

# What is that shellcode doing?
* Connecting to the localhost on port 4430 (where socat is listening). 
* The connection is than forwarded to your hidden service.

# Usage:
* Edit the variable 'onion' to reflect where your .onion url
* Edit the variable 'orPrt' to reflect which port you're listeing on
* Start a handler with nc (nc -lp 127.0.0.1 12345) or use the handler.
* Upload to target tor server somehow and execute (there's always the <a href=https://exploit-db.com> exploit db </a>...)
* Receive your torified reverse shell.

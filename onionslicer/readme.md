# onionslicer
A reverse shell wrapper for tor servers. Get a shell over tor via socat.

# What the hell is this?

Onionslice is a shell script for exploiting linux systems running tor. It does the following things:
* Checks for the presence of socat. If not there, download the binary.
* Creates a wrapper script that inifinitely starts a reverse shell, which connects to your .onion hidden service, where you receive your shell.
* Checks for python, ruby, or nc to use for the reverse shell. The target sytem likely has one of these on it.
* Checks for root, and if we got root, installs the wrapper as a boot service (via ./etc/rc.local)
* Finally, excutes your shellcode.

# What is that shellcode doing?
* Connecting to the localhost on port 4430 (where socat is listening)
* THe connection is than forwarded to your hidden service.

# Usage:
* Edit the variable 'onion' to reflect where your .onion url
* Edit the variable 'orPrt' to reflect which port you're listeing on
* Start a handler with nc (nc -lp 127.0.0.1 12345)
* Upload to target tor server somehow and execute
* You got a reverse shell over tor!

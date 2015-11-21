/*

flsocket.h

Copyright (C) 2004, 2005 Jordan Wilberding

This program is free software; you can redistribute it and/or 
modify it under the terms of the GNU General Public License as published by the 
Free Software Foundation; either version 2 of the License, or (at your option) 
any later version. This program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
details. You should have received a copy of the GNU General Public License along 
with this program; if not, write to the Free Software Foundation, Inc., 675 Mass 
Ave, Cambridge, MA 02139, USA.

diginux@diginux.net

Thanks: Portions of code borrowed from Rick Smereka's GPL'd cross-platform
sockets library.

*/
#ifdef OS_WIN32
#include <winsock.h>

#define WINSOCK_VERSION 0x0101	// program requires Winsock V1.1
#endif

#ifdef OS_UNIX
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>

#define INVALID_SOCKET (-1)
#define SOCKET_ERROR (-1)
#endif

#define DEFAULT_PROTOCOL 0	    // use default protocol
#define NO_FLAG 0                   // no send or receive flags
#define IPC_MAXREC 100000           // maximum size of send or receive data
#define IPC_SR_BUFSIZE 1024         // size of single send/receive buffer
#define QUEUE_SIZE 5                // allow up five requests in queue


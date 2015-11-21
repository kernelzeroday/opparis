/*

ssocket.cpp

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

#include <iostream>
using namespace std;

#include "stdhead.h"
#include "flsocket.h"
#include "ssocket.h"

ssocket::ssocket()
{
   // No parameter constructor.

   server_hostname = "";
   server_port = 0;
   server_init = FALSE;
}

ssocket::ssocket(int port)
{
   /* Constructor using port number. After loading port number,
      attempt to initialize the server. */

   server_hostname = "";
   server_port = port;
   server_init = FALSE;
   (void)init(port);
}

bool ssocket::init(int port)
{
   /* Initialize the server for communication. The port
      that the server listens to is expected in 'port'.
      Function returns 'TRUE' upon success,'FALSE' otherwise. */

   char *localHost;
   int err = FALSE;

   if (port <= 0)
      return(FALSE);

   if (server_init)
      return(FALSE);

   try
      {
      localHost = new char[1024];
      }

   catch(bad_alloc)
      {
      err = TRUE;
      }

   if (err)
      return(FALSE);

   // attempt to resolve the local host name

   if (gethostname(localHost, 1023))
      {
      delete localHost;
      return(FALSE);
      }

#ifdef OS_WIN32
	serverSocket = socket(PF_INET, SOCK_STREAM, DEFAULT_PROTOCOL);
#endif

#ifdef OS_UNIX
	serverSocket = socket(AF_INET, SOCK_STREAM, DEFAULT_PROTOCOL);
#endif

	if (serverSocket == INVALID_SOCKET)
	   {
      delete localHost;
	   return(FALSE);
	   }

	// populate server address structure

   memset(&sockServerAddr, 0,	sizeof(sockServerAddr));
	sockServerAddr.sin_family = AF_INET;
	sockServerAddr.sin_addr.s_addr = INADDR_ANY;
   sockServerAddr.sin_port = htons(port);

	// bind the server socket

#ifdef OS_WIN32
	if (bind(serverSocket,(LPSOCKADDR)&sockServerAddr,sizeof(sockServerAddr))
	   == SOCKET_ERROR)
#endif

#ifdef OS_UNIX
	if (bind(serverSocket, (sockaddr *)&sockServerAddr, sizeof(sockServerAddr))
	   == SOCKET_ERROR)
#endif

	   {
      delete localHost;
	   return(FALSE);
	   }

	// listen on port

	if (listen(serverSocket, QUEUE_SIZE) == SOCKET_ERROR)
	   {
      delete localHost;
	   return(FALSE);
	   }

	srvclientSocket = INVALID_SOCKET;
   server_hostname = localHost;
   delete localHost;
   server_init = TRUE;
	return(TRUE);
}

bool ssocket::server_wait(void)
{
   /* Accept a client connection. Function
		returns 'TRUE' if a client connection
		was successful, 'FALSE' otherwise. */

#ifdef OS_WIN32
   int len = sizeof(SOCKADDR);
#else
   socklen_t len = sizeof(sockClientAddr);
#endif

   if (!is_init())
      return(FALSE);

	srvclientSocket = INVALID_SOCKET;

#ifdef OS_WIN32
	srvclientSocket = accept(serverSocket, (LPSOCKADDR)&sockClientAddr,
	                      (LPINT)&len);
#endif

#ifdef OS_UNIX
	srvclientSocket = accept(serverSocket, (sockaddr *)&sockClientAddr, &len);
#endif

	if (srvclientSocket == INVALID_SOCKET)
		return(FALSE);

	return(TRUE);
}

bool ssocket::close_client(void)
{
   /* Close the client socket in use by the server.
      Function returns 'TRUE' upon success, 'FALSE'
      otherwise. */

   if (srvclientSocket == INVALID_SOCKET)
      return(FALSE);

#ifdef OS_WIN32
   if (closesocket(srvclientSocket) == SOCKET_ERROR)
      return(FALSE);
#endif

#ifdef OS_UNIX
   close(srvclientSocket);
#endif

   srvclientSocket = INVALID_SOCKET;
   return(TRUE);
}

bool ssocket::close_all(void)
{
   /* Close all sockets in use by the server.
      Function returns 'TRUE' upon success, 'FALSE'
      otherwise. */

   if (srvclientSocket != INVALID_SOCKET)
#ifdef OS_WIN32
      if (closesocket(srvclientSocket) == SOCKET_ERROR)
         return(FALSE);
#endif

#ifdef OS_UNIX
      close(srvclientSocket);
#endif

#ifdef OS_WIN32
   if (closesocket(serverSocket) == SOCKET_ERROR)
         return(FALSE);
#endif

#ifdef OS_UNIX
   close(serverSocket);
#endif

   return(TRUE);
}

int ssocket::recv_data(string& buf)
{
   /* Receive data from the socket which is assumed
      to be open. Method returns the number of bytes
      read upon success with the received data loaded
      into 'buf', zero otherwise. */

   char *fbuf;
   int charRecv, done = FALSE;

   fbuf = new char[IPC_SR_BUFSIZE];
   buf = "";

   while(!done)
   	{
#ifdef OS_WIN32
      charRecv = recv(srvclientSocket, (LPSTR)fbuf, (IPC_SR_BUFSIZE - 1), NO_FLAGS);
#endif

#ifdef OS_UNIX
      charRecv = recv(srvclientSocket, fbuf, (IPC_SR_BUFSIZE - 1), NO_FLAGS);
#endif

   	if (charRecv == SOCKET_ERROR)
   	   {
         delete fbuf;
         return(0);
         }

      fbuf[charRecv] = EOS;
      for (int i = 0; i < charRecv; i++)
      { 
        buf += fbuf[i];
      }
      //buf += fbuf;
      //cout << "char recieved: " << charRecv << endl;

   	if (charRecv < (IPC_SR_BUFSIZE - 1))
   	   done = TRUE;
   	}

   delete fbuf;
   return(buf.length());
}

int ssocket::send_data(string& buf)
{
   /* Send data to the socket. Method returns the
		number of bytes sent upon success, zero
      otherwise. */

   string fbuf;
	int len, charSent, pos = 0, bytesToGo, done = FALSE;
	int chunk;

   len = buf.length();

	if (!len)
		return(0);

	// if less than 'IPC_SR_BUFSIZE' to send, use one shot

	if (len < IPC_SR_BUFSIZE)
	   {
      if ((charSent = send(srvclientSocket, buf.c_str(), len, NO_FLAGS)) == SOCKET_ERROR)
		   return(FALSE);

	   return(charSent);
	   }

	bytesToGo = len;

	// send one buffer length at a time

	while(!done)
	   {
	   if (bytesToGo > (IPC_SR_BUFSIZE - 1))
	   	chunk = IPC_SR_BUFSIZE - 1;
	  	else
	  		chunk = bytesToGo;

      fbuf = buf.substr(pos, chunk);

      if ((charSent = send(srvclientSocket, fbuf.c_str(), chunk, NO_FLAGS)) == SOCKET_ERROR)
			{
	   	pos = 0;
	   	break;
	   	}

	   bytesToGo -= chunk;
	   pos += charSent;

	   if (bytesToGo <= 0)
	      done = TRUE;
	   }

	return(pos);
}

/*

csocket.cpp

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

#include "stdhead.h"
#include "flsocket.h"
#include "csocket.h"

csocket::csocket()
{
   // No parameter constructor.

   client_hostname = "";
   client_port = 0;
   client_init = FALSE;
}

csocket::csocket(string& host_name, int port)
{
   // Constructor using string host name and port number.

   if (!set_active(host_name, port))
      {
      client_hostname = "";
      client_port = 0;
      client_init = FALSE;
      }
}

csocket::csocket(char *host_name, int port)
{
   // Constructor using char host name and port number.

   string host;

   if (host_name == (char *)NULL || !strlen(host_name))
      {
      client_hostname = "";
      client_port = 0;
      client_init = FALSE;
      return;
      }

   host = host_name;

   if (!set_active(host, port))
      {
      client_hostname = "";
      client_port = 0;
      client_init = FALSE;
      }
}

int csocket::set_active(string& host_name, int port_number)
{
   /* Set the active server host name and port number.
      Method returns 'TRUE' upon success, 'FALSE'
      otherwise. */

   if (host_name.empty())
      return(FALSE);

   if (port_number <= 0)
      return(FALSE);

   /* load class data, do not check connection */

   client_hostname = host_name;
   client_port = port_number;
   client_init = TRUE;
   return(TRUE);
}

int csocket::get_active(string& host_name, int& port_number)
{
   /* Obtain the current server host name and port number.
      Method returns 'TRUE' upon success with the server
      host name loaded into 'host_name', the server port number will
      be loaded into 'port_number'. Method returns 'FALSE'
      upon failure. */

   if (host_name.empty())
      return(FALSE);

   host_name = "";
   port_number = 0;

   if (!client_init)
      return(FALSE);

   host_name = client_hostname;
   port_number = client_port;
   return(TRUE);
}

int csocket::close_socket(void)
{
   /* Close the socket between client and server.
      Method returns 'TRUE' upon success, 'FALSE'
      otherwise. */

#ifdef OS_WIN32
   if (closesocket(clientsock) == SOCKET_ERROR)
      return(FALSE);
#endif

#ifdef OS_UNIX
   close(clientsock);
#endif

   return(TRUE);
}

int csocket::recv_data(string& buf)
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
      charRecv = recv(clientsock, (LPSTR)fbuf, (IPC_SR_BUFSIZE - 1), NO_FLAGS);
#endif

#ifdef OS_UNIX
      charRecv = recv(clientsock, fbuf, (IPC_SR_BUFSIZE - 1), NO_FLAGS);
#endif

   	if (charRecv == SOCKET_ERROR)
   	   {
         delete fbuf;
         return(0);
         }

		fbuf[charRecv] = EOS;
      buf += fbuf;

   	if (charRecv < (IPC_SR_BUFSIZE - 1))
   	   done = TRUE;
   	}

   delete fbuf;
   return(buf.length());
}

int csocket::send_data(string& buf)
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
      if ((charSent = send(clientsock, buf.c_str(), len, NO_FLAGS)) == SOCKET_ERROR)
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

      if ((charSent = send(clientsock, fbuf.c_str(), chunk, NO_FLAGS)) == SOCKET_ERROR)
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


int csocket::client_connect(void)
{
   /* Use the previously loaded host name and port number to
      connect to the server. Method returns 'TRUE' if the
      connection was successful, 'FALSE' otherwise. */

   if (!client_init)
      return(FALSE);

   // resolve server host name

   lpHostEnt = gethostbyname(client_hostname.c_str());

   if (!lpHostEnt)
      return(FALSE);

	// create the socket

#ifdef OS_WIN32
	clientsock = socket(PF_INET, SOCK_STREAM, DEFAULT_PROTOCOL);
#endif

#ifdef OS_UNIX
	clientsock = socket(AF_INET, SOCK_STREAM, DEFAULT_PROTOCOL);
#endif

	if (clientsock == INVALID_SOCKET)
	   return(FALSE);

   // load client address data

   memset(&sockClientAddr, 0, sizeof(sockClientAddr));
	sockClientAddr.sin_family = AF_INET;
   sockClientAddr.sin_port = htons(client_port);

#ifdef OS_WIN32
	sockClientAddr.sin_addr = *((LPIN_ADDR)*lpHostEnt->h_addr_list);
#endif

#ifdef OS_UNIX
	sockClientAddr.sin_addr.s_addr = ((struct in_addr *)(lpHostEnt->h_addr))->s_addr;
#endif

	// connect to server

#ifdef OS_WIN32
	if (connect(clientsock, (LPSOCKADDR)&sockClientAddr, sizeof(sockClientAddr)))
#endif

#ifdef OS_UNIX
   if (connect(clientsock, (sockaddr *)&sockClientAddr, sizeof(sockClientAddr)) == SOCKET_ERROR)
#endif
	   return(FALSE);

	return(TRUE);
}

/*

csocket.h

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

#ifndef CSOCKET_HXX
#define CSOCKET_HXX

#include <string>
using namespace std;

class csocket
{
private:
#ifdef OS_WIN32
  SOCKET clientsock;
  SOCKADDR_IN sockClientAddr;
  LPHOSTENT lpHostEnt;
#endif

#ifdef OS_UNIX
  int clientsock;
  struct sockaddr_in sockClientAddr;
  struct hostent *lpHostEnt;
#endif

  string client_hostname;
  int client_port;
  bool client_init;

public:
  // constructors
  csocket();
  csocket(string& host_name, int port);
  csocket(char *host_name, int port);

  // member fuctions
  int set_active(string& host_name, int port_number);
  int get_active(string& host_name, int& port_number);
  int close_socket(void);
  int recv_data(string& buf);
  int send_data(string& buf);
  bool is_init(void) { return(client_init); }
  
  // private member functions
  int client_connect(void);
  int send_data_buf(char *buf, int length);
};
#endif

/*

ssocket.h

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

#ifndef SSOCKET_HXX
#define SSOCKET_HXX

#include <string>
using namespace std;

class ssocket
{
private:
#ifdef OS_WIN32
  SOCKET serverSocket;
  SOCKET srvclientSocket;
  SOCKADDR_IN sockServerAddr;
  SOCKADDR_IN sockClientAddr;
#endif

#ifdef OS_UNIX
  int serverSocket;
  int srvclientSocket;
  struct sockaddr_in sockServerAddr;
  struct sockaddr_in sockClientAddr;
#endif

  string server_hostname;
  int server_port;
  bool server_init;

public:
  // constructors
  ssocket();
  ssocket(int port);

  // member fuctions
  bool init(int port);
  bool server_wait(void);
  bool is_init(void) { return(server_init); }
  bool close_client(void);
  bool close_all(void);
  int recv_data(string& buf);
  int send_data(string& buf);
};
#endif

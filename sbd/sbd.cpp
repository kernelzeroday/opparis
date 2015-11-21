/*

sbd.cpp

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

*/

#include "stdhead.h"
#include "flsocket.h"
#include "csocket.h"
#include "sha1.h"
#include "utils.h"
#ifdef WIN32
#include <io.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#endif
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <assert.h>
using namespace std;

// Default SBD Port
#define SBD_PORT 31415

// Constants
const unsigned int SHA1_SIZE = 20;

/* The size in bytes of the hash output. */
#define HASH_BIN_SIZE 20
/* The size in bytes of the block the hash operates on. */
#define HASH_BLOCK_SIZE 64
#define HASH_TEXT_SIZE (HASH_BIN_SIZE*2+1)
#define HASH_INPUT_SIZE (HASH_BLOCK_SIZE+HASH_BIN_SIZE)
#define MAX_SECRET_SIZE 64

// Local functions
int EncryptString(string &serverAuthStr, string &msg, string &eMsg);

int main(int argc, char *argv[])
{
   string msg, eMsg, host, result, serverAuthStr;
   int msgSize, port, keyBytesUsed;
   csocket c1("localhost", SBD_PORT);

   InitSockets();

   if (argc > 2)
   {
    host = argv[1];
    
    // If user gives port, use it, otherwise use default
    if (argc > 3)
    {
      port = atoi(argv[2]);
      msg=argv[3];
    }
    else
    {
      port = SBD_PORT;
      msg=argv[2];
    }
    
    msgSize = msg.length();
    
    /*if (msgSize+ENC_BYTE_SIZE > BUF_SIZE)
    {
      cout << "Error! Message too big!" << endl;
    }*/

    c1.set_active(host, port);
  }
  else
  {
    cout << "Invalid usage! Use: " << argv[0] << " hostname port message" << endl;
    CleanupSockets();
    return 1;
  }
  
  if (!c1.client_connect())
  {
    cout << "Error! Could not connect!" << endl;
    CleanupSockets();
    return 1;
  }

  // Receive the random bytes that will hopefully stop most IP spoofs
  c1.recv_data(serverAuthStr);
  
  keyBytesUsed = EncryptString(serverAuthStr, msg, eMsg);
  
  if (keyBytesUsed == 0)
  {
    cout << "Error! Could not encrypt string!" << endl;
    return 1;
  }
  
  // Send data and receive result
  int count = c1.send_data(eMsg);
  cout << "Sent: " << count << " bytes" << endl;

  // Cleanup the sockets
  c1.close_socket();
  CleanupSockets();
  
  // We always assume server recieved the command ok
  // truncate file so same bytes are not used
  truncateFile("enckey.bits", keyBytesUsed);

  return 0;
}

// Main encryption done here
int EncryptString(string &serverAuthStr, string &msg, string &eMsg)
{
  unsigned int i;                        // Iterator
  vector<unsigned char> key;             // OTP key read from file
  unsigned char hashOTP[SHA1_SIZE];      // First 20 bytes of OTP used to comput HMAC-SHA1 
  unsigned char finishedHash[SHA1_SIZE]; // Finished HMAC-SHA1 hash
  eMsg="";                               // Finished cypher text
  
  // get key bytes from file
  readKey("enckey.bits", key, SHA1_SIZE*2 + msg.size());
  
  // Copy 20 bytes of key over to hashOTP for computing HMAC-SHA1
  for (i = 0; i < SHA1_SIZE; i++)
  {
    hashOTP[i] = key[i];
  }
  
  // Compute HMAC-SHA1
  serverAuthStr += msg;
  ComputHMACSHA1Hash(&hashOTP[0], SHA1_SIZE, (char *)serverAuthStr.c_str(), serverAuthStr.size(), &finishedHash[0]);
  
  // Prepend hash to message
  eMsg="";
  for (i = 0; i < SHA1_SIZE; i++)
  {
    eMsg += finishedHash[i];
  }
  eMsg += msg;
  
  // Now xor the whole thing with OTP
  for (i = 0; i < eMsg.size(); i++)
  {
    eMsg[i] = eMsg[i]^key[i+SHA1_SIZE];
  }
  
  // We are done, return the number of bytes of OTP we used
  return SHA1_SIZE*2 + msg.size();
}

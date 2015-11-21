/*

sbdd.cpp

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
#include "ssocket.h"
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

using namespace std;

// Constants
const unsigned int SHA1_SIZE = 20;
const unsigned int AUTH_SIZE = 20;

/* The size in bytes of the hash output. */
#define HASH_BIN_SIZE 20
/* The size in bytes of the block the hash operates on. */
#define HASH_BLOCK_SIZE 64
#define HASH_TEXT_SIZE (HASH_BIN_SIZE*2+1)
#define HASH_INPUT_SIZE (HASH_BLOCK_SIZE+HASH_BIN_SIZE)
#define MAX_SECRET_SIZE 64

// Log file
ofstream logFile;

// Local functions
char HandleString(string &infileCmd, string &serverAuthStr);
int CheckValid(string &infileCmd, string &serverAuthStr);

int main(int argc, char *argv[])
{
  string h1;
  vector<unsigned char> authBytes;
  string serverAuthStr, clientAuthStr;
  unsigned int i;
  bool done = false;
  int port = SBD_PORT;
  
  logFile.open("sbdd.log",ios::out);
  if (!logFile)
  {
    cout << "Error! Unable to open sbdd.log, logging disabled." << endl;
  }

  InitSockets();

  ssocket s1(SBD_PORT);

  // Use supplied port if given
  if (argc > 1)
  {
    port = atoi(argv[1]);
    s1.init(port);
  }

  if (!s1.is_init())
  {
    cout << "Could not initialize on port: " << port << endl;
    CleanupSockets();
    logFile.close();
    return 1;
  }

  // Wait endlessly for connections
  while(!done)
  {
    logFile << "waiting for client connection..." << endl;
    serverAuthStr = "";

    if (!s1.server_wait())
    {
      CleanupSockets();

      logFile << "Client connection error!" << endl;
      CleanupSockets();
      logFile.close();
      return 1;
    }
    
    readKey("athkey.bits", authBytes, AUTH_SIZE);
    truncateFile("athkey.bits", AUTH_SIZE);
  
    for (i = 0; i < authBytes.size() ; i++)
    {
      serverAuthStr += authBytes[i];
    }
    
    s1.send_data(serverAuthStr);
    
    if (s1.recv_data(h1) == 0)
    {
      logFile << "Error receiving client data!" << endl;
    }
    else
    {
      logFile << "Recieved : " << h1.length() << " bytes" << endl;
      
      // We just handle the string, and that is it, we do not
      // send a confirmation back to the client 
      HandleString(h1, serverAuthStr);
    }
    
    if (!s1.close_client())
    {
      logFile << "Error closing client socket!" << endl;
    }
  }

  if (!s1.close_all())
  {
    logFile << "Error closing sockets" << endl;
  }
  else
  {
    logFile << "Termination requested" << endl;
  }

  CleanupSockets();
  logFile.close();
  
  return 0;
}

// Handles incoming messages, for now it just iteratively guesses
// where the starting point is for the key.
char HandleString(string &infileCmd, string &serverAuthStr)
{
  if (CheckValid(infileCmd, serverAuthStr) == 0)
  {
    //logFile << "Yay!" << " " << i << endl;
    return 1;
  }
  else
  {
    //logFile << "No!" << " " << i << endl;
  }
  
  return 0;
}

// Our main function to check if incoming message is authentic
int CheckValid(string &infileCmd, string &serverAuthStr)
{
  string cmd;                            // Stores the incoming command
  vector<unsigned char> key;             // The key as read from file
  unsigned int i;                        // Used as iterator
  unsigned char hashOTP[SHA1_SIZE];      // First 20 bytes of OTP used to comput HMAC-SHA1 
  unsigned char finishedHash[SHA1_SIZE]; // Finished HMAC-SHA1 hash
  
  readKey("deckey.bits", key, infileCmd.size()+SHA1_SIZE);
  
  // Copy 20 bytes of key over to hashOTP for computing HMAC-SHA1
  for (i = 0; i < SHA1_SIZE; i++)
  {
    hashOTP[i] = key[i];
  }
  
  // Now xor the whole thing with OTP to get original message
  for (i = 0; i < infileCmd.size(); i++)
  {
    infileCmd[i] = infileCmd[i]^key[i+SHA1_SIZE];
  }
  
  // Now get the command
  cmd="";
  for (i = 0; i < infileCmd.size()-SHA1_SIZE; i++)
  {
    cmd += infileCmd[i+SHA1_SIZE];
  }
  
  logFile << "Command is: " << cmd.c_str() << endl;
  
  // Compute HMAC-SHA1
  serverAuthStr += cmd;
  ComputHMACSHA1Hash(&hashOTP[0], SHA1_SIZE, (char *)serverAuthStr.c_str(), serverAuthStr.size(), &finishedHash[0]);
 
  // Now compare hashes
  for (i = 0; i < SHA1_SIZE; i++)
  {
    if ((unsigned char)infileCmd[i] != finishedHash[i])
      break;
  }
  
  // Log result, and return
  if (i < SHA1_SIZE)
  {
    logFile << "Hash Not Verified:" << i << endl;
    return -1;
  }
  else
  {
    logFile << "Hash Verified" << endl;
    logFile << "Key confirmed, executing: " << cmd.c_str() << endl;
    logFile << "system() returned : " << system(cmd.c_str()) << endl;
    
    //truncate bytes file
    truncateFile("deckey.bits", infileCmd.size()+SHA1_SIZE);
    return 0;
  }

  return 0;
}

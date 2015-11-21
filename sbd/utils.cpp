/*

utils.cpp

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
const int SHA1_SIZE = 20;
const int AUTH_SIZE = 20;


// Needed for windows sockets to work correctly
#ifdef OS_WIN32
WSADATA wsaData;
#endif

/* The size in bytes of the hash output. */
#define HASH_BIN_SIZE 20
/* The size in bytes of the block the hash operates on. */
#define HASH_BLOCK_SIZE 64
#define HASH_TEXT_SIZE (HASH_BIN_SIZE*2+1)
#define HASH_INPUT_SIZE (HASH_BLOCK_SIZE+HASH_BIN_SIZE)
#define MAX_SECRET_SIZE 64



#include "utils.h"

// This reads next character from end of file
// we read backwards, since it is easier to truncate
// the end of the file, instead of the beginning
unsigned char getNextCharFromBack(FILE *fd)
{
  char c = fgetc(fd);
  long t = ftell(fd);
  fseek(fd, t-2, SEEK_SET);
  return c;
}

// Does platform specific socket initialization
void InitSockets()
{
#ifdef OS_WIN32
if (WSAStartup(WINSOCK_VERSION, &wsaData))
{
  cout << "Unable to start WinSock. Quiting." << endl;
  WSACleanup();
  exit(0);
}
#endif
}

// Does platform specific socket cleanup
void CleanupSockets()
{
#ifdef OS_WIN32
  WSACleanup();
#endif
}

// Reads key of size into vector
int readKey(string filename, vector<unsigned char> &key, int size)
{
  FILE *fd;
  int filesize;
  
  // Open file with encryption bytes, and seek to end
  fd = fopen(filename.c_str(), "r");
  if (fd == NULL)
  {
    cout << "Error opening " << filename.c_str() << " Quitting." << endl;
    return -1;
  }
  fseek(fd, 0L, SEEK_END);
  
  // get offset(since we just used SEEK_END, this will be file size)
  filesize = ftell(fd);
  
  // setup file to read last character
  fseek(fd, filesize-2, SEEK_SET);
  
  // get key bytes from file
  for (int i = 0; i < size; i++)
  {
    key.push_back(getNextCharFromBack(fd));
  }
  
  fclose(fd);
  
  return filesize;
}

int truncateFile(string filename, int numberTruncateBytes)
{
  int filesize;
  
  // Open file with encryption bytes, and seek to end
  FILE *fd = fopen(filename.c_str(), "r");
  if (fd == NULL)
  {
    cout << "Error opening " << filename.c_str() << " Quitting." << endl;
    return -1;
  }
  
  fseek(fd, 0L, SEEK_END);
  
  // get offset(since we just used SEEK_END, this will be file size)
  filesize = ftell(fd);
  fclose(fd);
    
   // Truncate file so same bits are not used
  #ifdef WIN32
  int fh;
  if((fh = _open(filename.c_str(), _O_RDWR | _O_CREAT, _S_IREAD | _S_IWRITE ))  != -1)
  {
    _chsize(fh, filesize-numberTruncateBytes);
    _close(fh);
  }
  #else
  truncate(filename.c_str(),filesize-numberTruncateBytes);
  #endif
  
  return 0;
}

// HMAC-SHA1 (TODO: Update to SHA-256), borrowed from GPL'd ostiary
void ComputHMACSHA1Hash(unsigned char *in_hash, size_t in_hash_siz,
             char *secret, size_t secret_siz, unsigned char *hash_out)
{
  int i;
  char temp_hash[HASH_BIN_SIZE]; /* only needed if secret's too big */
  char hash_input[HASH_INPUT_SIZE];

  assert(secret_siz < MAX_SECRET_SIZE);

  // Clear the input struct.
  memset(hash_input, 0, HASH_INPUT_SIZE);

  // Load up the secret.
  if (secret_siz < HASH_BLOCK_SIZE) {
    memcpy(hash_input, secret, secret_siz);
  } else {
    /* Too big, just store the hash, per the HMAC spec. */
    /* Note: currently this just can't happen, but if someone mucks with
       the max secret size, or changes hash functions, this won't break. */
    sha1_buffer(secret, secret_siz, temp_hash);
    memcpy(hash_input, temp_hash, HASH_BIN_SIZE);
  }

  // XOR the first block with the inner pad value.
  for (i=0; i<HASH_BLOCK_SIZE; i++) {
    hash_input[i] ^= 0x36;
  }

  // Now add the salt from the server.
  memcpy(hash_input+HASH_BLOCK_SIZE, in_hash, in_hash_siz);

  // The first (inner) hash. Note we use the 'hash_out' buffer as
  //   temporary storage for the inner hash.
  sha1_buffer(hash_input, HASH_BLOCK_SIZE+in_hash_siz, hash_out);

  // Now the outer hash.

  // Clear the input struct again.
  memset(hash_input, 0, HASH_INPUT_SIZE);

  // Copy the secret again.
  if (secret_siz < HASH_BLOCK_SIZE) {
    memcpy(hash_input, secret, secret_siz);
  } else {
    /* Too big, just store the hash, per the HMAC spec. */
    /* (temp_hash already computed above) */
    memcpy(hash_input, temp_hash, HASH_BIN_SIZE);
  }

  // The outer pad XOR value.
  for (i=0; i<HASH_BLOCK_SIZE; i++) {
    hash_input[i] ^= 0x5c;
  }

  // Append the inner hash.
  memcpy(hash_input+HASH_BLOCK_SIZE, hash_out, HASH_BIN_SIZE);

  // The second (outer) hash.
  sha1_buffer(hash_input, HASH_BLOCK_SIZE+HASH_BIN_SIZE , hash_out);
}



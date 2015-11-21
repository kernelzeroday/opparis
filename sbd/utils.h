/*

utils.h

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

#ifndef UTILS_HEADER
#define UTILS_HEADER

#include <vector>
#include <string>

using namespace std;

void InitSockets();
void CleanupSockets();
unsigned char getNextCharFromBack(FILE *fd);
int readKey(string filename, vector<unsigned char> &key, int size);
int truncateFile(string filename, int numberTruncateBytes);
void ComputHMACSHA1Hash(unsigned char *in_hash, size_t in_hash_siz,
             char *secret, size_t secret_siz, unsigned char *hash_out);

#endif

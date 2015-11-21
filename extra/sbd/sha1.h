/*

sha1.h

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

Thanks: Portions of code borrowed from Raymond Ingles's GPL'd cross-platform
ostiary program. Adapted to compile without a config file.

*/

/* sha1.h - Declaration of functions and data types used for SHA-1 sum
   computing library functions.
   Copyright (C) 2004 Raymond Ingles
*/

#ifndef _SHA1_H
#define _SHA1_H 1

/* Compute SHA-1 message digest for LEN bytes beginning at BUFFER.  The
   result is always in little endian byte order, so that a byte-wise
   output yields to the wanted ASCII representation of the message
   digest.  */
extern void *sha1_buffer (const char *buffer, size_t len, void *resblock);

#endif

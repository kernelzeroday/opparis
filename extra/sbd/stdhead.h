/*

stdhead.h

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

#ifndef STDHEAD_HXX
#define STDHEAD_HXX
#include <stdio.h>     /* standard I/O */

#ifdef __cplusplus
//#include <iostream>    /* C++ stream I/O */
//#include <iomanip.h>   /* other C++ stream stuff */
//#include <new.h>       /* C++ defs for 'new' and 'set_new_handler' */
//#include <string>      /* C++ string class */
#endif

#include <stdlib.h>    /* miscellanous definitions */
#include <stdarg.h>    /* header for variable function arguments */
#include <string.h>    /* standard string manipulation */
#include <ctype.h>     /* stardard character identification */
#include <fcntl.h>     /* ditto */
#include <time.h>      /* time functions */
#include <limits.h>    /* datatype limits */
#include <errno.h>     /* 'errno' processing */
//#include <dirent.h>    /* POSIX directory processing */
#include <sys/stat.h>  /* 'stat' function defines */

/* Various defines */

#define LNULL (0L)        /* long null constant */
/* #define EOF (-1) */    /* standard end of file */
#define TAB 9             /* tab character */
#define FA_NORMAL 0x00    /* normal file attribute */
#define EOLL 13           /* ASCII 'end of line' */
#define EOS '\0'          /* end of string marker */
#define EOL 10            /* end of line marker in batch file */
#define ALL "*.*"         /* directory global search */
#define TRUE 1            /* logic flags */
#define FALSE 0           /* ditto */
#define ESC 27            /* ASCII ESC */
#define BACKSP 8          /* ASCII backspace */
#define NO_FLAGS	0

/* platform specific defines */

/* one line from the following group of
   supported OS's should be uncommented
   based on the OS that the program will
   run under, defining 'OS_UNIX' and
   'OS_QNX' should be done in the case
   of QNX */

/* #define OS_DOS 1 */
#ifdef WIN32
#define OS_WIN32 1
/* #define OS_QNX 1 */
#else
#define OS_UNIX 1
#endif
/* #define OS_MAC 1 */

/* path separator and switch
   character based on platform */

#ifdef OS_DOS
#define PATH_SEP '\\'
#define SWITCH_CHAR '/'
#define PLATFORM_STRING "DOS"
#endif

#ifdef OS_WIN32
#define PATH_SEP '\\'
#define SWITCH_CHAR '/'
#define PLATFORM_STRING "32bit Windows"
#endif

#ifdef OS_QNX
#define PATH_SEP '/'
#define SWITCH_CHAR '-'
#define PLATFORM_STRING "QNX"
#endif

#ifdef OS_UNIX
#define PATH_SEP '/'
#define SWITCH_CHAR '-'
#define PLATFORM_STRING "Unix"

/* since there are many flavors of Unix,
   I have added a sub-platform string
   that can be quite specific, just uncomment
   one of the following or add your own
   once the port is solid */

/* #define SUB_PLATFORM_STRING "HP-UX" */
/* #define SUB_PLATFORM_STRING "AIX" */
/* #define SUB_PLATFORM_STRING "Solaris" */
#define SUB_PLATFORM_STRING "Linux"

/* Undefine one of Unix OS's below or create one.
   These are used for Unix OS specific code (which
   should not be very often) */

#define OS_UNIX_REDHAT_LINUX 1
/* #define OS_UNIX_HPUX 1 */
/* #define OS_UNIX_SOLARIS 1 */
/* #define OS_UNIX_AIX 1 */
/* #define OS_UNIX_IRIX */
#endif

#ifdef OS_MAC
#define PATH_SEP ':'
#define SWITCH_CHAR '-'
#define PLATFORM_STRING "Mac"
#endif

/* one line from the following group of
   supported interprocess communication
   methods (IPC) should be uncommented
   based on the IPC that the program will
   run under */

#define IPC_TCP 1
/* #define IPC_QNX 1 */

/* include files specific to non-Unix systems */

#ifndef OS_UNIX
#include <process.h>   /* child process control */
#include <conio.h>     /* console I/O */
#endif

/* include files specific to Unix systems */

#ifdef OS_UNIX
#include <unistd.h>
#endif

/* include files specific to DOS */

#ifdef OS_DOS
#include <io.h>
#include <dos.h>
#include <dir.h>
#include <bios.h>
#endif

/* if your compiler has 'stricmp' and 'strnicmp'
   functions built into its library (these are
   not standard ANSI), activate the next define */

#define HAS_STRICMP 1

/* global multiuser switch used for any compiler
   that cannot be supplied with a compiler define
   directive like CodeWarrior */

#define MULTIUSER 1

#endif


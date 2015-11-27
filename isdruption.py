#!/usr/bin/python env
# ISdrUpTiOn
# Auto search and silence ISIS
"""
README:

DEPENDENCIES:

- You need pygoogle, grab it from here and install it:
https://github.com/rnikhil275/pygoogle

- You also need the trunacated list of search terms:
http://pastebin.com/vyb8bjjm

Save it as 'strippedkws' in the same directory as this script.

Now just run the script and analyze the results. This saves a lot of
time because this script automatically chooses 3 keywords and searches google
for you. The results are returned to stout in the terminal. If someone wants to
help figure out what comes next, please PM me on irc.anonops.com , my sn is
shellzrus. 

"""

#choose 3 keywords

from random import randint
import os
import subprocess
from pygoogle import pygoogle
num_lines = sum(1 for line in open('strippedkws'))
print("%s lines in keyword file" % num_lines)
a = (randint(0,(num_lines)))
b = (randint(0,(num_lines)))
c = (randint(0,(num_lines)))



      
f=open('strippedkws')
lines=f.readlines()
a = (lines[a])
b = (lines[b])
c = (lines[c])


for i in a,b,c:
    print (i)

g = pygoogle(i)
g.pages = 5
print '*Found %s results*'%(g.get_result_count())
g.get_urls()
g.get_urls()
g.display_results()
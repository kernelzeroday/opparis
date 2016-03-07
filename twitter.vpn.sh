#!/bin/bash
IFS=$'\n'
hma-vpn -s >/dev/null 2>/dev/null
if [[ $? == 0 ]];then
echo "Déconnecter votre vpn avant d'agir"
exit
fi
for name in `cat $2`; do 
  echo "*************** $name ***************"
  hma-vpn -c /usr/share/hma-vpn/hmalogin -d  London  >/dev/null 2>/dev/null
  hma-vpn -s >/dev/null 2>/dev/null
  cpt=0
   res=1
  while [[ $res != 0 ]]; do
    sleep 2
    (( cpt= $cpt +1 ))
    if [[ $cpt == 20 ]];then
        echo "reload vpn"
        hma-vpn -c /usr/share/hma-vpn/hmalogin -d  London  >/dev/null 2>/dev/null
    fi
    hma-vpn -s >/dev/null 2>/dev/null
    res=$?
  done
  date 
  hma-vpn -s
  ip=$(/tmp/hma-ipcheck.sh)
  echo $ip
  notify-send "$ip"
  (./TwitterReport.py -u $name  -i $1 >/dev/null 2>/dev/null)&
  p=$!
  sleep 10
  ./TwitterReport.py -u $name  -i newlist2.txt  >/dev/null 2>/dev/null
  echo "Sortie $?"
  while ps $p >/dev/null
  do
    sleep 60
  done
  hma-vpn -x >/dev/null 2>/dev/null
  sleep 1
done
exit
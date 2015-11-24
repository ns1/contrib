#!/bin/bash

# NOTE: You must edit the next 4 lines!!
IFACE="eth0"
APIKEY="your_ns1_api_key"
ZONE="example.org"
RECORD="host.example.org"

#copied from http://www.linuxjournal.com/content/validating-ip-address-bash-script
function valid_ip()
{
  local ip=$1
  local stat=1

  if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
    OIFS=$IFS
    IFS='.'
    ip=($ip)
    IFS=$OIFS
    [[ ${ip[0]} -le 255 && ${ip[1]} -le 255 && ${ip[2]} -le 255 && ${ip[3]} -le 255 ]]
      stat=$?
  fi
  return $stat
}

#inspired by https://unix.stackexchange.com/questions/98923/programmatically-extract-private-ip-addresses
function public_ip()
{
  local ip=$1
  local stat=2

  echo $ip | grep -q -E '^(192\.168|10\.|172\.1[6789]\.|172\.2[0-9]\.|172\.3[01]\.)'
  stat=$?
  return $stat
}

function check_ip()
{
  valid_ip $1
  if [ $? -ne 0 ]; then
    echo "Couldn't find a valid IP address, your interface might be down or you failed to fill out the 4 obvious lines at the top"
    exit 1
  fi
}

IPDATA=`/sbin/ifconfig $IFACE | egrep "^[[:space:]]+inet addr:"`
if [ -z $IPDATA ]; then
  IPDATA=`/sbin/ifconfig $IFACE | egrep "^[[:space:]]+inet "`
fi
IPADDR=`echo $IPDATA | awk {'print $2'} | cut -d : -f 2`

check_ip $IPADDR

public_ip $IPADDR
if [ $? -eq 2 ]; then
  echo "This should never happen..."
  exit 2
elif [ $? -eq  1 ]; then
  IPADDR=`curl -s http://ipinfo.io/ip`
  check_ip $IPADDR
fi

curl -X POST -H "X-NSONE-Key: $APIKEY" -d '{
 "answers": [
  {
   "answer": [
    "'$IPADDR'"
   ]
  }
 ]
}' https://api.nsone.net/v1/zones/$ZONE/$RECORD/A

#!/usr/bin/python

import socket
import fcntl
import struct
import os
import time
import httplib
import json
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("apikey", help="NS1 API Key (req'd)")
    parser.add_argument("zone", help="Zone to update (req'd)")
    parser.add_argument("record", help="Record to update (req'd)")
    parser.add_argument("--iface", default="eth0", help="WAN Interface (defaults to eth0)")
    parser.add_argument("--ipfile", default="/tmp/lastip.txt", help="File to store last IP address (defaults to /tmp/lastip.txt)")
    parser.add_argument("--apihost", default="api.nsone.net", help="API Hostname (defaults to api.nsone.net)")
    parser.add_argument("--apiport", type=int, default=443, help="API Port (defaults to 443)")
    parser.add_argument("--maxival", type=int, default=3600, help="Max seconds between updates (defaults to 3600)")
    return parser.parse_args() 

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

def write_file(fileName, ipAddress):
    f = open(fileName, 'w')
    f.write(ipAddress)
    f.close

def update_dns(ns1Host, ns1Port, ns1ApiKey, zone, record, answer):
    uri = '/v1/zones/%s/%s/A' % (zone, record)
    headers = { 'X-NSONE-Key' : ns1ApiKey }
    body = { 'answers' : [ { 'answer' : [ answer ] } ] }
    conn = httplib.HTTPSConnection(ns1Host, ns1Port)
    conn.request("POST", uri, json.dumps(body), headers)
    response = conn.getresponse()
    if response.status == 200:
        print "IP Address updated to %s" % answer
    else:
        print "!!! Error updating IP address - status %s" % response.status
    conn.close()
    exit()

def main(args):
    currentIp = get_ip_address(args.iface);
    doUpdate = bool(False)

    if os.path.isfile(args.ipfile):
        # Always update if our last update was more than maxInterval
        if int(time.time()) - int(os.path.getmtime(args.ipfile)) > args.maxival:
            doUpdate = True
        # Send update if current IP differs from last IP
        f = open(args.ipfile, 'r')
        if currentIp != f.read():
            doUpdate = True
        f.close()
    else:
        doUpdate = True

    if doUpdate:
        write_file(args.ipfile, currentIp)
        update_dns(args.apihost, args.apiport, args.apikey, args.zone, args.record, currentIp)

if __name__ == "__main__":
    main(parse_args())

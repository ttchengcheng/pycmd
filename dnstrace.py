#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""record ip/hostname/ping of network traffic"""

import socket
# pylint: disable=E0611
from scapy.all import sniff, DNS, DNSQR, dnsqtypes
# pylint: enable=E0611
import tclib.cmd

CMD = tclib.cmd.INSTANCE
IP_SET = dict()


def is_valid_address(addr):
    "check whethe an address string is valid"
    try:
        socket.inet_aton(addr)
        return True
    except socket.error:
        # Not legal ip address
        return False


def lookup(addr):
    "try get hostname from ip address"

    # try to get hostname
    try:
        return socket.gethostbyaddr(addr)
    except socket.herror:
        return None, None, None


def process_dns(packet):
    "parse dns package"
    dns = packet[DNS]
    if dns.qr == 0:
        if dns.haslayer("dns"):
            query = dns[DNSQR]
            CMD.show_cmd(" < {0:56s} | ({1})".format(
                query.qname.decode('utf-8'), dnsqtypes.get(query.qtype)))
        else:
            CMD.show_error(packet.summary())

    rcount = 0
    if dns.qr == 1:
        if dns.an is not None:
            rcount = dns.ancount
        if dns.ns is not None:
            rcount = dns.nscount
        if dns.ar is not None:
            rcount += dns.arcount

        i = 1
        while i < rcount:
            ans = packet[0][i + 4]
            print(" > {0:56s} | {1}".format(
                ans.rrname.decode('utf-8'), str(ans.rdata)))
            i += 1


if __name__ == "__main__":
    sniff(filter="udp port 53", prn=process_dns)

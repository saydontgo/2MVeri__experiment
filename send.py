#!/usr/bin/env python3

import argparse
import time
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import sendp, get_if_list, get_if_hwaddr
from scapy.all import Packet, IPOption
from scapy.all import Ether, IP, UDP,TCP
from scapy.all import FieldLenField, ShortField, PacketListField, BitField
from scapy.layers.inet import _IPOption_HDR

from time import sleep


def get_if():
    ifs=get_if_list()
    iface=None # "h1-eth0"
    print(ifs)
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break
    if not iface:
        print("Cannot find interface eth1")
        exit(1)
    return iface

class SwitchTrace(Packet):
    fields_desc = [ BitField("swid", 0x0, 14),
                  BitField("inport", 0x0, 9),
                  BitField("outport", 0x0, 9)]#qdepth

    def extract_padding(self, p):
                return "", p


class IPOption_TAG(IPOption):
    name = "TAG"
    option = 1
    fields_desc = [ _IPOption_HDR,
                    BitField("length", 0, 8),
                    # BitField("bloom_filter", 0, 16),
                    BitField("prime_product", 0, 32)]

class IPOption_MRI(IPOption):
    name = "MRI"
    option = 2
    fields_desc = [ _IPOption_HDR,
                    FieldLenField("length", None, fmt="B", length_of="swtraces",  adjust=lambda pkt, l:l*2+4),
                    BitField("count", 0, 16),
                    PacketListField("swtraces",
                                   [],
                                   SwitchTrace,
                                   count_from=lambda pkt:(pkt.count*1)) ]


def get_args():
    parser = argparse.ArgumentParser(description='send parser')
    parser.add_argument('--n', help='number of packets', type=int, action="store", required=False, default=1)
    parser.add_argument('--ip', help='dst ip', type=str, action="store", required=True)
    parser.add_argument('--m', help="mode", type=str, action='store', required=False, default="prime")     
    parser.add_argument('--t', help="interval", type=float, action='store', required=False, default=0.0)     
                        
    return parser.parse_args()

def main():
    args = get_args()
    iface = get_if()

    print("sending on interface %s" % iface)
    print('start time: %s' % (time.time()))
    
    pkt1 = Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff') / IP(dst = args.ip) / UDP (sport=7777, dport=8888)
    
    pkt2 = Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff') 
    if args.m == 'tag':
        pkt2 = pkt2/ IP(dst = args.ip, options = IPOption_TAG(prime_product=1))
    elif args.m == 'mri':
        pkt2 = pkt2/ IP(dst = args.ip, options = IPOption_MRI(count=0, swtraces=[]))
    else:
        pkt2 = pkt2/ IP(dst = args.ip)
    pkt2 = pkt2/ UDP (sport=7777, dport=8888)

    pkt2.show2()
    
    # sendp(pkt2, iface=iface, verbose=False)
    
    pre_time = time.time()
    
    try:
      for i in range(args.n):
        now = time.time()
        
        if now - pre_time > args.t:
            pre_time = now
            sendp(pkt2, iface=iface, verbose=False)
        else:
            sendp(pkt1, iface=iface, verbose=False)
            
        # sleep(1)
    except KeyboardInterrupt:
        raise

if __name__ == '__main__':
    main()
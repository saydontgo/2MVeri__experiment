#!/usr/bin/env python3

import argparse
import time
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import sendp, get_if_hwaddr
from scapy.all import Ether, IP, UDP
from tools import get_if, SwitchTrace, IPOption_TAG, IPOption_MRI



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
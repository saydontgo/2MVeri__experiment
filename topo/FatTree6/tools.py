from scapy.all import get_if_list
from scapy.all import Packet, IPOption
from scapy.all import PacketListField, BitField, FieldLenField
from scapy.layers.inet import _IPOption_HDR

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
                    BitField("prime_product", 1, 32)]

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

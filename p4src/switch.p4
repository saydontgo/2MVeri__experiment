/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

#define ETH_TYPE_IPV4 0x0800
#define IP_PROTO_TCP 8w6
#define IP_PROTO_UDP 8w17
#define IP_VERSION_4 4w4
#define IPV4_IHL_MIN 4w5

#define IPV4_OPTION_TAG 5w1
#define IPV4_OPTION_MRI 5w2

#define MAX_HOPS 9
#define REPORT_MIRROR_SESSION_ID 500

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;
typedef bit<14> switchID_t;
typedef bit<9> inport_t;
typedef bit<9> outport_t;

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}

header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    diffserv;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    ip4Addr_t srcAddr;
    ip4Addr_t dstAddr;
}

header ipv4_option_t {
    bit<1> copyFlag;
    bit<2> optClass;
    bit<5> option;
}

header tag_t { 
    bit<8> length;
    // bit<16> bloom_filter;
    bit<32> prime_product;
}

header mri_t {
    bit<8> length;
    bit<16>  count;
}

header switch_t {
    switchID_t  swid;
    inport_t    inport;
    outport_t   outport;
}

header tcp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<32> seq_no;
    bit<32> ack_no;
    bit<4>  data_offset;
    bit<3>  res;
    bit<3>  ecn;
    bit<6>  ctrl;
    bit<16> window;
    bit<16> checksum;
    bit<16> urgent_ptr;
}

header udp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<16> length_;
    bit<16> checksum;
}

struct headers {
    ethernet_t         ethernet;
    ipv4_t             ipv4;
    ipv4_option_t      ipv4_option;
    tag_t              tag;
    mri_t              mri;
    switch_t[MAX_HOPS] swtraces;
    udp_t              udp;
    tcp_t              tcp;
}

struct metadata {
    bit<16>  remaining;
    bit<16>  srcPort;
    bit<16>  dstPort;
    switchID_t swid;
    bool  source;
    bool  sink;
    bool  transit;
}

error { IPHeaderTooShort }

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            ETH_TYPE_IPV4: parse_ipv4;
            default: accept;
        }
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        verify(hdr.ipv4.ihl >= 5, error.IPHeaderTooShort);
        transition select(hdr.ipv4.ihl) {
            5             : parse_next_protocol;
            default       : parse_ipv4_option;
        }
    }

    state parse_ipv4_option {
        packet.extract(hdr.ipv4_option);
        transition select(hdr.ipv4_option.option) {
            IPV4_OPTION_TAG: parse_tag;
            IPV4_OPTION_MRI: parse_mri;
            default: parse_next_protocol;
        }
    }

    state parse_tag {
        packet.extract(hdr.tag);
        transition parse_next_protocol;
    }

    state parse_mri {
        packet.extract(hdr.mri);
        meta.remaining = hdr.mri.count;
        transition select(meta.remaining) {
            0 : parse_next_protocol;
            default: parse_swtrace;
        }
    }

    state parse_swtrace {
        packet.extract(hdr.swtraces.next);
        meta.remaining = meta.remaining  - 1;
        transition select(meta.remaining) {
            0 : parse_next_protocol;
            default: parse_swtrace;
        }
    }

    state parse_next_protocol {
        transition select(hdr.ipv4.protocol) {
            IP_PROTO_TCP : parse_tcp;
            IP_PROTO_UDP : parse_udp;
            default: accept;
        }
    }

    state parse_udp {
        packet.extract(hdr.udp);
        meta.srcPort = hdr.udp.srcPort;
        meta.dstPort = hdr.udp.dstPort;
        transition accept;
    }

    state parse_tcp {
        packet.extract(hdr.tcp);
        meta.srcPort = hdr.tcp.srcPort;
        meta.dstPort = hdr.tcp.dstPort;
        transition accept;
    }  
}

control MyDeparser(packet_out packet, in headers hdr) {
    apply {           
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.ipv4_option);
        packet.emit(hdr.tag);
        packet.emit(hdr.mri);
        packet.emit(hdr.swtraces);
        packet.emit(hdr.tcp);  
        packet.emit(hdr.udp);
    }
}

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply {  }
}

control MyComputeChecksum(inout headers hdr, inout metadata meta){
    apply{
        update_checksum(
            hdr.ipv4.isValid(),
            { hdr.ipv4.version,
	          hdr.ipv4.ihl,
              hdr.ipv4.diffserv,
              hdr.ipv4.totalLen,
              hdr.ipv4.identification,
              hdr.ipv4.flags,
              hdr.ipv4.fragOffset,
              hdr.ipv4.ttl,
              hdr.ipv4.protocol,
              hdr.ipv4.srcAddr,
              hdr.ipv4.dstAddr},
            hdr.ipv4.hdrChecksum,
            HashAlgorithm.csum16
        );
    }
}

/*************************************************************************
****************  I N G R E S S   P R O C E S S I N G   ******************
*************************************************************************/
control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {
    action drop() {
        mark_to_drop(standard_metadata);
    }
    
    // ipv4 forward table
    action ipv4_forward(macAddr_t dstAddr, egressSpec_t port) {
        standard_metadata.egress_spec = port;
        standard_metadata.egress_port = port;
        
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
        hdr.ethernet.dstAddr = dstAddr;
        hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
    }

    table ipv4_lpm {
        key = {
            hdr.ipv4.dstAddr: lpm;
            standard_metadata.ingress_port:exact;
        }
        actions = {
            ipv4_forward;
            drop;
            NoAction;
        }
        size = 60024; //1024
        default_action = drop();
    }

    action int_set_source () {
        meta.source = true;
    }

    action int_set_transit () {
        meta.transit = true;
    }

    action int_set_sink () {
        meta.sink = true;
    }

    table tb_set_role {
        key = {
            standard_metadata.ingress_port: exact;
        }
        actions = {
            int_set_source;
            int_set_transit;
            int_set_sink;
            NoAction();
        }
        const default_action = NoAction();
    }

    apply {
        if (hdr.ipv4.isValid()) {
            ipv4_lpm.apply();
        }
        tb_set_role.apply();
        if(meta.source == true) {
            
        }else if(meta.sink == true) {
            
        }
    }
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/


control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {

    action drop() {
        mark_to_drop(standard_metadata);
    }

    // add path information
    action add_swtrace(switchID_t swid) { 
        hdr.mri.count = hdr.mri.count + 1;
        hdr.swtraces.push_front(1);
        // According to the P4_16 spec, pushed elements are invalid, so we need
        // to call setValid(). Older bmv2 versions would mark the new header(s)
        // valid automatically (P4_14 behavior), but starting with version 1.11,
        // bmv2 conforms with the P4_16 spec.
        hdr.swtraces[0].setValid();
        hdr.swtraces[0].swid = swid;
        hdr.swtraces[0].inport =  standard_metadata.ingress_port;
        hdr.swtraces[0].outport = standard_metadata.egress_port;

        hdr.ipv4.ihl = hdr.ipv4.ihl + 1;
        hdr.mri.length = hdr.mri.length + 4;
	    hdr.ipv4.totalLen = hdr.ipv4.totalLen + 4;
    }

    table swtrace {
        actions = { 
            add_swtrace; 
            NoAction; 
        }
        default_action = NoAction();      
    }
    
    // action add_bf(switchID_t swid) {
    //     bit<16> hash1;
    //     bit<16> hash2;
    //     bit<16> hash3;
    //     bit<16> hash4;

    //     // enum HashAlgorithm { crc32, crc32_custom, crc16, crc16_custom, random, identity, csum16, xor16 }
    //     hash(hash1, HashAlgorithm.crc16, (bit<16>)0, {swid}, (bit<32>)65535);
    //     hash(hash2, HashAlgorithm.crc32, (bit<16>)0, {swid}, (bit<32>)65535);
    //     hash(hash3, HashAlgorithm.xor16, (bit<16>)0, {swid}, (bit<32>)65535);
    //     hash(hash4, HashAlgorithm.csum16, (bit<16>)0, {swid},(bit<32>) 65535);
    //     // 1 2 4 8 16 32 ... 65535
    //     // hash1 =  1 << (hash1 & 15);

    //     hdr.tag.bloom_filter = hdr.tag.bloom_filter | hash1 | hash2 | hash3 | hash4;
    // }

    // table tbl_bf {
    //     actions = { 
    //         add_bf;
    //         NoAction; 
    //     }
    //     default_action = NoAction();   
    // }

    action prime_multiply(bit<32> switch_prime) {
        hdr.tag.prime_product = hdr.tag.prime_product * switch_prime;
    }

    table tbl_prime {
        actions = { 
            prime_multiply; 
            NoAction; 
        }
        default_action = NoAction();      
    }
    
    apply {
        // Phase 1: consistency verification
        if (hdr.tag.isValid()) {
            // tbl_bf.apply();
            tbl_prime.apply();
        }
        // Phase 2: inconsistency location
        if (hdr.mri.isValid()) {
            swtrace.apply();
        }
       
    }
}

/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

V1Switch(
    MyParser(),
    MyVerifyChecksum(),
    MyIngress(),
    MyEgress(),
    MyComputeChecksum(),
    MyDeparser()
) main;
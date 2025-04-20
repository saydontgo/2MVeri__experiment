#!/usr/bin/env python3
import sys
import time
import logging
import json
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


from scapy.all import sniff
from scapy.all import Packet
from scapy.all import IP, UDP, TCP
from tools import get_if, SwitchTrace, IPOption_TAG, IPOption_MRI
from topo import Topology

    
def load_rules(rule_path):
    rules = {}
    with open(rule_path, 'r') as json_file:
        rule_list = json.load(json_file)
        for rule in rule_list:
            key = rule['src_ip'] + '-' + rule['dst_ip']
            rules[key] = rule['path']
    return rules

def get_5tuple(pkt):
    if TCP in pkt:
        return pkt[IP].src, pkt[IP].dst, pkt[TCP].sport, pkt[TCP].dport, pkt[IP].proto
    elif UDP in pkt:    
        return pkt[IP].src, pkt[IP].dst, pkt[UDP].sport, pkt[UDP].dport, pkt[IP].proto
    
def hash_5tuple(src, sport, dst, dport, proto):
    ret = hash(src)
    ret = ret ^ hash(sport)
    ret = ret ^ hash(dst)
    ret = ret ^ hash(dport)
    ret = ret ^ hash(proto)
    return ret   

NUM = 0
bytes = 0
check_bytes = 0
end_time = time.time()
topo = Topology('topology.json')
# rules = load_rules('./topo/FatTree/rules.json')
rules = load_rules('topo/FatTree/rules.json')
# bug_num = 0
flagg = 0

def verification(pkt: Packet):
    # global bug_num
    # verification consistent
    src_ip, dst_ip, sport, dport, proto = get_5tuple(pkt)
    # print("src_ip: %s, dst_ip: %s, sport: %s, dport: %s, proto: %s" % (src_ip, dst_ip, sport, dport, proto))
    # print("rules: %s" %(rules))
    key = src_ip + '-' + dst_ip

    with open("res.txt", "a")as f: # 如果发送的是一个普通的包，res.json里面的下面三条信息将无效
        global flagg
        if key not in rules:
            print("not found src_ip: %s, dest_ip: %s in rules store.\n" % (src_ip, dst_ip))
            sys.exit()
            
        expected_path = rules[key]
        print('source-destination pair: (%s, %s), expected_path: %s\n' % (src_ip, dst_ip, expected_path))
        if IPOption_TAG in pkt:
            prime_prod = pkt['TAG'].prime_product
            # 验证质数乘积是否正确
            # TODO
            expected_prod = 1
            for node in expected_path:
                prime = topo.get_prime('s' + str(node))
                if prime == 1:
                    continue
                expected_prod = expected_prod * prime
                
            if prime_prod != expected_prod:
                if flagg != 1:
                    f.write(f'Inconsistent, time : {time.time()}\n')
                    flagg = 1
                print('Inconsistent = source-destination pair: (%s, %s), prime_prod: %s, expected_prod: %s,  time: %s\n' % (src_ip, dst_ip, prime_prod, expected_prod,  time.time()))
                # bug_num = bug_num + 1
                # if bug_num == 7:
                #     sys.exit()
            
                # 故障定位
                tmp_prod = prime_prod
                pre_switch = None
                end_switch = None
                flag = False
                path=[]
                # 确定尾部交换机
                for node in topo.get_neighbors(topo.get_id(dst_ip)):
                    tmp_prime = topo.get_prime(node)
                    if tmp_prod % tmp_prime == 0:
                        end_switch = node
                        tmp_prod /= tmp_prime
                        flag = True
                        break
                   
                if end_switch != None: 
                    path.append(int(end_switch[1:]))
                    while tmp_prod > 1:
                        flag = False
                        for node in topo.get_neighbors(end_switch):
                            if pre_switch == None or node != pre_switch:
                                prime = topo.get_prime(node)
                                if prime == 1:
                                    continue
                                if tmp_prod % prime == 0:
                                    pre_switch = end_switch
                                    end_switch = node
                                    tmp_prod /= prime
                                    path.append(int(end_switch[1:]))
                                    flag = True
                                    break
                            
                if flag :
                    print("recover success! prime_prod: %s, forward path: %s\n"% (prime_prod, path[::-1]))
                else:
                    print("Error: can't recover th actual forward path. prime product: %s\n" % (prime_prod))
                    sys.exit()
                
        elif IPOption_MRI in pkt:
            count = pkt['MRI'].count - 1
            path = []
            while (count >= 0):
                swid = pkt['MRI'].swtraces[count].swid
                inport = pkt['MRI'].swtraces[count].inport
                outport = pkt['MRI'].swtraces[count].outport
                
                # [swid, inport, outport]
                path.append(swid)
                count = count - 1
            
            found = False
            if len(path) != len(expected_path):
                found = True
            else:
                i = 0
                while i < len(path):
                    if path[i] != expected_path[i]:
                        found = True
                        break
                    i = i + 1
                    
            if found:
                if flagg != 1:
                    f.write(f'Inconsistent, time : {time.time()}\n')
                    flagg = 1
                print('Inconsistent = source-destination pair: (%s, %s), path: %s, expected_path: %s, time: %s' % (src_ip, dst_ip, path, expected_path, time.time()))
                # bug_num = bug_num + 1
                # if bug_num == 7:
                #     sys.exit()

        
def handle_pkt(pkt: Packet):
    global NUM
    global bytes
    global check_bytes
    global end_time
    
    # pkt.show2()
    
    # bandwidth 
    # NUM += 1
    # bytes += len(pkt)
    # end_time = time.time()
    
    # if IPOption_TAG in pkt:
    #     check_bytes += 4
    # elif IPOption_MRI in pkt:
    #     check_bytes += 4 * pkt['MRI'].count
    
    verification(pkt)
        
    sys.stdout.flush()

def main():
    iface = get_if()
    # args = get_args()
    print("sniffing on %s" % iface)
    sys.stdout.flush()
    sniff(iface = iface, filter='inbound', prn = lambda x: handle_pkt(x))
    
    # print('num: %s, byes: %s, check_bytes: %s, end time: %s' % (NUM, bytes, check_bytes, end_time))
    
if __name__ == '__main__':
    main()
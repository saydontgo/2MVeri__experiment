from p4utils.mininetlib.network_API import NetworkAPI
from p4utils.mininetlib.log import setLogLevel, debug, info, output, warning, error
import time
import re

def conf():
    net = NetworkAPI()

    # Network general options
    net.setLogLevel('info')
    net.enableCli()

    # Switch

    # edge switch
    net.addP4Switch('s1', cli_input='topo/FatTree/rules/s1-commands.txt')
    net.addP4Switch('s2', cli_input='topo/FatTree/rules/s2-commands.txt')
    net.addP4Switch('s3', cli_input='topo/FatTree/rules/s3-commands.txt')
    net.addP4Switch('s4', cli_input='topo/FatTree/rules/s4-commands.txt')
    net.addP4Switch('s5', cli_input='topo/FatTree/rules/s5-commands.txt')
    net.addP4Switch('s6', cli_input='topo/FatTree/rules/s6-commands.txt')
    net.addP4Switch('s7', cli_input='topo/FatTree/rules/s7-commands.txt')
    net.addP4Switch('s8', cli_input='topo/FatTree/rules/s8-commands.txt')

    # aggregate switch
    net.addP4Switch('s9', cli_input='topo/FatTree/rules/s9-commands.txt')
    net.addP4Switch('s10', cli_input='topo/FatTree/rules/s10-commands.txt')
    net.addP4Switch('s11', cli_input='topo/FatTree/rules/s11-commands.txt')
    net.addP4Switch('s12', cli_input='topo/FatTree/rules/s12-commands.txt')
    net.addP4Switch('s13', cli_input='topo/FatTree/rules/s13-commands.txt')
    net.addP4Switch('s14', cli_input='topo/FatTree/rules/s14-commands.txt')
    net.addP4Switch('s15', cli_input='topo/FatTree/rules/s15-commands.txt')
    net.addP4Switch('s16', cli_input='topo/FatTree/rules/s16-commands.txt')

    # core switch 
    net.addP4Switch('s17', cli_input='topo/FatTree/rules/s17-commands.txt')
    net.addP4Switch('s18', cli_input='topo/FatTree/rules/s18-commands.txt')
    net.addP4Switch('s19', cli_input='topo/FatTree/rules/s19-commands.txt')
    net.addP4Switch('s20', cli_input='topo/FatTree/rules/s20-commands.txt')

    net.setP4SourceAll('p4src/switch.p4')

    # Host
    net.addHost('h1')
    net.addHost('h2')
    net.addHost('h3')
    net.addHost('h4')
    net.addHost('h5')
    net.addHost('h6')
    net.addHost('h7')
    net.addHost('h8')
    net.addHost('h9')
    net.addHost('h10')
    net.addHost('h11')
    net.addHost('h12')
    net.addHost('h13')
    net.addHost('h14')
    net.addHost('h15')
    net.addHost('h16')

    # core Link
    net.addLink('s1', 's9')
    net.addLink('s1', 's10')
    net.addLink('s2', 's9')
    net.addLink('s2', 's10')

    net.addLink('s3', 's11')
    net.addLink('s3', 's12')
    net.addLink('s4', 's11')
    net.addLink('s4', 's12')

    net.addLink('s5', 's13')
    net.addLink('s5', 's14')
    net.addLink('s6', 's13')
    net.addLink('s6', 's14')

    net.addLink('s7', 's15')
    net.addLink('s7', 's16')
    net.addLink('s8', 's15')
    net.addLink('s8', 's16')

    # aggregate Link
    net.addLink('s17', 's9')
    net.addLink('s17', 's11')
    net.addLink('s17', 's13')
    net.addLink('s17', 's15')

    net.addLink('s18', 's9')
    net.addLink('s18', 's11')
    net.addLink('s18', 's13')
    net.addLink('s18', 's15')

    net.addLink('s19', 's10')
    net.addLink('s19', 's12')
    net.addLink('s19', 's14')
    net.addLink('s19', 's16')

    net.addLink('s20', 's10')
    net.addLink('s20', 's12')
    net.addLink('s20', 's14')
    net.addLink('s20', 's16')

    # host link
    net.addLink('s1', 'h1')
    net.addLink('s1', 'h2')
    net.addLink('s2', 'h3')
    net.addLink('s2', 'h4')
    net.addLink('s3', 'h5')
    net.addLink('s3', 'h6')
    net.addLink('s4', 'h7')
    net.addLink('s4', 'h8')
    net.addLink('s5', 'h9')
    net.addLink('s5', 'h10')
    net.addLink('s6', 'h11')
    net.addLink('s6', 'h12')
    net.addLink('s7', 'h13')
    net.addLink('s7', 'h14')
    net.addLink('s8', 'h15')
    net.addLink('s8', 'h16')


    # Assignment strategy
    net.mixed()
    # Nodes general options
    # net.enableCpuPortAll()
    # net.enablePcapDumpAll()
    # net.enableLogAll()

    return net


def d2h(d):
    if d > 15:
        return f'{hex(d)[2:]}'
    return f'0{hex(d)[2:]}'

def hex_IP(ip):
    res = ""
    tmp = ""
    for s in ip:
        if s == '.':
            res += d2h(int(tmp))
            tmp = ""
        else:
            tmp += s
    if tmp != "":
        res += d2h(int(tmp))
    return res


def modify_switch(net, swid, dst_host, dst_swid):
    cur_sw = net.net.get(swid)
    dst_sw = net.net.get(dst_swid)
    dst_port = None

    # 获取交换机连接的端口信息
    for intf in cur_sw.intfList():
        if intf.name != 'lo':
            peer = intf.link.intf2 if intf.link.intf1 == intf else intf.link.intf1
            if peer.node == dst_sw:
                dst_port = re.findall("eth(.*)", intf.name)[0]
    if dst_port == None: 
        info(f'These two switches are not neighbours! You can\'t modify switch {swid}.\n')
        return False
    
    # 将每一条有关该目的地主机的流表进行修改
    h = net.net.get(dst_host)
    thriftPort = 9089+int(swid[1:])
    try:
        output = net.net.get(swid).cmd(f'echo "table_dump MyIngress.ipv4_lpm" | simple_switch_CLI --thrift-port {thriftPort}')
    except Exception as e:
        error(f"Execution of your command failed. Detailed info is as follow:{e}\n")
        return False
    handle = None
    hexIP = hex_IP(h.IP())
    for line in output.strip().split('\n'):
        if "Dumping entry" in line:
            handle = int(line[16:], 16)
        if hexIP in line:
            if handle == None:
                continue
            cmd = f'echo "table_modify ipv4_lpm ipv4_forward {handle} {h.MAC()} {dst_port}" | simple_switch_CLI --thrift-port {thriftPort}'
            res = net.net.get(swid).cmd(cmd)
            handle = None
            info('modify results:\n' + res + '\n')
    with open("res.txt", 'a') as f:
        f.write('time: %s\n' % (time.time()))

    return True

if __name__ == '__main__':
    net = conf()
    # Start the network
    net.startNetwork()
    # net.net.get('h5').cmd('./topo/FatTree6/receive.py &')
    # time.sleep(5)
    # modify_switch(net, 's2', 'h5', 's10')
    # net.net.get('h4').cmd('./topo/FatTree6/send.py --n 2000 --ip 10.0.3.5 --t 0.01')
    # time.sleep(2)
    # 修改流表

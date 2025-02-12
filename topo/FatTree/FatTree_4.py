from p4utils.mininetlib.network_API import NetworkAPI

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

# Start the network
net.startNetwork()
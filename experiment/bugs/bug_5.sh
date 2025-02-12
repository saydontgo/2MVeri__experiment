#!/bin/bash
echo $(date +%s.%N)

# 10.0.1.1 - 10.0.8.16 
echo "================================ -- S1 10 -- =====================================\n"
simple_switch_CLI --thrift-port 9090 --thrift-ip 127.0.0.1 --pre SimplePreLAG <<EOD
table_modify MyIngress.ipv4_lpm MyIngress.ipv4_forward 20 00:00:0a:00:08:10 3
EOD

# 10.0.2.4 - 10.0.8.16 
echo "================================ -- S1 10 -- =====================================\n"
simple_switch_CLI --thrift-port 9091 --thrift-ip 127.0.0.1 --pre SimplePreLAG <<EOD
table_modify MyIngress.ipv4_lpm MyIngress.ipv4_forward 35 00:00:0a:00:08:10 3
EOD

# 10.0.3.5 - 10.0.8.16 
echo "================================ -- S1 10 -- =====================================\n"
simple_switch_CLI --thrift-port 9092 --thrift-ip 127.0.0.1 --pre SimplePreLAG <<EOD
table_modify MyIngress.ipv4_lpm MyIngress.ipv4_forward 20 00:00:0a:00:08:10 3
EOD

# 10.0.5.9 - 10.0.8.16 
echo "================================ -- S1 10 -- =====================================\n"
simple_switch_CLI --thrift-port 9094 --thrift-ip 127.0.0.1 --pre SimplePreLAG <<EOD
table_modify MyIngress.ipv4_lpm MyIngress.ipv4_forward 20 00:00:0a:00:08:10 3
EOD

# 10.0.6.12 - 10.0.8.16 
echo "================================ -- S1 10 -- =====================================\n"
simple_switch_CLI --thrift-port 9095 --thrift-ip 127.0.0.1 --pre SimplePreLAG <<EOD
table_modify MyIngress.ipv4_lpm MyIngress.ipv4_forward 35 00:00:0a:00:08:10 3
EOD


# time=$(date +"%M:%S.%6N")
# echo "$time" > ./experiment/bug_insertion.log
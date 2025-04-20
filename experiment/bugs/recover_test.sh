#! /bin/bash
echo 'table_modify ipv4_lpm ipv4_forward 24 00:00:0a:00:03:05 3' | simple_switch_CLI --thrift-port 9091
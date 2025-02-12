
ifndef RULE_NUMBER
RULE_NUMBER = 250
endif

#config forward rules
RULE_DIR 		:= rules
RULE_DIR_JSON 	:= ${RULE_DIR}/rules_$(RULE_NUMBER)

all: run

# start network
run:
	python3 network.py

# consistent check
consistent-check:
	python3 receive_check.py --rule_dir runtime_rules/default/ --output_file experiment/output

# loop check
loop-check:
	python3 receive_loop.py --output_file experiment/loop_output

# #gnerate forward rules for all switch
dump_rules:
	python3 runtime_rules/dummy_rules.py --topo mininet/topology.json --rule_dir runtime_rules --rule_num 250

#build rules for all switch
install_rules:${RULE_DIR_JSON}
	python3 rules/install_rules.py --rules $(RULE_NUMBER)

${RULE_DIR_JSON}:
	python3 rules/dummy_rules.py --rules $(RULE_NUMBER) 

stop:
	sudo mn -c


clean: stop
	rm -f *.pcap
	rm -rf $(PCAP_DIR) $(LOG_DIR) $(RULE_DIR)/rule*

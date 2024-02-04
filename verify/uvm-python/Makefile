PLUSARGS += "+UVM_VERBOSITY=UVM_MEDIUM"
TOPLEVEL := top
MODULE   ?= top_module
VERILOG_SOURCES ?=  $(PWD)/top.v $(PWD)/../../hdl/rtl/bus_wrappers/EF_UART_APB.v  $(PWD)/../../hdl/rtl/EF_UART.v
RTL_MACROS ?= ""
YAML_FILE = $(PWD)/../../EF_UART.yaml
MAKEFLAGS += --no-print-directory

# include $(shell cocotb-config --makefiles)/Makefile.sim

# List of tests
TESTS := TX_StressTest RX_StressTest LoopbackTest PrescalarStressTest LengthParityTXStressTest LengthParityRXStressTest WriteReadRegsTest

# Variable for tag - set this as required
SIM_TAG ?= default_tag

# Define SIM_PATH variable
SIM_PATH := $(PWD)/sim/$(SIM_TAG)

# Target to run all tests
run_all_tests:
	$(foreach test,$(TESTS), \
		$(MAKE) run_test UVM_TEST=$(test) SIM_TAG=$(SIM_TAG); \
	)
	$(MAKE) run_merge_coverage

RED=\033[0;31m
GREEN=\033[0;32m
YELLOW=\033[0;33m
NC=\033[0m # No Color

# Target to run a single test
run_test:
	@echo "Running test: $(UVM_TEST) with tag: $(SIM_TAG)"
	@mkdir -p $(SIM_PATH)/compilation
	@mkdir -p $(SIM_PATH)/$(UVM_TEST)
	@if [ ! -f "$(SIM_PATH)/compilation/sim.vvp" ]; then \
        echo "Compiling since sim.vvp does not exist..."; \
        iverilog -g2012 -Ttyp $(RTL_MACROS) $(VERILOG_SOURCES) -o $(SIM_PATH)/compilation/sim.vvp -s top; \
    fi
	@$(MAKE) create_top_py UVM_TEST=$(UVM_TEST)
	@cd $(SIM_PATH)/$(UVM_TEST) &&  MODULE=top_module vvp -M $(shell cocotb-config --lib-dir) -m $(shell cocotb-config --lib-name vpi icarus) $(SIM_PATH)/compilation/sim.vvp +UVM_TESTNAME=$(UVM_TEST) +TEST_PATH=$(SIM_PATH)/$(UVM_TEST) +YAML_FILE=$(YAML_FILE) COCOTB_RESULTS_FILE=$(SIM_PATH)/$(UVM_TEST)/results.xml > $(SIM_PATH)/$(UVM_TEST)/test.log 2>&1
	@echo "Checking test results..."
	@if grep -q "UVM TEST FAIL" $(SIM_PATH)/$(UVM_TEST)/test.log; then \
		echo "Test Failed" > $(SIM_PATH)/$(UVM_TEST)/failed; \
		echo "$(RED)Test $(UVM_TEST) Failed$(NC)" ; \
	elif grep -q "UVM TEST PASSED" $(SIM_PATH)/$(UVM_TEST)/test.log; then \
		echo "Test Passed" > $(SIM_PATH)/$(UVM_TEST)/passed; \
		echo "$(GREEN)Test $(UVM_TEST) Passed$(NC)" ; \
	else \
		echo "Test Result Unknown" > $(SIM_PATH)/$(UVM_TEST)/unknown; \
		echo "$(YELLOW)Test $(UVM_TEST) Result Unknown$(NC)" ; \
	fi

create_top_py:
	@echo "from os import path" > $(SIM_PATH)/$(UVM_TEST)/top_module.py
	@echo "import sys" >> $(SIM_PATH)/$(UVM_TEST)/top_module.py
	@echo "sys.path.append(path.abspath('$(PWD)'))" >> $(SIM_PATH)/$(UVM_TEST)/top_module.py
	@echo "from test_lib import *" >> $(SIM_PATH)/$(UVM_TEST)/top_module.py


run_merge_coverage:
	@python3 $(PWD)/merge_cov.py $(SIM_PATH)

clean_sim:
	@echo "Cleaning up..."
	@rm -rf $(PWD)/sim

# @$(MAKE) all SIM_BUILD=$(SIM_PATH)/sim_build PLUSARGS+="+UVM_TESTNAME=$(UVM_TEST) +TEST_PATH=$(SIM_PATH)/$(UVM_TEST)" COCOTB_RESULTS_FILE=$(SIM_PATH)/$(UVM_TEST)/results.xml | tee $(SIM_PATH)/$(UVM_TEST)/test.log

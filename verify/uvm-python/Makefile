PLUSARGS += "+UVM_VERBOSITY=UVM_HIGH"
TOPLEVEL := top
MODULE   ?= top_module
VERILOG_INCLUDE_DIRS = $(PWD)/IP_Utilities/rtl $(PWD)/../../hdl/rtl $(PWD)/../../hdl/rtl/bus_wrappers
VERILOG_SOURCES ?=  $(PWD)/top.v  $(PWD)/IP_Utilities/rtl/aucohl_lib.v $(PWD)/IP_Utilities/rtl/aucohl_rtl.vh $(PWD)/../../hdl/rtl/bus_wrappers/EF_UART_AHBL.pp.v $(PWD)/../../hdl/rtl/bus_wrappers/EF_UART_APB.pp.v  $(PWD)/../../hdl/rtl/EF_UART.v 
RTL_MACROS += ""
BUS_TYPE ?= APB
ifeq ($(BUS_TYPE),APB)
    RTL_MACROS += -DBUS_TYPE_APB
else ifeq ($(BUS_TYPE),AHB)
    RTL_MACROS += -DBUS_TYPE_AHB
else ifeq ($(BUS_TYPE),WISHBONE)
    RTL_MACROS += -DBUS_TYPE_WISHBONE
endif
# RTL_MACROS ?= "-DSKIP_WAVE_DUMP"
YAML_FILE = $(PWD)/../../EF_UART.yaml
MAKEFLAGS += --no-print-directory

# List of tests
TESTS := TX_StressTest RX_StressTest LoopbackTest PrescalarStressTest LengthParityTXStressTest LengthParityRXStressTest WriteReadRegsTest
# TESTS := TX_StressTest 

# Variable for tag - set this as required
SIM_TAG ?= default_tag

# Define SIM_PATH variable
SIM_PATH := $(PWD)/sim/$(SIM_TAG)

# Check and clone EF_UVM repository at the beginning of the Makefile execution

clone_ip_util := $(shell if [ ! -d "IP_Utilities" ]; then \
	echo "Cloning the IP_Utilities repository..."; \
	git clone https://github.com/shalan/IP_Utilities.git; \
fi;)

clone_ef_uvm := $(shell if [ ! -d "EF_UVM" ]; then \
	echo "Cloning the EF_UVM repository..."; \
	git clone https://github.com/M0stafaRady/EF_UVM.git; \
fi;)



include EF_UVM/Makefile.test

PLUSARGS += "+UVM_VERBOSITY=UVM_HIGH"
TOPLEVEL := top
MODULE   ?= top_module
VERILOG_SOURCES ?=  $(PWD)/top.v $(PWD)/../../hdl/rtl/bus_wrappers/EF_UART_APB.v  $(PWD)/../../hdl/rtl/EF_UART.v
RTL_MACROS ?= ""
# RTL_MACROS ?= "-DSKIP_WAVE_DUMP"
YAML_FILE = $(PWD)/../../EF_UART.yaml
MAKEFLAGS += --no-print-directory

# List of tests
TESTS := TX_StressTest RX_StressTest LoopbackTest PrescalarStressTest LengthParityTXStressTest LengthParityRXStressTest WriteReadRegsTest
# TESTS := WriteReadRegsTest 

# Variable for tag - set this as required
SIM_TAG ?= default_tag

# Define SIM_PATH variable
SIM_PATH := $(PWD)/sim/$(SIM_TAG)

include EF_UVM/Makefile.test

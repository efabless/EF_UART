
# include ../MakefileCommon.mk

# SIM_ARGS = ""
# PLUSARGS += "+UVM_VERBOSITY=UVM_HIGH"
TOPLEVEL := top
MODULE   ?= test_lib
VERILOG_SOURCES ?=  $(PWD)/top.v $(PWD)/../../hdl/rtl/bus_wrappers/EF_UART_APB.v  $(PWD)/../../hdl/rtl/EF_UART.v
include $(shell cocotb-config --makefiles)/Makefile.sim

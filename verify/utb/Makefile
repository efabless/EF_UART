SOURCE = ../../hdl/rtl/EF_UART.v
SOURCE_APB =  ../../hdl/rtl/bus_wrappers/EF_UART_APB.v
SOURCE_AHBL = ../../hdl/rtl/bus_wrappers/EF_UART_AHBL.v
TESTBENCH_APB = EF_UART_APB_tb.v
TESTBENCH_AHBL = EF_UART_AHBL_tb.v
RTL_LIB = ../../../IP_Utilities/rtl/aucohl_lib.v
WRAPPER_HEADER_DIR = ../../../IP_Utilities/generators/

APB-RTL: 
	iverilog -o run.vvp -I../../../IP_Utilities/verify/ -I$(WRAPPER_HEADER_DIR) $(RTL_LIB)  $(SOURCE) $(SOURCE_APB) $(TESTBENCH_APB)
	./run.vvp

AHBL-RTL: 
	iverilog -o run.vvp -I../../../IP_Utilities/verify/ -I$(WRAPPER_HEADER_DIR) $(RTL_LIB)  $(SOURCE) $(SOURCE_AHBL) $(TESTBENCH_AHBL)
	./run.vvp

clean:
	rm -f *.vvp
	rm -f *.vcd

all: APB-RTL
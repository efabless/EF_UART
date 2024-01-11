SOURCE = ../../hdl/rtl/EF_UART.v ../../hdl/rtl/bus_wrappers/EF_UART_APB.v
TESTBENCH = EF_UART_APB_tb.v
RTL_LIB = ../../IP_Utilities/rtl/aucohl_lib.vh
WRAPPER_HEADER_DIR = ../../hdl/rtl/bus_wrappers/

APB-RTL: 
	iverilog -o run.vvp -I../../IP_Utilities/verify/ -I$(WRAPPER_HEADER_DIR) $(RTL_LIB)  $(SOURCE) $(TESTBENCH)
	./run.vvp

clean:
	rm -f *.vvp
	rm -f *.vcd

all: APB-RTL
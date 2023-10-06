SIM-RTL:
	iverilog  -s EF_UART_apb_tb ../../hdl/rtl/EF_UART.v ../../hdl/rtl/bus_wrappers/EF_UART_apb.v EF_UART_apb_tb.v
	./a.out

SIM-GL:
	iverilog  -s EF_UART_apb_tb ../../hdl/rtl/EF_UART.v ../../hdl/gl/sky130/EF_UART_apb.v EF_UART_apb_tb.v ../../util/tech/sky130/sky130_hd.v
	./a.out

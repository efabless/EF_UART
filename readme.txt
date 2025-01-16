/*
	Copyright 2024 Efabless Corp.

	Author: Efabless Corp. (ip_admin@efabless.com)

	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

	    http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.

*/

IP_name: EF_UART
Author: Efabless
Directory Structure:

    - fw 
        - **EF_UART_regs.h**: Header file containing the register definitions for the EF_UART interface.
        - **EF_UART.c**: C source file implementing the low-level driver functions for the EF_UART.
        - **EF_UART.h**: Header file declaring the API functions and data structures for the EF_UART driver.
        - **DEVICE_DRIVER.pdf**: Documentation for users to understand how to use the EF_UART driver and interface with the IP.

    - hdl 
        - rtl 
            - **EF_UART.v**: Verilog source code for the EF_UART design, including the core logic of the UART module.
            - **bus_wrappers**
                - **EF_UART_AHBL.v**: Verilog wrapper to interface the EF_UART with the AMBA High-performance Bus (AHB-Lite) protocol.
                - **EF_UART_APB.v**: Verilog wrapper to interface the EF_UART with the Advanced Peripheral Bus (APB) protocol.
                - **EF_UART_WB.v**: Verilog wrapper to interface the EF_UART with the Wishbone bus protocol.
            - **dft**
                - **EF_UART_AHBL_DFT.v**: Verilog wrapper with Design for Test (DFT) support specific to the AHB-Lite interface of the EF_UART .
                - **EF_UART_APB_DFT.v**: Verilog wrapper with DFT support specific to the APB interface of the EF_UART.
                - **EF_UART_WB_DFT.v**: Verilog wrapper with DFT support specific to the Wishbone interface of the EF_UART.

    - ip 
        - **dependencies.json**: Used by IPM [Do NOT EDIT OR DELETE].
    
    - **EF_UART.pdf**: Comprehensive documentation for the EF_UART, including its features, configuration, and usage.
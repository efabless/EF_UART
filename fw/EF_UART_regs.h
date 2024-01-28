/*
	Copyright 2024 Efabless Corp.

	Author: Mohamed Shalan (mshalan@aucegypt.edu)

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

/*! \file EF_UART_regs.h
    \brief C header file which contains UART registers definition 
    
*/

#ifndef EF_UARTREGS_H
#define EF_UARTREGS_H

#ifndef IO_TYPES
#define IO_TYPES
#define   __R     volatile const unsigned int
#define   __W     volatile       unsigned int
#define   __RW    volatile       unsigned int
#endif

#define EF_UART_CTRL_REG_EN_BIT	0
#define EF_UART_CTRL_REG_EN_MASK	0x1
#define EF_UART_CTRL_REG_TXEN_BIT	1
#define EF_UART_CTRL_REG_TXEN_MASK	0x2
#define EF_UART_CTRL_REG_RXEN_BIT	2
#define EF_UART_CTRL_REG_RXEN_MASK	0x4
#define EF_UART_CTRL_REG_LPEN_BIT	3
#define EF_UART_CTRL_REG_LPEN_MASK	0x8
#define EF_UART_CTRL_REG_GFEN_BIT	4
#define EF_UART_CTRL_REG_GFEN_MASK	0x10
#define EF_UART_CFG_REG_WLEN_BIT	0
#define EF_UART_CFG_REG_WLEN_MASK	0xf
#define EF_UART_CFG_REG_STP2_BIT	4
#define EF_UART_CFG_REG_STP2_MASK	0x10
#define EF_UART_CFG_REG_PARITY_BIT	5
#define EF_UART_CFG_REG_PARITY_MASK	0xe0
#define EF_UART_CFG_REG_TIMEOUT_BIT	8
#define EF_UART_CFG_REG_TIMEOUT_MASK	0x3f00
#define EF_UART_FIFOCTRL_REG_TXLT_BIT	0
#define EF_UART_FIFOCTRL_REG_TXLT_MASK	0xf
#define EF_UART_FIFOCTRL_REG_RXLT_BIT	8
#define EF_UART_FIFOCTRL_REG_RXLT_MASK	0xf00
#define EF_UART_FIFOS_REG_RXL_BIT	0
#define EF_UART_FIFOS_REG_RXL_MASK	0xf
#define EF_UART_FIFOS_REG_TXL_BIT	8
#define EF_UART_FIFOS_REG_TXL_MASK	0xf00

#define EF_UART_TXE_FLAG	0x1
#define EF_UART_RXF_FLAG	0x2
#define EF_UART_TXB_FLAG	0x4
#define EF_UART_RXA_FLAG	0x8
#define EF_UART_BRK_FLAG	0x10
#define EF_UART_MATCH_FLAG	0x20
#define EF_UART_FE_FLAG	0x40
#define EF_UART_PRE_FLAG	0x80
#define EF_UART_OR_FLAG	0x100
#define EF_UART_RTO_FLAG	0x200

typedef struct _EF_UART_TYPE_ {
	__R 	RXDATA;
	__W 	TXDATA;
	__W 	PR;
	__W 	CTRL;
	__W 	CFG;
	__W 	FIFOCTRL;
	__R 	FIFOS;
	__W 	MATCH;
	__R 	reserved[952];
	__RW	im;
	__R 	mis;
	__R 	ris;
	__W 	icr;
} EF_UART_TYPE;

#endif


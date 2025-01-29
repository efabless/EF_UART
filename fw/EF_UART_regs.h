/*
	Copyright 2024 Efabless Corp.

	Author: Mohamed Shalan (mshalan@efabless.com)

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

#ifndef EF_UARTREGS_H
#define EF_UARTREGS_H


/******************************************************************************
* Includes
******************************************************************************/
#include "EF_Driver_Common.h"


/******************************************************************************
* Macros and Constants
******************************************************************************/
#ifndef IO_TYPES
#define IO_TYPES
#define   __R     volatile const uint32_t
#define   __W     volatile       uint32_t
#define   __RW    volatile       uint32_t
#endif

#define EF_UART_RXDATA_REG_RXDATA_BIT	((uint32_t)0)
#define EF_UART_RXDATA_REG_RXDATA_MASK	((uint32_t)0x1ff)
#define EF_UART_RXDATA_REG_MAX_VALUE	((uint32_t)0x1FF)

#define EF_UART_TXDATA_REG_TXDATA_BIT	((uint32_t)0)
#define EF_UART_TXDATA_REG_TXDATA_MASK	((uint32_t)0x1ff)
#define EF_UART_TXDATA_REG_MAX_VALUE	((uint32_t)0x1FF)

#define EF_UART_PR_REG_PR_BIT	((uint32_t)0)
#define EF_UART_PR_REG_PR_MASK	((uint32_t)0xffff)
#define EF_UART_PR_REG_MAX_VALUE	((uint32_t)0xFFFF)

#define EF_UART_CTRL_REG_EN_BIT	((uint32_t)0)
#define EF_UART_CTRL_REG_EN_MASK	((uint32_t)0x1)
#define EF_UART_CTRL_REG_TXEN_BIT	((uint32_t)1)
#define EF_UART_CTRL_REG_TXEN_MASK	((uint32_t)0x2)
#define EF_UART_CTRL_REG_RXEN_BIT	((uint32_t)2)
#define EF_UART_CTRL_REG_RXEN_MASK	((uint32_t)0x4)
#define EF_UART_CTRL_REG_LPEN_BIT	((uint32_t)3)
#define EF_UART_CTRL_REG_LPEN_MASK	((uint32_t)0x8)
#define EF_UART_CTRL_REG_GFEN_BIT	((uint32_t)4)
#define EF_UART_CTRL_REG_GFEN_MASK	((uint32_t)0x10)
#define EF_UART_CTRL_REG_MAX_VALUE	((uint32_t)0x1F)

#define EF_UART_CFG_REG_WLEN_BIT	((uint32_t)0)
#define EF_UART_CFG_REG_WLEN_MASK	((uint32_t)0xf)
#define EF_UART_CFG_REG_STP2_BIT	((uint32_t)4)
#define EF_UART_CFG_REG_STP2_MASK	((uint32_t)0x10)
#define EF_UART_CFG_REG_PARITY_BIT	((uint32_t)5)
#define EF_UART_CFG_REG_PARITY_MASK	((uint32_t)0xe0)
#define EF_UART_CFG_REG_TIMEOUT_BIT	((uint32_t)8)
#define EF_UART_CFG_REG_TIMEOUT_MASK	((uint32_t)0x3f00)
#define EF_UART_CFG_REG_MAX_VALUE	((uint32_t)0x3FFF)

#define EF_UART_MATCH_REG_MATCH_BIT	((uint32_t)0)
#define EF_UART_MATCH_REG_MATCH_MASK	((uint32_t)0x1ff)
#define EF_UART_MATCH_REG_MAX_VALUE	((uint32_t)0x1FF)

#define EF_UART_RX_FIFO_LEVEL_REG_LEVEL_BIT	((uint32_t)0)
#define EF_UART_RX_FIFO_LEVEL_REG_LEVEL_MASK	((uint32_t)0xf)
#define EF_UART_RX_FIFO_LEVEL_REG_MAX_VALUE	((uint32_t)0xF)

#define EF_UART_RX_FIFO_THRESHOLD_REG_THRESHOLD_BIT	((uint32_t)0)
#define EF_UART_RX_FIFO_THRESHOLD_REG_THRESHOLD_MASK	((uint32_t)0xf)
#define EF_UART_RX_FIFO_THRESHOLD_REG_MAX_VALUE	((uint32_t)0xF)

#define EF_UART_RX_FIFO_FLUSH_REG_FLUSH_BIT	((uint32_t)0)
#define EF_UART_RX_FIFO_FLUSH_REG_FLUSH_MASK	((uint32_t)0x1)
#define EF_UART_RX_FIFO_FLUSH_REG_MAX_VALUE	((uint32_t)0x1)

#define EF_UART_TX_FIFO_LEVEL_REG_LEVEL_BIT	((uint32_t)0)
#define EF_UART_TX_FIFO_LEVEL_REG_LEVEL_MASK	((uint32_t)0xf)
#define EF_UART_TX_FIFO_LEVEL_REG_MAX_VALUE	((uint32_t)0xF)

#define EF_UART_TX_FIFO_THRESHOLD_REG_THRESHOLD_BIT	((uint32_t)0)
#define EF_UART_TX_FIFO_THRESHOLD_REG_THRESHOLD_MASK	((uint32_t)0xf)
#define EF_UART_TX_FIFO_THRESHOLD_REG_MAX_VALUE	((uint32_t)0xF)

#define EF_UART_TX_FIFO_FLUSH_REG_FLUSH_BIT	((uint32_t)0)
#define EF_UART_TX_FIFO_FLUSH_REG_FLUSH_MASK	((uint32_t)0x1)
#define EF_UART_TX_FIFO_FLUSH_REG_MAX_VALUE	((uint32_t)0x1)


#define EF_UART_TXE_FLAG	((uint32_t)0x1)
#define EF_UART_RXF_FLAG	((uint32_t)0x2)
#define EF_UART_TXB_FLAG	((uint32_t)0x4)
#define EF_UART_RXA_FLAG	((uint32_t)0x8)
#define EF_UART_BRK_FLAG	((uint32_t)0x10)
#define EF_UART_MATCH_FLAG	((uint32_t)0x20)
#define EF_UART_FE_FLAG	((uint32_t)0x40)
#define EF_UART_PRE_FLAG	((uint32_t)0x80)
#define EF_UART_OR_FLAG	((uint32_t)0x100)
#define EF_UART_RTO_FLAG	((uint32_t)0x200)



/******************************************************************************
* Typedefs and Enums
******************************************************************************/
typedef struct _EF_UART_TYPE_ {
	__R 	RXDATA;
	__W 	TXDATA;
	__W 	PR;
	__W 	CTRL;
	__W 	CFG;
	__R 	reserved_0[2];
	__W 	MATCH;
	__R 	reserved_1[16248];
	__R 	RX_FIFO_LEVEL;
	__W 	RX_FIFO_THRESHOLD;
	__W 	RX_FIFO_FLUSH;
	__R 	reserved_2[1];
	__R 	TX_FIFO_LEVEL;
	__W 	TX_FIFO_THRESHOLD;
	__W 	TX_FIFO_FLUSH;
	__R 	reserved_3[57];
	__RW	IM;
	__R 	MIS;
	__R 	RIS;
	__W 	IC;
	__W 	GCLK;
} EF_UART_TYPE;


typedef EF_UART_TYPE* EF_UART_TYPE_PTR;



/******************************************************************************
* Function Prototypes
******************************************************************************/



/******************************************************************************
* External Variables
******************************************************************************/




#endif // EF_UARTREGS_H

/******************************************************************************
* End of File
******************************************************************************/

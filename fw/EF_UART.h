/*
	Copyright 2025 Efabless Corp.


	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

	    www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.

*/


/*! \file EF_UART.h
    \brief C header file for UART APIs which contains the function prototypes 
    
*/


#ifndef EF_UART_H
#define EF_UART_H


/******************************************************************************
* Includes
******************************************************************************/
#include "EF_UART_regs.h"
#include "EF_Driver_Common.h"


/******************************************************************************
* Macros and Constants
******************************************************************************/
#define EF_UART_DataLength_MIN_VALUE            ((uint32_t)0x00000005)  // This UART IP only supports data length from 5 to 9 bits
#define EF_UART_DataLength_MAX_VALUE            ((uint32_t)0x00000009)  // This UART IP only supports data length from 5 to 9 bits
#define EF_UART_CFG_REG_TIMEOUT_MAX_VALUE       ((uint32_t)0x0000003F)  // The CFG register timeout field is 6 bits


/******************************************************************************
* Typedefs and Enums
******************************************************************************/

enum parity_type {NONE = 0, ODD = 1, EVEN = 2, STICKY_0 = 4, STICKY_1 = 5};



/******************************************************************************
* Function Prototypes
******************************************************************************/

//! sets the GCLK enable bit in the UART register to a certain value
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [in] value The value of the GCLK enable bit
        
        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */

EF_DRIVER_STATUS EF_UART_setGclkEnable (EF_UART_TYPE_PTR uart, uint32_t value);

//! enables using uart by setting "en" bit in the control register to 1 
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        
        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_enable(EF_UART_TYPE_PTR uart);


//! disables using uart by clearing "en" bit in the control register
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        
        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */  
EF_DRIVER_STATUS EF_UART_disable(EF_UART_TYPE_PTR uart);


//! enables using uart RX by setting uart "rxen" bit in the control register to 1 
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        
        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_enableRx(EF_UART_TYPE_PTR uart);


//! disables using uart RX by clearing uart "rxen" bit in the control register
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        
        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_disableRx(EF_UART_TYPE_PTR uart);


//! enables using uart TX by setting uart "txen" bit in the control register to 1 
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        
        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_enableTx(EF_UART_TYPE_PTR uart);


//! disables using uart TX by clearing uart "txen" bit in the control register
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        
        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_disableTx(EF_UART_TYPE_PTR uart);


//! enables loopback (connecting TX to RX signal) by setting "lpen" bit in the control register to 1 
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        
        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_enableLoopBack(EF_UART_TYPE_PTR uart);


//! disables loopback (connecting TX to RX signal) by clearing "lpen" bit in the control register
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        
        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_disableLoopBack(EF_UART_TYPE_PTR uart);


//! enables glitch filter (filter out noise or glitches on the received signal) by setting "gfen" bit in the control register to 1 
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        
        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_enableGlitchFilter(EF_UART_TYPE_PTR uart);


//! disables glitch filter (filter out noise or glitches on the received signal) by clearing "gfen" bit in the control register
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_disableGlitchFilter(EF_UART_TYPE_PTR uart);


//! sets the control register to a certain value where
//! *  bit 0: UART enable
//! *  bit 1: UART Transmitter enable
//! *  bit 2: UART Receiver enable
//! *  bit 3: Loopback (connect RX and TX pins together) enable
//! *  bit 4: UART Glitch Filer on RX enable
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [in] value The value of the control register

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_setCTRL(EF_UART_TYPE_PTR uart, uint32_t value);


//! returns the value of the control register
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [out] CTRL_value The value of the control register

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_getCTRL(EF_UART_TYPE_PTR uart, uint32_t* CTRL_value);


//! sets the Data Size (Data word length: 5-9 bits ) by setting the "wlen" field in configuration register 
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [in] value The value of the required data word length  

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_setDataSize(EF_UART_TYPE_PTR uart, uint32_t value);


//! sets the "stp2" bit in configuration register (whether the stop boits are two or one)
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [in] is_two_bits bool value, if "true", the stop bits are two and if "false", the stop bit is one

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_setStopBits(EF_UART_TYPE_PTR uart, bool is_two_bits);


//! sets the "parity" field  in configuration register (could be none, odd, even, sticky 0 or sticky 1)
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [in] parity enum parity_type could be "NONE" , "ODD" , "EVEN" ,  "STICKY_0" , or  "STICKY_1"

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_setParityType(EF_UART_TYPE_PTR uart, enum parity_type parity);


//! sets the "timeout" field in configuration register which is receiver timeout measured in number of bits at which the timeout flag will be raised
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [in] value timeout bits value 
        
        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_setTimeoutBits(EF_UART_TYPE_PTR uart, uint32_t value);


//! sets the configuration register to a certain value where
//! *  bit 0-3: Data word length: 5-9 bits
//! *  bit 4: Two Stop Bits Select
//! *  bit 5-7: Parity Type: 000: None, 001: odd, 010: even, 100: Sticky 0, 101: Sticky 1
//! *  bit 8-13: Receiver Timeout measured in number of bits
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [in] config The value of the configuration register

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_setConfig(EF_UART_TYPE_PTR uart, uint32_t config);


//! returns the value of the configuration register
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [out] CFG_value The value of the configuration register

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_getConfig(EF_UART_TYPE_PTR uart, uint32_t* CFG_value);


//! sets the RX FIFO threshold to a certain value at which "RXA" interrupt will be raised 
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [in] threshold The value of the required threshold 

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_setRxFIFOThreshold(EF_UART_TYPE_PTR uart, uint32_t threshold);


//! returns the current value of the RX FIFO  threshold
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [out] RX_FIFO_THRESHOLD_value The value of the RX FIFO threshold register

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_getRxFIFOThreshold(EF_UART_TYPE_PTR uart, uint32_t* RX_FIFO_THRESHOLD_value);


//! sets the TX FIFO threshold to a certain value at which "TXB" interrupt will be raised 
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [in] threshold The value of the required threshold 

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_setTxFIFOThreshold(EF_UART_TYPE_PTR uart, uint32_t threshold);


//! returns the current value of the TX FIFO  threshold
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [out] TX_FIFO_THRESHOLD_value The value of the TX FIFO threshold register

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_getTxFIFOThreshold(EF_UART_TYPE_PTR uart, uint32_t* TX_FIFO_THRESHOLD_value);



//! sets the matchData to a certain value at which "MATCH" interrupt will be raised 
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [in] matchData The value of the required match data  

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_setMatchData(EF_UART_TYPE_PTR uart, uint32_t matchData);


//! returns the value of the match data register
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [out] MATCH_value The value of the match data register

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_getMatchData(EF_UART_TYPE_PTR uart, uint32_t* MATCH_value);


//! returns the current level of the TX FIFO (the number of bytes in the FIFO)
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [out] TX_FIFO_LEVEL_value The value of the TX FIFO level register

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_getTxCount(EF_UART_TYPE_PTR uart, uint32_t* TX_FIFO_LEVEL_value);


//! returns the current level of the RX FIFO (the number of bytes in the FIFO)
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [out] RX_FIFO_LEVEL_value The value of the RX FIFO level register

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_getRxCount(EF_UART_TYPE_PTR uart, uint32_t* RX_FIFO_LEVEL_value);


//! sets the prescaler to a certain value where Baud_rate = Bus_Clock_Freq/((Prescaler+1)*16)
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [in] prescaler The value of the required prescaler 

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_setPrescaler(EF_UART_TYPE_PTR uart, uint32_t prescaler);


//! returns the value of the prescaler
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [out] Prescaler_value The value of the prescaler register

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_getPrescaler(EF_UART_TYPE_PTR uart, uint32_t* Prescaler_value);


//! returns the value of the Raw Interrupt Status Register
//! *  bit 0 TXE : Transmit FIFO is Empty.
//! *  bit 1 RXF :  Receive FIFO is Full.
//! *  bit 2 TXB : Transmit FIFO level is Below Threshold.
//! *  bit 3 RXA : Receive FIFO level is Above Threshold.
//! *  bit 4 BRK : Line Break; 13 consecutive 0's have been detected on the line.
//! *  bit 5 MATCH : the receive data matches the MATCH register.
//! *  bit 6 FE : Framing Error, the receiver does not see a "stop" bit at the expected "stop" bit time.
//! *  bit 7 PRE : Parity Error; the receiver calculated parity does not match the received one.
//! *  bit 8 OR : Overrun; data has been received but the RX FIFO is full.
//! *  bit 9 RTO : Receiver Timeout; no data has been received for the time of a specified number of bits.
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [out] RIS_value The value of the Raw Interrupt Status Register

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_getRIS(EF_UART_TYPE_PTR uart, uint32_t* RIS_value);


//! returns the value of the Masked Interrupt Status Register
//! *  bit 0 TXE : Transmit FIFO is Empty.
//! *  bit 1 RXF :  Receive FIFO is Full.
//! *  bit 2 TXB : Transmit FIFO level is Below Threshold.
//! *  bit 3 RXA : Receive FIFO level is Above Threshold.
//! *  bit 4 BRK : Line Break; 13 consecutive 0's have been detected on the line.
//! *  bit 5 MATCH : the receive data matches the MATCH register.
//! *  bit 6 FE : Framing Error, the receiver does not see a "stop" bit at the expected "stop" bit time.
//! *  bit 7 PRE : Parity Error; the receiver calculated parity does not match the received one.
//! *  bit 8 OR : Overrun; data has been received but the RX FIFO is full.
//! *  bit 9 RTO : Receiver Timeout; no data has been received for the time of a specified number of bits.
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [out] MIS_value The value of the Masked Interrupt Status Register

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_getMIS(EF_UART_TYPE_PTR uart, uint32_t* MIS_value);


//! sets the value of the Interrupts Masking Register; which enable and disables interrupts
//! *  bit 0 TXE : Transmit FIFO is Empty.
//! *  bit 1 RXF :  Receive FIFO is Full.
//! *  bit 2 TXB : Transmit FIFO level is Below Threshold.
//! *  bit 3 RXA : Receive FIFO level is Above Threshold.
//! *  bit 4 BRK : Line Break; 13 consecutive 0's have been detected on the line.
//! *  bit 5 MATCH : the receive data matches the MATCH register.
//! *  bit 6 FE : Framing Error, the receiver does not see a "stop" bit at the expected "stop" bit time.
//! *  bit 7 PRE : Parity Error; the receiver calculated parity does not match the received one.
//! *  bit 8 OR : Overrun; data has been received but the RX FIFO is full.
//! *  bit 9 RTO : Receiver Timeout; no data has been received for the time of a specified number of bits.
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [in] mask The required mask value

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_setIM(EF_UART_TYPE_PTR uart, uint32_t mask);


//! returns the value of the Interrupts Masking Register; which enable and disables interrupts
//! *  bit 0 TXE : Transmit FIFO is Empty.
//! *  bit 1 RXF :  Receive FIFO is Full.
//! *  bit 2 TXB : Transmit FIFO level is Below Threshold.
//! *  bit 3 RXA : Receive FIFO level is Above Threshold.
//! *  bit 4 BRK : Line Break; 13 consecutive 0's have been detected on the line.
//! *  bit 5 MATCH : the receive data matches the MATCH register.
//! *  bit 6 FE : Framing Error, the receiver does not see a "stop" bit at the expected "stop" bit time.
//! *  bit 7 PRE : Parity Error; the receiver calculated parity does not match the received one.
//! *  bit 8 OR : Overrun; data has been received but the RX FIFO is full.
//! *  bit 9 RTO : Receiver Timeout; no data has been received for the time of a specified number of bits.
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [out] IM_value The value of the Interrupts Masking Register

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_getIM(EF_UART_TYPE_PTR uart, uint32_t* IM_value);


//! sets the value of the Interrupts Clear Register; write 1 to clear the flag
//! *  bit 0 TXE : Transmit FIFO is Empty.
//! *  bit 1 RXF :  Receive FIFO is Full.
//! *  bit 2 TXB : Transmit FIFO level is Below Threshold.
//! *  bit 3 RXA : Receive FIFO level is Above Threshold.
//! *  bit 4 BRK : Line Break; 13 consecutive 0's have been detected on the line.
//! *  bit 5 MATCH : the receive data matches the MATCH register.
//! *  bit 6 FE : Framing Error, the receiver does not see a "stop" bit at the expected "stop" bit time.
//! *  bit 7 PRE : Parity Error; the receiver calculated parity does not match the received one.
//! *  bit 8 OR : Overrun; data has been received but the RX FIFO is full.
//! *  bit 9 RTO : Receiver Timeout; no data has been received for the time of a specified number of bits.
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [in] mask The required mask value

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_setICR(EF_UART_TYPE_PTR uart, uint32_t mask);


//! transmit an array of characters through uart 
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [in] char_arr An array of characters to send 

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 

    */
EF_DRIVER_STATUS EF_UART_writeCharArr(EF_UART_TYPE_PTR uart, const char *char_arr);


//! transmit a single character through uart 
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [in] data The character or byte required to send 

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_writeChar(EF_UART_TYPE_PTR uart, char data);


//! recieve a single character through uart 
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [out] RXDATA_value The value of the received character

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_readChar(EF_UART_TYPE_PTR uar, char* RXDATA_value);



// The following functions are not verified yet
/******************************************************************************************************************************************/
/******************************************************************************************************************************************/


//! This is a non-blocking function that reads a character from the UART receive FIFO if data is available and returns a status code
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [out] RXDATA_value The value of the received character
        \param [out] data_available A flag indicating if data is available in the receive FIFO

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_readCharNonBlocking(EF_UART_TYPE_PTR uart, char* RXDATA_value, bool* data_available);

//! This is a non-blocking function that writes a character to the UART transmit FIFO if the FIFO is not full and returns a status code
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [in] data The character or byte required to send 
        \param [out] data_sent A flag indicating if the data was sent successfully

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_writeCharNonBlocking(EF_UART_TYPE_PTR uart, char data, bool* data_sent);

//! This function returns a flag indicating whether or not there is data available in the receive FIFO
    /*!
        \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
        \param [out] flag a flag indicating if there is data available in the receive FIFO

        \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_charsAvailable(EF_UART_TYPE_PTR uart, bool* flag);


//! This function returns a flag indicating whether or not the transmit is available, i.e. the transmit FIFO is not full
    /*!
      \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
      \param [out] flag a flag indicating if the transmit FIFO is not full

      \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_spaceAvailable(EF_UART_TYPE_PTR uart, bool* flag);

//! This function return the parity mode of the UART
    /*!
      \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
      \param [out] parity The parity mode of the UART

      \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_getParityMode(EF_UART_TYPE_PTR uart, uint32_t* parity_mode);

//! This function checks id the UART is busy
    /*!
      \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
      \param [out] flag a flag indicating if the UART is busy

      \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_busy(EF_UART_TYPE_PTR uart, bool* flag);


//! This function initializes the UART with the specified parameters
    /*!
      \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
      \param [in] baud_rate The baud rate of the UART
      \param [in] bus_clock The bus clock frequency
      \param [in] data_bits The number of data bits
      \param [in] two_stop_bits A flag indicating if two stop bits are used
      \param [in] parity The parity mode
      \param [in] timeout The receiver timeout
      \param [in] rx_threshold The receive FIFO threshold
      \param [in] tx_threshold The transmit FIFO threshold

      \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS UART_Init(EF_UART_TYPE_PTR uart, uint32_t baud_rate, uint32_t bus_clock, uint32_t data_bits, bool two_stop_bits, enum parity_type parity, uint32_t timeout, uint32_t rx_threshold, uint32_t tx_threshold);


//! This function receives a string message from the UART. The message is stored in a buffer with a specified size. 
/// \note This is a blocking function and can only terminate under the following conditions:
/// 1. The buffer is full
/// 2. A "\n" character is received
/// 3. An error is detected
    /*!
      \param [in] uart An \ref EF_UART_TYPE_PTR , which points to the base memory address of UART registers. \ref EF_UART_TYPE is a structure that contains the UART registers.
      \param [out] buffer The buffer to store the received message
      \param [in] buffer_size The size of the buffer

      \return status A value of type \ref EF_DRIVER_STATUS : returns a success or error code 
    */
EF_DRIVER_STATUS EF_UART_readCharArr(EF_UART_TYPE_PTR uart, char *buffer, uint32_t buffer_size);


/******************************************************************************
* External Variables
******************************************************************************/


#endif // EF_UART_H

/******************************************************************************
* End of File
******************************************************************************/

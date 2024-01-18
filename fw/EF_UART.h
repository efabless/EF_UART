/*! \file EF_UART.h
    \brief C header file for UART APIs which contains the function prototypes 
    
*/


#ifndef EF_UART_H
#define EF_UART_H

#include <EF_UART_regs.h>
#include <stdint.h>
#include <stdbool.h>

enum parity_type {NONE = 0, ODD = 1, EVEN = 2, STICKY_0 = 4, STICKY_1 = 5};


//! enables using uart by setting uart enable bit in the control register to 1 
    /*!
      \param uart_base The base memory address of UART registers.
    */

void EF_UART_enable(uint32_t uart_base);

//! disables using uart by clearing uart enable bit in the control register
    /*!
    \param uart_base The base memory address of UART registers.
    */
   
void EF_UART_disable(uint32_t uart_base);

//! enables using uart RX by setting uart RX enable bit in the control register to 1 
    /*!
    \param uart_base The base memory address of UART registers.
    */
void EF_UART_enableRx(uint32_t uart_base);

//! disables using uart RX by clearing uart RX enable bit in the control register
    /*!
    \param uart_base The base memory address of UART registers.
    */
void EF_UART_disableRx(uint32_t uart_base);

//! enables using uart TX by setting uart TX enable bit in the control register to 1 
    /*!
    \param uart_base The base memory address of UART registers.
    */
void EF_UART_enableTx(uint32_t uart_base);

//! disables using uart TX by clearing uart TX enable bit in the control register
    /*!
    \param uart_base The base memory address of UART registers.
*/
void EF_UART_disableTx(uint32_t uart_base);


void EF_UART_enableLoopBack(uint32_t uart_base);
void EF_UART_disableLoopBack(uint32_t uart_base);
void EF_UART_enableGlitchFilter(uint32_t uart_base);
void EF_UART_disableGlitchFilter(uint32_t uart_base);
void EF_UART_setControl(uint32_t uart_base, int value);
int EF_UART_getControl(uint32_t uart_base);
void EF_UART_setDataSize(uint32_t uart_base, int value);
void EF_UART_setTwoStopBitsSelect(uint32_t uart_base, bool is_two_bits);
void EF_UART_setParityType(uint32_t uart_base, enum parity_type parity);
void EF_UART_setTimeoutBits(uint32_t uart_base, int value);
void EF_UART_setConfig(uint32_t uart_base, int config);
int EF_UART_getConfig(uint32_t uart_base);
void EF_UART_setRxFifoThreshold(uint32_t uart_base, int threshold);
int EF_UART_getRxFifoThreshold(uint32_t uart_base);
void EF_UART_setTxFifoThreshold(uint32_t uart_base, int threshold);
int EF_UART_getTxFifoThreshold(uint32_t uart_base);
void EF_UART_setFifoControl (uint32_t uart_base, int value);
int EF_UART_getFifoControl (uint32_t uart_base);
int EF_UART_getFifoStatus(uint32_t uart_base);
void EF_UART_setMatchData(uint32_t uart_base, int matchData);
int EF_UART_getMatchData(uint32_t uart_base);




//! returns the current level of the TX FIFO (the number of bytes in the FIFO)
    /*!
      \param uart_base The base memory address of UART registers.
      \return TX FIFO level register
    */
int EF_UART_getTxFifoLevel(uint32_t uart_base);


//! returns the current level of the RX FIFO (the number of bytes in the FIFO)
    /*!
      \param uart_base The base memory address of UART registers.
      \return RX FIFO level register
    */
int EF_UART_getRxFifoLevel(uint32_t uart_base);



//! sets the prescaler to a certain value where Baud_rate = Bus_Clock_Freq/((Prescaler+1)*16)
    /*!
      \param uart_base The base memory address of UART registers.
      \param prescaler The value of the required prescaler 

    */
void EF_UART_setPrescaler(uint32_t uart_base, int prescaler);


//! returns the value of the prescaler
    /*!
      \param uart_base The base memory address of UART registers.
      \return prescaler register value 
    */
int EF_UART_getPrescaler(uint32_t uart_base);

//! returns the value of the Raw Interrupt Status Register
//! *  bit 0: TX FIFO is Empty
//! *  bit 1: TX FIFO level is below the value in the TX FIFO Level Threshold Register
//! *  bit 2: RX FIFO is Full
//! *  bit 3: RX FIFO level is above the value in the RX FIFO Level Threshold Register
    /*!
      \param uart_base The base memory address of UART registers.
      \return RIS register value 
    */
int EF_UART_getRIS(uint32_t uart_base);


//! returns the value of the Masked Interrupt Status Register
//! *  bit 0: TX FIFO is Empty
//! *  bit 1: TX FIFO level is below the value in the TX FIFO Level Threshold Register
//! *  bit 2: RX FIFO is Full
//! *  bit 3: RX FIFO level is above the value in the RX FIFO Level Threshold Register
    /*!
      \param uart_base The base memory address of UART registers.
      \return MIS register value 
    */
int EF_UART_getMIS(uint32_t uart_base);


//! sets the value of the Interrupts Masking Register; which enable and disables interrupts
//! *  bit 0: TX FIFO is Empty
//! *  bit 1: TX FIFO level is below the value in the TX FIFO Level Threshold Register
//! *  bit 2: RX FIFO is Full
//! *  bit 3: RX FIFO level is above the value in the RX FIFO Level Threshold Register
    /*!
      \param uart_base The base memory address of UART registers.
      \param mask The required mask value
    */
void EF_UART_setIM(uint32_t uart_base, int mask);


//! returns the value of the Interrupts Masking Register; which enable and disables interrupts
//! *  bit 0: TX FIFO is Empty
//! *  bit 1: TX FIFO level is below the value in the TX FIFO Level Threshold Register
//! *  bit 2: RX FIFO is Full
//! *  bit 3: RX FIFO level is above the value in the RX FIFO Level Threshold Register
    /*!
      \param uart_base The base memory address of UART registers.
      \return IM register value 
    */
int EF_UART_getIM(uint32_t uart_base);


//! sets the value of the Interrupts Clear Register; write 1 to clear the flag
//! *  bit 0: TX FIFO is Empty
//! *  bit 1: TX FIFO level is below the value in the TX FIFO Level Threshold Register
//! *  bit 2: RX FIFO is Full
//! *  bit 3: RX FIFO level is above the value in the RX FIFO Level Threshold Register
    /*!
      \param uart_base The base memory address of UART registers.
      \param mask The required mask value
    */
void EF_UART_setICR(uint32_t uart_base, int mask);


//! transmit an array of characters through uart 
    /*!
      \param uart_base The base memory address of UART registers.
      \param char_arr An array of characters to send 

    */
void EF_UART_writeCharArr(uint32_t uart_base, const char *char_arr);


//! transmit a single character through uart 
    /*!
      \param uart_base The base memory address of UART registers.
      \param data The character or byte required to send 

    */
void EF_UART_writeChar(uint32_t uart_base, char data);


//! recieve a single character through uart 
    /*!
      \param uart_base The base memory address of UART registers.
      \return the byte recieved 

    */
int EF_UART_readChar(uint32_t uart_base);

#endif
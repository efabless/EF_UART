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


/*! \file EF_UART.c
    \brief C file for UART APIs which contains the function implmentations 
    
*/

#ifndef EF_UART_C
#define EF_UART_C

/******************************************************************************
* Includes
******************************************************************************/
#include "EF_UART.h"

/******************************************************************************
* File-Specific Macros and Constants
******************************************************************************/



/******************************************************************************
* Static Variables
******************************************************************************/



/******************************************************************************
* Static Function Prototypes
******************************************************************************/



/******************************************************************************
* Function Definitions
******************************************************************************/

EF_DRIVER_STATUS EF_UART_setGclkEnable(EF_UART_TYPE_PTR uart, uint32_t value){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK;

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;    // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if ((value < (uint32_t)0x0) || (value > (uint32_t)0x1)) {  
        status = EF_DRIVER_ERROR_PARAMETER;    // Return EF_DRIVER_ERROR_PARAMETER if value is out of range
    }else {
        uart->GCLK = value;                     // Set the GCLK enable bit to the given value
    }

    return status;
}

EF_DRIVER_STATUS EF_UART_enable(EF_UART_TYPE_PTR uart){

    EF_DRIVER_STATUS status = EF_DRIVER_OK;

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else{
        uart->CTRL |= ((uint32_t)0x1 << EF_UART_CTRL_REG_EN_BIT);   // set the enable bit to 1 at the specified offset
        
    }   

    return status;
}

EF_DRIVER_STATUS EF_UART_disable(EF_UART_TYPE_PTR uart){

    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else{
        uart->CTRL &= ~EF_UART_CTRL_REG_EN_MASK;        // Clear the enable bit using the specified  mask
        
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_enableRx(EF_UART_TYPE_PTR uart){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else{
        uart->CTRL |= ((uint32_t)0x1 << EF_UART_CTRL_REG_RXEN_BIT); // set the enable bit to 1 at the specified offset
        
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_disableRx(EF_UART_TYPE_PTR uart){

    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else{
        uart->CTRL &= ~EF_UART_CTRL_REG_RXEN_MASK;      // Clear the enable bit using the specified  mask
        
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_enableTx(EF_UART_TYPE_PTR uart){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else{
        uart->CTRL |= ((uint32_t)0x1 << EF_UART_CTRL_REG_TXEN_BIT); // set the enable bit to 1 at the specified offset
        
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_disableTx(EF_UART_TYPE_PTR uart){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else{
        uart->CTRL &= ~EF_UART_CTRL_REG_TXEN_MASK;      // Clear the enable bit using the specified  mask
        
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_enableLoopBack(EF_UART_TYPE_PTR uart){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else{
        uart->CTRL |= ((uint32_t)0x1 << EF_UART_CTRL_REG_LPEN_BIT); // set the enable bit to 1 at the specified offset
        
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_disableLoopBack(EF_UART_TYPE_PTR uart){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else{
        uart->CTRL &= ~EF_UART_CTRL_REG_LPEN_MASK;      // Clear the enable bit using the specified  mask
        
    }
    return status;
}


EF_DRIVER_STATUS EF_UART_enableGlitchFilter(EF_UART_TYPE_PTR uart){

    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else{
        uart->CTRL &= ~EF_UART_CTRL_REG_GFEN_MASK;      // Clear the enable bit using the specified  mask
        uart->CTRL |= ((uint32_t)0x1 << EF_UART_CTRL_REG_GFEN_BIT); // set the enable bit to 1 at the specified offset
        
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_disableGlitchFilter(EF_UART_TYPE_PTR uart){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else{
        uart->CTRL &= ~EF_UART_CTRL_REG_GFEN_MASK;      // Clear the enable bit using the specified  mask
        
    }
    return status;
}


EF_DRIVER_STATUS EF_UART_setCTRL(EF_UART_TYPE_PTR uart, uint32_t value){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (value > EF_UART_CTRL_REG_MAX_VALUE) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if value is out of range
    } else {
        uart->CTRL = value;
        
    }
    return status;
}


EF_DRIVER_STATUS EF_UART_getCTRL(EF_UART_TYPE_PTR uart, uint32_t* CTRL_value){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (CTRL_value == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if CTRL_value is NULL, 
                                                        // i.e. there is no memory location to store the value
    } else {
        *CTRL_value = uart->CTRL;
        
    }
    return status;
}


EF_DRIVER_STATUS EF_UART_setPrescaler(EF_UART_TYPE_PTR uart, uint32_t prescaler){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (prescaler > EF_UART_PR_REG_MAX_VALUE) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if prescaler is out of range
    } else {
        uart->PR = prescaler;
        
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_getPrescaler(EF_UART_TYPE_PTR uart, uint32_t* Prescaler_value){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;             // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (Prescaler_value == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;             // Return EF_DRIVER_ERROR_PARAMETER if Prescaler_value is NULL, 
                                                        // i.e. there is no memory location to store the value
    } else {
        *Prescaler_value = uart->PR;
        
    }
    return status;
}


EF_DRIVER_STATUS EF_UART_setDataSize(EF_UART_TYPE_PTR uart, uint32_t value){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if ((value < EF_UART_DataLength_MIN_VALUE) || (value > EF_UART_DataLength_MAX_VALUE)) {
        status = EF_DRIVER_ERROR_UNSUPPORTED;              // Return EF_DRIVER_ERROR_UNSUPPORTED if data length is out of range
                                                        // This UART IP only supports data length from 5 to 9 bits
    } else {

        uart->CFG &= ~EF_UART_CFG_REG_WLEN_MASK;        // Clear the field bits in the register using the defined mask
        uart->CFG |= ((value << EF_UART_CFG_REG_WLEN_BIT) & EF_UART_CFG_REG_WLEN_MASK);     // Set the bits with the given value at the defined offset
        
    }
    return status;
}

// todo: make this generic between 1 and 2 bits 
EF_DRIVER_STATUS EF_UART_setTwoStopBitsSelect(EF_UART_TYPE_PTR uart, bool is_two_bits){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else {
        if (is_two_bits){
            uart->CFG |= ((uint32_t)0x1 << EF_UART_CFG_REG_STP2_BIT); // set the enable bit to 1 at the specified offset
        } else {
            uart->CFG &= ~EF_UART_CFG_REG_STP2_MASK;      // Clear the enable bit using the specified  mask
        }
        
    }
    return status;
}

// enum parity_type {NONE = 0, ODD = 1, EVEN = 2, STICKY_0 = 4, STICKY_1 = 5};
// This violates misrac 10.1 because the enum is not an essential type, and should not be used as an operand of a logical operator
EF_DRIVER_STATUS EF_UART_setParityType(EF_UART_TYPE_PTR uart, enum parity_type parity){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else {
        uart->CFG &= ~EF_UART_CFG_REG_PARITY_MASK;      // Clear the field bits in the register using the defined mask
        uart->CFG |= ((parity << EF_UART_CFG_REG_PARITY_BIT) & EF_UART_CFG_REG_PARITY_MASK); // Set the bits with the given value at the defined offset
        
    }
    return status;
}


EF_DRIVER_STATUS EF_UART_setTimeoutBits(EF_UART_TYPE_PTR uart, uint32_t value){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (value > EF_UART_CFG_REG_TIMEOUT_MAX_VALUE) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if value is out of range
    } else {
        uart->CFG &= ~EF_UART_CFG_REG_TIMEOUT_MASK;     // Clear the field bits in the register using the defined mask
        uart->CFG |= ((value << EF_UART_CFG_REG_TIMEOUT_BIT) & EF_UART_CFG_REG_TIMEOUT_MASK); // Set the bits with the given value at the defined offset
        
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_setConfig(EF_UART_TYPE_PTR uart, uint32_t value){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (value > EF_UART_CFG_REG_MAX_VALUE) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if value is out of range
    } else {
        uart->CFG = value;
        
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_getConfig(EF_UART_TYPE_PTR uart, uint32_t* CFG_value){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (CFG_value == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if CFG_value is NULL, 
                                                        // i.e. there is no memory location to store the value
    } else {
        *CFG_value = uart->CFG;
        
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_setRxFIFOThreshold(EF_UART_TYPE_PTR uart, uint32_t value){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (value > EF_UART_RX_FIFO_THRESHOLD_REG_MAX_VALUE) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if value is out of range
    } else {
        uart->RX_FIFO_THRESHOLD = value;
        
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_getRxFIFOThreshold(EF_UART_TYPE_PTR uart, uint32_t* RX_FIFO_THRESHOLD_value){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (RX_FIFO_THRESHOLD_value == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if RX_FIFO_THRESHOLD_value is NULL, 
                                                        // i.e. there is no memory location to store the value
    } else {
        *RX_FIFO_THRESHOLD_value = uart->RX_FIFO_THRESHOLD;
        
    }
    return status;
}


EF_DRIVER_STATUS EF_UART_setTxFIFOThreshold(EF_UART_TYPE_PTR uart, uint32_t value){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (value > EF_UART_TX_FIFO_THRESHOLD_REG_MAX_VALUE) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if value is out of range
    } else {
        uart->TX_FIFO_THRESHOLD = value;
        
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_getTxFIFOThreshold(EF_UART_TYPE_PTR uart, uint32_t* TX_FIFO_THRESHOLD_value){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (TX_FIFO_THRESHOLD_value == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if TX_FIFO_THRESHOLD_value is NULL, 
                                                        // i.e. there is no memory location to store the value
    } else {
        *TX_FIFO_THRESHOLD_value = uart->TX_FIFO_THRESHOLD;
        
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_getTxCount(EF_UART_TYPE_PTR uart, uint32_t* TX_FIFO_LEVEL_value){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (TX_FIFO_LEVEL_value == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if TX_FIFO_LEVEL_value is NULL, 
                                                        // i.e. there is no memory location to store the value
    } else {
        *TX_FIFO_LEVEL_value = uart->TX_FIFO_LEVEL;
        
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_getRxCount(EF_UART_TYPE_PTR uart, uint32_t* RX_FIFO_LEVEL_value){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (RX_FIFO_LEVEL_value == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if RX_FIFO_LEVEL_value is NULL, 
                                                        // i.e. there is no memory location to store the value
    } else {
        *RX_FIFO_LEVEL_value = uart->RX_FIFO_LEVEL;
        
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_setMatchData(EF_UART_TYPE_PTR uart, uint32_t matchData){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (matchData > EF_UART_MATCH_REG_MAX_VALUE) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if matchData is out of range
    } else {
        uart->MATCH = matchData;
        
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_getMatchData(EF_UART_TYPE_PTR uart, uint32_t* MATCH_value){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (MATCH_value == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if MATCH_value is NULL, 
                                                        // i.e. there is no memory location to store the value
    } else {
        *MATCH_value = uart->MATCH;
        
    }
    return status;
}

 // Interrupts bits in RIS, MIS, IM, and ICR
 // bit 0: TX FIFO is Empty
 // bit 1: RX FIFO is Full
 // bit 2: TX FIFO level is below the value in the TX FIFO Level Threshold Register
 // bit 3: RX FIFO level is above the value in the RX FIFO Level Threshold Register
 // bit 4: line break
 // bit 5: match
 // bit 6: frame error
 // bit 7: parity error
 // bit 8: overrun 
 // bit 9: timeout 

EF_DRIVER_STATUS EF_UART_getRIS(EF_UART_TYPE_PTR uart, uint32_t* RIS_value){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (RIS_value == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if RIS_value is NULL, 
                                                        // i.e. there is no memory location to store the value
    } else {
        *RIS_value = uart->RIS;
        
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_getMIS(EF_UART_TYPE_PTR uart, uint32_t* MIS_value){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (MIS_value == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if MIS_value is NULL, 
                                                        // i.e. there is no memory location to store the value
    } else {
        *MIS_value = uart->MIS;
        
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_setIM(EF_UART_TYPE_PTR uart, uint32_t mask){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (mask > EF_UART_IM_REG_MAX_VALUE) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if mask is out of range

    } else {
        uart->IM = mask;
        
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_getIM(EF_UART_TYPE_PTR uart, uint32_t* IM_value){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (IM_value == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if IM_value is NULL, 
                                                        // i.e. there is no memory location to store the value
    } else {
        *IM_value = uart->IM;
        
    }
    return status;
}


EF_DRIVER_STATUS EF_UART_setICR(EF_UART_TYPE_PTR uart, uint32_t mask){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK; 

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (mask > EF_UART_IC_REG_MAX_VALUE) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if mask is out of range
    } else {
        uart->IC = mask;
        
    }
    return status;
}


EF_DRIVER_STATUS EF_UART_writeChar(EF_UART_TYPE_PTR uart, char data){

    EF_DRIVER_STATUS status = EF_DRIVER_OK;   

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else {

        uint32_t RIS_value;
        do {
            status = EF_UART_getRIS(uart, &RIS_value);
        } while ((status == EF_DRIVER_OK) && (RIS_value & EF_UART_TXB_FLAG) == (uint32_t)0x0); // wait until tx level below flag is 1

        if (status == EF_DRIVER_OK) {
            uart->TXDATA = data;
            status = EF_UART_setICR(uart, EF_UART_TXB_FLAG);
        } else {}
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_writeCharArr(EF_UART_TYPE_PTR uart, const char *char_arr){

    EF_DRIVER_STATUS status = EF_DRIVER_OK;
    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else {
        uint32_t RIS_value;
        char *char_arr_iterator = char_arr;
        while ((status == EF_DRIVER_OK) && (*char_arr_iterator)){
            do {
                status = EF_UART_getRIS(uart, &RIS_value);
            } while ((status == EF_DRIVER_OK) && (RIS_value & EF_UART_TXB_FLAG) == (uint32_t)0x0); // wait until tx level below flag is 1

            if (status == EF_DRIVER_OK) {
                uart->TXDATA = (*(char_arr_iterator));
                char_arr_iterator++;
                status = EF_UART_setICR(uart, EF_UART_TXB_FLAG);
            }else{}
        }
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_readChar(EF_UART_TYPE_PTR uart, char* RXDATA_value){

    EF_DRIVER_STATUS status = EF_DRIVER_OK;

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else {
        uint32_t RIS_value;
        do {
            status = EF_UART_getRIS(uart, &RIS_value);
        } while((status == EF_DRIVER_OK) && (RIS_value & EF_UART_RXA_FLAG) == (uint32_t)0x0); // wait over RX fifo level above flag to be 1

        if (status == EF_DRIVER_OK) {
            *RXDATA_value = uart->RXDATA;
            status = EF_UART_setICR(uart, EF_UART_RXA_FLAG);
        } else {}
    }
    return status;
}


// The following functions are not verified yet
/******************************************************************************************************************************************/
/*******************************************************************************xs***********************************************************/

EF_DRIVER_STATUS EF_UART_readCharNonBlocking(EF_UART_TYPE_PTR uart, char* RXDATA_value, bool* data_available){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK;

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else  if (RXDATA_value == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if RXDATA_value is NULL, 
                                                        // i.e. there is no memory location to store the value
    } else if (data_available == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if data_available is NULL, 
                                                        // i.e. there is no memory location to store the value
    } else {
        
        uint32_t RIS_value;
        status = EF_UART_getRIS(uart, &RIS_value);

        // Check if data is available
        if ((status == EF_DRIVER_OK) && (RIS_value & EF_UART_RXA_FLAG) == (uint32_t)0x0) {
            *data_available = false;
        } else {
            *data_available = true;
            *RXDATA_value = uart->RXDATA;
            status = EF_UART_setICR(uart, EF_UART_RXA_FLAG);
        }
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_writeCharNonBlocking(EF_UART_TYPE_PTR uart, char data, bool* data_sent){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK;

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else  if (data_sent == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if data_sent is NULL, 
                                                        // i.e. there is no memory location to store the value
    } else {
        
        uint32_t RIS_value;
        status = EF_UART_getRIS(uart, &RIS_value);

        // Check if data is available
        if ((status == EF_DRIVER_OK) && (RIS_value & EF_UART_TXB_FLAG) == (uint32_t)0x0) {
            *data_sent = false;
        } else {
            *data_sent = true;
            uart->TXDATA = data;
            status = EF_UART_setICR(uart, EF_UART_TXB_FLAG);
        }
    }
    return status;
}


EF_DRIVER_STATUS EF_UART_charsAvailable(EF_UART_TYPE_PTR uart, bool* RXA_flag) {

    EF_DRIVER_STATUS status = EF_DRIVER_OK;
    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (RXA_flag == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if RXA_flag is NULL, 
                                                        // i.e. there is no memory location to store the value
    } else {
        uint32_t RIS_value;
        status = EF_UART_getRIS(uart, &RIS_value);
        if (status == EF_DRIVER_OK) {
            *RXA_flag = (RIS_value & EF_UART_RXA_FLAG) != (uint32_t)0x0;
        }else {}
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_spaceAvailable(EF_UART_TYPE_PTR uart, bool* TXB_flag) {

    EF_DRIVER_STATUS status = EF_DRIVER_OK;
    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                 // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (TXB_flag == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                 // Return EF_DRIVER_ERROR_PARAMETER if TXB_flag is NULL, 
                                                            // i.e. there is no memory location to store the value
    } else {
        uint32_t RIS_value;
        status = EF_UART_getRIS(uart, &RIS_value);
        if (status == EF_DRIVER_OK) {
            *TXB_flag = (RIS_value & EF_UART_TXB_FLAG);     // check if TX FIFO level is below the value in the TX FIFO Level Threshold Register
        }else {}
    }
    return status;
}


EF_DRIVER_STATUS EF_UART_getParityMode(EF_UART_TYPE_PTR uart, uint32_t* parity_mode){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK;
    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (parity_mode == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if parity_mode is NULL, 
                                                        // i.e. there is no memory location to store the value
    } else {
        *parity_mode = (uart->CFG & EF_UART_CFG_REG_PARITY_MASK) >> EF_UART_CFG_REG_PARITY_BIT;
    }
    return status;
}

EF_DRIVER_STATUS EF_UART_busy(EF_UART_TYPE_PTR uart, bool* busy_flag){
    
    EF_DRIVER_STATUS status = EF_DRIVER_OK;
    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (busy_flag == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;                // Return EF_DRIVER_ERROR_PARAMETER if busy_flag is NULL, 
                                                        // i.e. there is no memory location to store the value
    } else {
        uint32_t RIS_value;
        status = EF_UART_getRIS(uart, &RIS_value);
        if (status == EF_DRIVER_OK) {
            *busy_flag = (RIS_value & EF_UART_TXE_FLAG) == (uint32_t)0x0;
        }else {}
    }
    return status;
}

// todo: document the threshold is the fifo max


// Function to initialize and configure the UART
EF_DRIVER_STATUS UART_Init(EF_UART_TYPE_PTR uart, uint32_t baud_rate, uint32_t bus_clock, uint32_t data_bits, bool two_stop_bits, enum parity_type parity, uint32_t timeout, uint32_t rx_threshold, uint32_t tx_threshold) {
    EF_DRIVER_STATUS status = EF_DRIVER_OK;

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;    // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    }

    // Calculate and set the prescaler
    uint32_t prescaler = (bus_clock / (baud_rate * (uint32_t)8)) - (uint32_t)1;
    if (status == EF_DRIVER_OK) {status = EF_UART_setPrescaler(uart, prescaler);} else {}

    // Configure data bits, stop bits, and parity

    // Set data bits (5-9 bits)
    if (status == EF_DRIVER_OK) {status = EF_UART_setDataSize(uart, data_bits);} else {}

    // Set stop bits (1 or 2)
    if (status == EF_DRIVER_OK) {status = EF_UART_setTwoStopBitsSelect(uart, two_stop_bits);} else {}

    // Set parity type
    if (status == EF_DRIVER_OK) {status = EF_UART_setParityType(uart, parity);} else {}

    // Set the receiver timeout value
    if (status == EF_DRIVER_OK) {status = EF_UART_setTimeoutBits(uart, timeout);} else {}

    // Set RX and TX FIFO thresholds
    if (status == EF_DRIVER_OK) {status = EF_UART_setRxFIFOThreshold(uart, rx_threshold);} else {}
    if (status == EF_DRIVER_OK) {status = EF_UART_setTxFIFOThreshold(uart, tx_threshold);} else {}

    // Enable the UART and both RX and TX
    if (status == EF_DRIVER_OK) {status = EF_UART_enable(uart);} else {}
    if (status == EF_DRIVER_OK) {status = EF_UART_setGclkEnable(uart, (uint32_t)1);} else {}
    if (status == EF_DRIVER_OK) {status = EF_UART_enableRx(uart);} else {}
    if (status == EF_DRIVER_OK) {status = EF_UART_enableTx(uart);} else {}

    // Optionally enable glitch filter and loopback for testing
    if (status == EF_DRIVER_OK) {status = EF_UART_enableGlitchFilter(uart);} else {}
    if (status == EF_DRIVER_OK) {status = EF_UART_enableLoopBack(uart);} else {}

    return EF_DRIVER_OK;
}


// Function to receive a string using UART
EF_DRIVER_STATUS EF_UART_readCharArr(EF_UART_TYPE_PTR uart, char *buffer, uint32_t buffer_size) {

    EF_DRIVER_STATUS status = EF_DRIVER_OK;

    if (uart == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;    // Return EF_DRIVER_ERROR_PARAMETER if uart is NULL
    } else if (buffer == NULL) {
        status = EF_DRIVER_ERROR_PARAMETER;    // Return EF_DRIVER_ERROR_PARAMETER if buffer is NULL
    } else if (buffer_size == (uint32_t)0) {
        status = EF_DRIVER_ERROR_PARAMETER;    // Return EF_DRIVER_ERROR_PARAMETER if buffer_size is 0
    }else{
        uint32_t index = 0;
        while (index < (buffer_size - (uint32_t)1)) {
            bool data_available = false;
            status = EF_UART_charsAvailable(uart, &data_available);
            if (status != EF_DRIVER_OK){break;}     // return on error
            if (!data_available) {continue;}        // skip this iteration and wait for data

            char received_char;
            status = EF_UART_readChar(uart, &received_char);
            if (status != EF_DRIVER_OK){break;}     // return on error

            buffer[index] = received_char;
            index++;
            if (received_char == '\n') break;       // Stop reading at newline
        }
        buffer[index] = '\0';                       // Null-terminate the string
    }

    return EF_DRIVER_OK;
}



/******************************************************************************
* Static Function Definitions
******************************************************************************/





#endif // EF_UART_C

/******************************************************************************
* End of File
******************************************************************************/

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


/*! \file EF_UART_example.c
    \brief C header file containing an example of how to use the UART APIs
    
*/


#ifndef EF_UART_EXAMPLE_H
#define EF_UART_EXAMPLE_H

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



/******************************************************************************
* Example Usage
******************************************************************************/

/** @brief Example Usage
 Example usage:
 @code
 #include "EF_UART.h"

 #define Example_UART_BASE_ADDRESS 0x40000000
 #define UART0 ((EF_UART_TYPE_PTR)Example_UART_BASE_ADDRESS)

 EF_DRIVER_STATUS EF_UART_example(void){
    EF_DRIVER_STATUS status;

    // Initialize UART with required configurations
    status = UART_Init(UART0, 9600, 16000000, 8, false, EVEN, 10, 4, 4);
    if (status != EF_DRIVER_OK) {
        return status;
    }

    // Transmit a message
    const char *message = "Hello, UART!\n";
    status = EF_UART_writeCharArr(UART0, message);
    if (status != EF_DRIVER_OK) {
        // Handle transmission error
        return status;
    }

    // Receive a message
    char buffer[100];
    status = EF_UART_readCharArr(UART0, buffer, sizeof(buffer));
    if (status != EF_DRIVER_OK) {
        // Handle reception error
        return status;
    }
     return EF_DRIVER_OK;
 }
 @endcode
 */
EF_DRIVER_STATUS EF_UART_example(void);

/******************************************************************************
* Static Function Definitions
******************************************************************************/



#endif // EF_UART_EXAMPLE_H

/******************************************************************************
* End of File
******************************************************************************/

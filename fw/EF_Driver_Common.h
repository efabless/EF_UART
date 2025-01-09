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

/*! \file EF_Driver_Common.h
    \brief C header file for common driver definitions and types
    
*/


#ifndef EF_DRIVER_COMMON_H
#define EF_DRIVER_COMMON_H

/******************************************************************************
* Includes
******************************************************************************/
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>


/******************************************************************************
* Macros and Constants
******************************************************************************/
/* General return codes */
#define EF_DRIVER_OK                    ((uint32_t)0)   ///< Operation succeeded 
#define EF_DRIVER_ERROR                 ((uint32_t)1)   ///< Unspecified error
#define EF_DRIVER_ERROR_BUSY            ((uint32_t)2)   ///< Driver is busy
#define EF_DRIVER_ERROR_TIMEOUT         ((uint32_t)3)   ///< Timeout occurred
#define EF_DRIVER_ERROR_UNSUPPORTED     ((uint32_t)4)   ///< Operation not supported
#define EF_DRIVER_ERROR_PARAMETER       ((uint32_t)5)   ///< Parameter error
#define EF_DRIVER_ERROR_SPECIFIC        ((uint32_t)6)   ///< Start of driver specific errors 


/******************************************************************************
* Typedefs and Enums
******************************************************************************/

typedef uint32_t EF_DRIVER_STATUS;      ///<  A type that is used to return the status of the driver functions


/******************************************************************************
* External Variables
******************************************************************************/


/******************************************************************************
* Function Prototypes
******************************************************************************/


#endif // EF_DRIVER_COMMON_H 

/******************************************************************************
* End of File
******************************************************************************/

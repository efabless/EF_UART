# API Reference

## Header files

- [EF_Driver_Common.h](#file-ef_driver_commonh)
- [EF_UART.h](#file-ef_uarth)
- [EF_UART_regs.h](#file-ef_uart_regsh)

## File EF_Driver_Common.h

_C header file for common driver definitions and types._



## Structures and Types

| Type | Name |
| ---: | :--- |
| typedef uint32\_t | [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status)  <br>_A type that is used to return the status of the driver functions._ |


## Macros

| Type | Name |
| ---: | :--- |
| define  | [**EF\_DRIVER\_ERROR**](#define-ef_driver_error)  1<br>_Unspecified error._ |
| define  | [**EF\_DRIVER\_ERROR\_BUSY**](#define-ef_driver_error_busy)  2<br>_Driver is busy._ |
| define  | [**EF\_DRIVER\_ERROR\_NO\_DATA**](#define-ef_driver_error_no_data)  7<br>_No data available._ |
| define  | [**EF\_DRIVER\_ERROR\_PARAMETER**](#define-ef_driver_error_parameter)  5<br>_Parameter error._ |
| define  | [**EF\_DRIVER\_ERROR\_SPECIFIC**](#define-ef_driver_error_specific)  6<br>_Start of driver specific errors._ |
| define  | [**EF\_DRIVER\_ERROR\_TIMEOUT**](#define-ef_driver_error_timeout)  3<br>_Timeout occurred._ |
| define  | [**EF\_DRIVER\_ERROR\_UNSUPPORTED**](#define-ef_driver_error_unsupported)  4<br>_Operation not supported._ |
| define  | [**EF\_DRIVER\_OK**](#define-ef_driver_ok)  0<br>_Operation succeeded._ |

## Structures and Types Documentation

### typedef `EF_DRIVER_STATUS`

_A type that is used to return the status of the driver functions._
```c
typedef uint32_t EF_DRIVER_STATUS;
```



## Macros Documentation

### define `EF_DRIVER_ERROR`

_Unspecified error._
```c
#define EF_DRIVER_ERROR 1
```

### define `EF_DRIVER_ERROR_BUSY`

_Driver is busy._
```c
#define EF_DRIVER_ERROR_BUSY 2
```

### define `EF_DRIVER_ERROR_NO_DATA`

_No data available._
```c
#define EF_DRIVER_ERROR_NO_DATA 7
```

### define `EF_DRIVER_ERROR_PARAMETER`

_Parameter error._
```c
#define EF_DRIVER_ERROR_PARAMETER 5
```

### define `EF_DRIVER_ERROR_SPECIFIC`

_Start of driver specific errors._
```c
#define EF_DRIVER_ERROR_SPECIFIC 6
```

### define `EF_DRIVER_ERROR_TIMEOUT`

_Timeout occurred._
```c
#define EF_DRIVER_ERROR_TIMEOUT 3
```

### define `EF_DRIVER_ERROR_UNSUPPORTED`

_Operation not supported._
```c
#define EF_DRIVER_ERROR_UNSUPPORTED 4
```

### define `EF_DRIVER_OK`

_Operation succeeded._
```c
#define EF_DRIVER_OK 0
```


## File EF_UART.h

_C header file for UART APIs which contains the function prototypes._



## Structures and Types

| Type | Name |
| ---: | :--- |
| enum  | [**parity\_type**](#enum-parity_type)  <br> |

## Functions

| Type | Name |
| ---: | :--- |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_busy**](#function-ef_uart_busy) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, bool \*flag) <br>_This function checks id the UART is busy._ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_charsAvailable**](#function-ef_uart_charsavailable) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, bool \*flag) <br>_This function returns a flag indicating whether or not there is data available in the receive FIFO._ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_disable**](#function-ef_uart_disable) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart) <br>_disables using uart by clearing "en" bit in the control register_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_disableGlitchFilter**](#function-ef_uart_disableglitchfilter) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart) <br>_disables glitch filter (filter out noise or glitches on the received signal) by clearing "gfen" bit in the control register_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_disableLoopBack**](#function-ef_uart_disableloopback) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart) <br>_disables loopback (connecting TX to RX signal) by clearing "lpen" bit in the control register_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_disableRx**](#function-ef_uart_disablerx) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart) <br>_disables using uart RX by clearing uart "rxen" bit in the control register_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_disableTx**](#function-ef_uart_disabletx) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart) <br>_disables using uart TX by clearing uart "txen" bit in the control register_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_enable**](#function-ef_uart_enable) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart) <br>_enables using uart by setting "en" bit in the control register to 1_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_enableGlitchFilter**](#function-ef_uart_enableglitchfilter) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart) <br>_enables glitch filter (filter out noise or glitches on the received signal) by setting "gfen" bit in the control register to 1_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_enableLoopBack**](#function-ef_uart_enableloopback) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart) <br>_enables loopback (connecting TX to RX signal) by setting "lpen" bit in the control register to 1_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_enableRx**](#function-ef_uart_enablerx) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart) <br>_enables using uart RX by setting uart "rxen" bit in the control register to 1_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_enableTx**](#function-ef_uart_enabletx) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart) <br>_enables using uart TX by setting uart "txen" bit in the control register to 1_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_getCTRL**](#function-ef_uart_getctrl) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t \*CTRL\_value) <br>_returns the value of the control register_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_getConfig**](#function-ef_uart_getconfig) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t \*CFG\_value) <br>_returns the value of the configuration register_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_getIM**](#function-ef_uart_getim) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t \*IM\_value) <br> |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_getMIS**](#function-ef_uart_getmis) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t \*MIS\_value) <br> |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_getMatchData**](#function-ef_uart_getmatchdata) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t \*MATCH\_value) <br>_returns the value of the match data register_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_getParityMode**](#function-ef_uart_getparitymode) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t \*parity\_mode) <br>_This function return the parity mode of the UART._ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_getPrescaler**](#function-ef_uart_getprescaler) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t \*Prescaler\_value) <br>_returns the value of the prescaler_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_getRIS**](#function-ef_uart_getris) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t \*RIS\_value) <br> |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_getRxCount**](#function-ef_uart_getrxcount) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t \*RX\_FIFO\_LEVEL\_value) <br>_returns the current level of the RX FIFO (the number of bytes in the FIFO)_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_getRxFIFOThreshold**](#function-ef_uart_getrxfifothreshold) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t \*RX\_FIFO\_THRESHOLD\_value) <br>_returns the current value of the RX FIFO threshold_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_getTxCount**](#function-ef_uart_gettxcount) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t \*TX\_FIFO\_LEVEL\_value) <br>_returns the current level of the TX FIFO (the number of bytes in the FIFO)_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_getTxFIFOThreshold**](#function-ef_uart_gettxfifothreshold) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t \*TX\_FIFO\_THRESHOLD\_value) <br>_returns the current value of the TX FIFO threshold_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_readChar**](#function-ef_uart_readchar) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uar, char \*RXDATA\_value) <br>_recieve a single character through uart_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_readCharNonBlocking**](#function-ef_uart_readcharnonblocking) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, char \*RXDATA\_value, bool \*data\_available) <br>_This is a non-blocking function that reads a character from the UART receive FIFO if data is available and returns a status code._ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_setCTRL**](#function-ef_uart_setctrl) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t value) <br> |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_setConfig**](#function-ef_uart_setconfig) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t config) <br> |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_setDataSize**](#function-ef_uart_setdatasize) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t value) <br>_sets the Data Size (Data word length: 5-9 bits ) by setting the "wlen" field in configuration register_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_setGclkEnable**](#function-ef_uart_setgclkenable) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t value) <br>_sets the GCLK enable bit in the UART register to a certain value_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_setICR**](#function-ef_uart_seticr) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t mask) <br> |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_setIM**](#function-ef_uart_setim) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t mask) <br> |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_setMatchData**](#function-ef_uart_setmatchdata) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t matchData) <br>_sets the matchData to a certain value at which "MATCH" interrupt will be raised_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_setParityType**](#function-ef_uart_setparitytype) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, enum [**parity\_type**](#enum-parity_type) parity) <br>_sets the "parity" field in configuration register (could be none, odd, even, sticky 0 or sticky 1)_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_setPrescaler**](#function-ef_uart_setprescaler) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t prescaler) <br>_sets the prescaler to a certain value where Baud\_rate = Bus\_Clock\_Freq/((Prescaler+1)\*16)_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_setRxFIFOThreshold**](#function-ef_uart_setrxfifothreshold) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t threshold) <br>_sets the RX FIFO threshold to a certain value at which "RXA" interrupt will be raised_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_setTimeoutBits**](#function-ef_uart_settimeoutbits) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t value) <br>_sets the "timeout" field in configuration register which is receiver timeout measured in number of bits at which the timeout flag will be raised_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_setTwoStopBitsSelect**](#function-ef_uart_settwostopbitsselect) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, bool is\_two\_bits) <br>_sets the "stp2" bit in configuration register (whether the stop boits are two or one)_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_setTxFIFOThreshold**](#function-ef_uart_settxfifothreshold) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, uint32\_t threshold) <br>_sets the TX FIFO threshold to a certain value at which "TXB" interrupt will be raised_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_spaceAvailable**](#function-ef_uart_spaceavailable) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, bool \*flag) <br>_This function returns a flag indicating whether or not the transmit is available, i.e. the transmit FIFO is not full._ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_writeChar**](#function-ef_uart_writechar) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, char data) <br>_transmit a single character through uart_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_writeCharArr**](#function-ef_uart_writechararr) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, const char \*char\_arr) <br>_transmit an array of characters through uart_ |
|  [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) | [**EF\_UART\_writeCharNonBlocking**](#function-ef_uart_writecharnonblocking) ([**EF\_UART\_TYPE**](#typedef-ef_uart_type) \*uart, char data, bool \*data\_sent) <br>_This is a non-blocking function that writes a character to the UART transmit FIFO if the FIFO is not full and returns a status code._ |

## Macros

| Type | Name |
| ---: | :--- |
| define  | [**EF\_UART\_CFG\_REG\_MAX\_VALUE**](#define-ef_uart_cfg_reg_max_value)  ((uint32\_t)0x00001FFF)<br> |
| define  | [**EF\_UART\_CFG\_REG\_TIMEOUT\_MAX\_VALUE**](#define-ef_uart_cfg_reg_timeout_max_value)  ((uint32\_t)0x0000003F)<br> |
| define  | [**EF\_UART\_CTRL\_REG\_MAX\_VALUE**](#define-ef_uart_ctrl_reg_max_value)  ((uint32\_t)0x0000001F)<br> |
| define  | [**EF\_UART\_DataLength\_MAX\_VALUE**](#define-ef_uart_datalength_max_value)  ((uint32\_t)0x00000009)<br> |
| define  | [**EF\_UART\_DataLength\_MIN\_VALUE**](#define-ef_uart_datalength_min_value)  ((uint32\_t)0x00000005)<br> |
| define  | [**EF\_UART\_ERROR\_RX\_UNAVAILABLE**](#define-ef_uart_error_rx_unavailable)  -1<br> |
| define  | [**EF\_UART\_ERROR\_TX\_UNAVAILABLE**](#define-ef_uart_error_tx_unavailable)  1<br> |
| define  | [**EF\_UART\_IC\_REG\_MAX\_VALUE**](#define-ef_uart_ic_reg_max_value)  ((uint32\_t)0x000003FF)<br> |
| define  | [**EF\_UART\_IM\_REG\_MAX\_VALUE**](#define-ef_uart_im_reg_max_value)  ((uint32\_t)0x000003FF)<br> |
| define  | [**EF\_UART\_MATCH\_REG\_MAX\_VALUE**](#define-ef_uart_match_reg_max_value)  ((uint32\_t)0x00001FFF)<br> |
| define  | [**EF\_UART\_PR\_REG\_MAX\_VALUE**](#define-ef_uart_pr_reg_max_value)  ((uint32\_t)0x0000FFFF)<br> |
| define  | [**EF\_UART\_RX\_FIFO\_THRESHOLD\_REG\_MAX\_VALUE**](#define-ef_uart_rx_fifo_threshold_reg_max_value)  ((uint32\_t)0x0000000F)<br> |
| define  | [**EF\_UART\_SUCCESS**](#define-ef_uart_success)  0<br> |
| define  | [**EF\_UART\_TX\_FIFO\_THRESHOLD\_REG\_MAX\_VALUE**](#define-ef_uart_tx_fifo_threshold_reg_max_value)  ((uint32\_t)0x0000000F)<br> |

## Structures and Types Documentation

### enum `parity_type`

```c
enum parity_type {
    NONE = 0,
    ODD = 1,
    EVEN = 2,
    STICKY_0 = 4,
    STICKY_1 = 5
};
```


## Functions Documentation

### function `EF_UART_busy`

_This function checks id the UART is busy._
```c
EF_DRIVER_STATUS EF_UART_busy (
    EF_UART_TYPE *uart,
    bool *flag
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `flag` a flag indicating if the UART is busy


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_charsAvailable`

_This function returns a flag indicating whether or not there is data available in the receive FIFO._
```c
EF_DRIVER_STATUS EF_UART_charsAvailable (
    EF_UART_TYPE *uart,
    bool *flag
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `flag` a flag indicating if there is data available in the receive FIFO


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_disable`

_disables using uart by clearing "en" bit in the control register_
```c
EF_DRIVER_STATUS EF_UART_disable (
    EF_UART_TYPE *uart
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_disableGlitchFilter`

_disables glitch filter (filter out noise or glitches on the received signal) by clearing "gfen" bit in the control register_
```c
EF_DRIVER_STATUS EF_UART_disableGlitchFilter (
    EF_UART_TYPE *uart
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_disableLoopBack`

_disables loopback (connecting TX to RX signal) by clearing "lpen" bit in the control register_
```c
EF_DRIVER_STATUS EF_UART_disableLoopBack (
    EF_UART_TYPE *uart
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_disableRx`

_disables using uart RX by clearing uart "rxen" bit in the control register_
```c
EF_DRIVER_STATUS EF_UART_disableRx (
    EF_UART_TYPE *uart
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_disableTx`

_disables using uart TX by clearing uart "txen" bit in the control register_
```c
EF_DRIVER_STATUS EF_UART_disableTx (
    EF_UART_TYPE *uart
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_enable`

_enables using uart by setting "en" bit in the control register to 1_
```c
EF_DRIVER_STATUS EF_UART_enable (
    EF_UART_TYPE *uart
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_enableGlitchFilter`

_enables glitch filter (filter out noise or glitches on the received signal) by setting "gfen" bit in the control register to 1_
```c
EF_DRIVER_STATUS EF_UART_enableGlitchFilter (
    EF_UART_TYPE *uart
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_enableLoopBack`

_enables loopback (connecting TX to RX signal) by setting "lpen" bit in the control register to 1_
```c
EF_DRIVER_STATUS EF_UART_enableLoopBack (
    EF_UART_TYPE *uart
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_enableRx`

_enables using uart RX by setting uart "rxen" bit in the control register to 1_
```c
EF_DRIVER_STATUS EF_UART_enableRx (
    EF_UART_TYPE *uart
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_enableTx`

_enables using uart TX by setting uart "txen" bit in the control register to 1_
```c
EF_DRIVER_STATUS EF_UART_enableTx (
    EF_UART_TYPE *uart
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_getCTRL`

_returns the value of the control register_
```c
EF_DRIVER_STATUS EF_UART_getCTRL (
    EF_UART_TYPE *uart,
    uint32_t *CTRL_value
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `CTRL_value` The value of the control register


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_getConfig`

_returns the value of the configuration register_
```c
EF_DRIVER_STATUS EF_UART_getConfig (
    EF_UART_TYPE *uart,
    uint32_t *CFG_value
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `CFG_value` The value of the configuration register


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_getIM`

```c
EF_DRIVER_STATUS EF_UART_getIM (
    EF_UART_TYPE *uart,
    uint32_t *IM_value
) 
```


returns the value of the Interrupts Masking Register; which enable and disables interrupts

* bit 0 TXE : Transmit FIFO is Empty.
* bit 1 RXF : Receive FIFO is Full.
* bit 2 TXB : Transmit FIFO level is Below Threshold.
* bit 3 RXA : Receive FIFO level is Above Threshold.
* bit 4 BRK : Line Break; 13 consecutive 0's have been detected on the line.
* bit 5 MATCH : the receive data matches the MATCH register.
* bit 6 FE : Framing Error, the receiver does not see a "stop" bit at the expected "stop" bit time.
* bit 7 PRE : Parity Error; the receiver calculated parity does not match the received one.
* bit 8 OR : Overrun; data has been received but the RX FIFO is full.
* bit 9 RTO : Receiver Timeout; no data has been received for the time of a specified number of bits.



**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `IM_value` The value of the Interrupts Masking Register


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_getMIS`

```c
EF_DRIVER_STATUS EF_UART_getMIS (
    EF_UART_TYPE *uart,
    uint32_t *MIS_value
) 
```


returns the value of the Masked Interrupt Status Register

* bit 0 TXE : Transmit FIFO is Empty.
* bit 1 RXF : Receive FIFO is Full.
* bit 2 TXB : Transmit FIFO level is Below Threshold.
* bit 3 RXA : Receive FIFO level is Above Threshold.
* bit 4 BRK : Line Break; 13 consecutive 0's have been detected on the line.
* bit 5 MATCH : the receive data matches the MATCH register.
* bit 6 FE : Framing Error, the receiver does not see a "stop" bit at the expected "stop" bit time.
* bit 7 PRE : Parity Error; the receiver calculated parity does not match the received one.
* bit 8 OR : Overrun; data has been received but the RX FIFO is full.
* bit 9 RTO : Receiver Timeout; no data has been received for the time of a specified number of bits.



**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `MIS_value` The value of the Masked Interrupt Status Register


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_getMatchData`

_returns the value of the match data register_
```c
EF_DRIVER_STATUS EF_UART_getMatchData (
    EF_UART_TYPE *uart,
    uint32_t *MATCH_value
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `MATCH_value` The value of the match data register


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_getParityMode`

_This function return the parity mode of the UART._
```c
EF_DRIVER_STATUS EF_UART_getParityMode (
    EF_UART_TYPE *uart,
    uint32_t *parity_mode
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `parity` The parity mode of the UART


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_getPrescaler`

_returns the value of the prescaler_
```c
EF_DRIVER_STATUS EF_UART_getPrescaler (
    EF_UART_TYPE *uart,
    uint32_t *Prescaler_value
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `Prescaler_value` The value of the prescaler register


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_getRIS`

```c
EF_DRIVER_STATUS EF_UART_getRIS (
    EF_UART_TYPE *uart,
    uint32_t *RIS_value
) 
```


returns the value of the Raw Interrupt Status Register

* bit 0 TXE : Transmit FIFO is Empty.
* bit 1 RXF : Receive FIFO is Full.
* bit 2 TXB : Transmit FIFO level is Below Threshold.
* bit 3 RXA : Receive FIFO level is Above Threshold.
* bit 4 BRK : Line Break; 13 consecutive 0's have been detected on the line.
* bit 5 MATCH : the receive data matches the MATCH register.
* bit 6 FE : Framing Error, the receiver does not see a "stop" bit at the expected "stop" bit time.
* bit 7 PRE : Parity Error; the receiver calculated parity does not match the received one.
* bit 8 OR : Overrun; data has been received but the RX FIFO is full.
* bit 9 RTO : Receiver Timeout; no data has been received for the time of a specified number of bits.



**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `RIS_value` The value of the Raw Interrupt Status Register


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_getRxCount`

_returns the current level of the RX FIFO (the number of bytes in the FIFO)_
```c
EF_DRIVER_STATUS EF_UART_getRxCount (
    EF_UART_TYPE *uart,
    uint32_t *RX_FIFO_LEVEL_value
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `RX_FIFO_LEVEL_value` The value of the RX FIFO level register


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_getRxFIFOThreshold`

_returns the current value of the RX FIFO threshold_
```c
EF_DRIVER_STATUS EF_UART_getRxFIFOThreshold (
    EF_UART_TYPE *uart,
    uint32_t *RX_FIFO_THRESHOLD_value
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `RX_FIFO_THRESHOLD_value` The value of the RX FIFO threshold register


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_getTxCount`

_returns the current level of the TX FIFO (the number of bytes in the FIFO)_
```c
EF_DRIVER_STATUS EF_UART_getTxCount (
    EF_UART_TYPE *uart,
    uint32_t *TX_FIFO_LEVEL_value
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `TX_FIFO_LEVEL_value` The value of the TX FIFO level register


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_getTxFIFOThreshold`

_returns the current value of the TX FIFO threshold_
```c
EF_DRIVER_STATUS EF_UART_getTxFIFOThreshold (
    EF_UART_TYPE *uart,
    uint32_t *TX_FIFO_THRESHOLD_value
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `TX_FIFO_THRESHOLD_value` The value of the TX FIFO threshold register


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_readChar`

_recieve a single character through uart_
```c
EF_DRIVER_STATUS EF_UART_readChar (
    EF_UART_TYPE *uar,
    char *RXDATA_value
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `RXDATA_value` The value of the received character


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_readCharNonBlocking`

_This is a non-blocking function that reads a character from the UART receive FIFO if data is available and returns a status code._
```c
EF_DRIVER_STATUS EF_UART_readCharNonBlocking (
    EF_UART_TYPE *uart,
    char *RXDATA_value,
    bool *data_available
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `RXDATA_value` The value of the received character 
* `data_available` A flag indicating if data is available in the receive FIFO


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_setCTRL`

```c
EF_DRIVER_STATUS EF_UART_setCTRL (
    EF_UART_TYPE *uart,
    uint32_t value
) 
```


sets the control register to a certain value where

* bit 0: UART enable
* bit 1: UART Transmitter enable
* bit 2: UART Receiver enable
* bit 3: Loopback (connect RX and TX pins together) enable
* bit 4: UART Glitch Filer on RX enable



**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `value` The value of the control register


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_setConfig`

```c
EF_DRIVER_STATUS EF_UART_setConfig (
    EF_UART_TYPE *uart,
    uint32_t config
) 
```


sets the configuration register to a certain value where

* bit 0-3: Data word length: 5-9 bits
* bit 4: Two Stop Bits Select
* bit 5-7: Parity Type: 000: None, 001: odd, 010: even, 100: Sticky 0, 101: Sticky 1
* bit 8-13: Receiver Timeout measured in number of bits



**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `config` The value of the configuration register


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_setDataSize`

_sets the Data Size (Data word length: 5-9 bits ) by setting the "wlen" field in configuration register_
```c
EF_DRIVER_STATUS EF_UART_setDataSize (
    EF_UART_TYPE *uart,
    uint32_t value
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `value` The value of the required data word length 


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_setGclkEnable`

_sets the GCLK enable bit in the UART register to a certain value_
```c
EF_DRIVER_STATUS EF_UART_setGclkEnable (
    EF_UART_TYPE *uart,
    uint32_t value
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `value` The value of the GCLK enable bit


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_setICR`

```c
EF_DRIVER_STATUS EF_UART_setICR (
    EF_UART_TYPE *uart,
    uint32_t mask
) 
```


sets the value of the Interrupts Clear Register; write 1 to clear the flag

* bit 0 TXE : Transmit FIFO is Empty.
* bit 1 RXF : Receive FIFO is Full.
* bit 2 TXB : Transmit FIFO level is Below Threshold.
* bit 3 RXA : Receive FIFO level is Above Threshold.
* bit 4 BRK : Line Break; 13 consecutive 0's have been detected on the line.
* bit 5 MATCH : the receive data matches the MATCH register.
* bit 6 FE : Framing Error, the receiver does not see a "stop" bit at the expected "stop" bit time.
* bit 7 PRE : Parity Error; the receiver calculated parity does not match the received one.
* bit 8 OR : Overrun; data has been received but the RX FIFO is full.
* bit 9 RTO : Receiver Timeout; no data has been received for the time of a specified number of bits.



**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `mask` The required mask value


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_setIM`

```c
EF_DRIVER_STATUS EF_UART_setIM (
    EF_UART_TYPE *uart,
    uint32_t mask
) 
```


sets the value of the Interrupts Masking Register; which enable and disables interrupts

* bit 0 TXE : Transmit FIFO is Empty.
* bit 1 RXF : Receive FIFO is Full.
* bit 2 TXB : Transmit FIFO level is Below Threshold.
* bit 3 RXA : Receive FIFO level is Above Threshold.
* bit 4 BRK : Line Break; 13 consecutive 0's have been detected on the line.
* bit 5 MATCH : the receive data matches the MATCH register.
* bit 6 FE : Framing Error, the receiver does not see a "stop" bit at the expected "stop" bit time.
* bit 7 PRE : Parity Error; the receiver calculated parity does not match the received one.
* bit 8 OR : Overrun; data has been received but the RX FIFO is full.
* bit 9 RTO : Receiver Timeout; no data has been received for the time of a specified number of bits.



**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `mask` The required mask value


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_setMatchData`

_sets the matchData to a certain value at which "MATCH" interrupt will be raised_
```c
EF_DRIVER_STATUS EF_UART_setMatchData (
    EF_UART_TYPE *uart,
    uint32_t matchData
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `matchData` The value of the required match data 


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_setParityType`

_sets the "parity" field in configuration register (could be none, odd, even, sticky 0 or sticky 1)_
```c
EF_DRIVER_STATUS EF_UART_setParityType (
    EF_UART_TYPE *uart,
    enum parity_type parity
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `parity` enum parity\_type could be "NONE" , "ODD" , "EVEN" , "STICKY\_0" , or "STICKY\_1"


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_setPrescaler`

_sets the prescaler to a certain value where Baud\_rate = Bus\_Clock\_Freq/((Prescaler+1)\*16)_
```c
EF_DRIVER_STATUS EF_UART_setPrescaler (
    EF_UART_TYPE *uart,
    uint32_t prescaler
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `prescaler` The value of the required prescaler


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_setRxFIFOThreshold`

_sets the RX FIFO threshold to a certain value at which "RXA" interrupt will be raised_
```c
EF_DRIVER_STATUS EF_UART_setRxFIFOThreshold (
    EF_UART_TYPE *uart,
    uint32_t threshold
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `threshold` The value of the required threshold


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_setTimeoutBits`

_sets the "timeout" field in configuration register which is receiver timeout measured in number of bits at which the timeout flag will be raised_
```c
EF_DRIVER_STATUS EF_UART_setTimeoutBits (
    EF_UART_TYPE *uart,
    uint32_t value
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `value` timeout bits value


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_setTwoStopBitsSelect`

_sets the "stp2" bit in configuration register (whether the stop boits are two or one)_
```c
EF_DRIVER_STATUS EF_UART_setTwoStopBitsSelect (
    EF_UART_TYPE *uart,
    bool is_two_bits
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `is_two_bits` bool value, if "true", the stop bits are two and if "false", the stop bit is one


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_setTxFIFOThreshold`

_sets the TX FIFO threshold to a certain value at which "TXB" interrupt will be raised_
```c
EF_DRIVER_STATUS EF_UART_setTxFIFOThreshold (
    EF_UART_TYPE *uart,
    uint32_t threshold
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `threshold` The value of the required threshold


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_spaceAvailable`

_This function returns a flag indicating whether or not the transmit is available, i.e. the transmit FIFO is not full._
```c
EF_DRIVER_STATUS EF_UART_spaceAvailable (
    EF_UART_TYPE *uart,
    bool *flag
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `flag` a flag indicating if the transmit FIFO is not full


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_writeChar`

_transmit a single character through uart_
```c
EF_DRIVER_STATUS EF_UART_writeChar (
    EF_UART_TYPE *uart,
    char data
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `data` The character or byte required to send


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_writeCharArr`

_transmit an array of characters through uart_
```c
EF_DRIVER_STATUS EF_UART_writeCharArr (
    EF_UART_TYPE *uart,
    const char *char_arr
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `char_arr` An array of characters to send


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code
### function `EF_UART_writeCharNonBlocking`

_This is a non-blocking function that writes a character to the UART transmit FIFO if the FIFO is not full and returns a status code._
```c
EF_DRIVER_STATUS EF_UART_writeCharNonBlocking (
    EF_UART_TYPE *uart,
    char data,
    bool *data_sent
) 
```


**Parameters:**


* `uart` An [**EF\_UART\_TYPE**](#typedef-ef_uart_type) pointer, which points to the base memory address of UART registers.[**EF\_UART\_TYPE**](#typedef-ef_uart_type) is a structure that contains the UART registers.
* `data` The character or byte required to send 
* `data_sent` A flag indicating if the data was sent successfully


**Returns:**

status A value of type [**EF\_DRIVER\_STATUS**](#typedef-ef_driver_status) : returns a success or error code

## Macros Documentation

### define `EF_UART_CFG_REG_MAX_VALUE`

```c
#define EF_UART_CFG_REG_MAX_VALUE ((uint32_t)0x00001FFF)
```

### define `EF_UART_CFG_REG_TIMEOUT_MAX_VALUE`

```c
#define EF_UART_CFG_REG_TIMEOUT_MAX_VALUE ((uint32_t)0x0000003F)
```

### define `EF_UART_CTRL_REG_MAX_VALUE`

```c
#define EF_UART_CTRL_REG_MAX_VALUE ((uint32_t)0x0000001F)
```

### define `EF_UART_DataLength_MAX_VALUE`

```c
#define EF_UART_DataLength_MAX_VALUE ((uint32_t)0x00000009)
```

### define `EF_UART_DataLength_MIN_VALUE`

```c
#define EF_UART_DataLength_MIN_VALUE ((uint32_t)0x00000005)
```

### define `EF_UART_ERROR_RX_UNAVAILABLE`

```c
#define EF_UART_ERROR_RX_UNAVAILABLE -1
```

### define `EF_UART_ERROR_TX_UNAVAILABLE`

```c
#define EF_UART_ERROR_TX_UNAVAILABLE 1
```

### define `EF_UART_IC_REG_MAX_VALUE`

```c
#define EF_UART_IC_REG_MAX_VALUE ((uint32_t)0x000003FF)
```

### define `EF_UART_IM_REG_MAX_VALUE`

```c
#define EF_UART_IM_REG_MAX_VALUE ((uint32_t)0x000003FF)
```

### define `EF_UART_MATCH_REG_MAX_VALUE`

```c
#define EF_UART_MATCH_REG_MAX_VALUE ((uint32_t)0x00001FFF)
```

### define `EF_UART_PR_REG_MAX_VALUE`

```c
#define EF_UART_PR_REG_MAX_VALUE ((uint32_t)0x0000FFFF)
```

### define `EF_UART_RX_FIFO_THRESHOLD_REG_MAX_VALUE`

```c
#define EF_UART_RX_FIFO_THRESHOLD_REG_MAX_VALUE ((uint32_t)0x0000000F)
```

### define `EF_UART_SUCCESS`

```c
#define EF_UART_SUCCESS 0
```

### define `EF_UART_TX_FIFO_THRESHOLD_REG_MAX_VALUE`

```c
#define EF_UART_TX_FIFO_THRESHOLD_REG_MAX_VALUE ((uint32_t)0x0000000F)
```


## File EF_UART_regs.h





## Structures and Types

| Type | Name |
| ---: | :--- |
| typedef struct [**\_EF\_UART\_TYPE\_**](#struct-_ef_uart_type_) | [**EF\_UART\_TYPE**](#typedef-ef_uart_type)  <br> |
| struct | [**\_EF\_UART\_TYPE\_**](#struct-_ef_uart_type_) <br> |


## Macros

| Type | Name |
| ---: | :--- |
| define  | [**EF\_UART\_BRK\_FLAG**](#define-ef_uart_brk_flag)  0x10<br> |
| define  | [**EF\_UART\_CFG\_REG\_PARITY\_BIT**](#define-ef_uart_cfg_reg_parity_bit)  5<br> |
| define  | [**EF\_UART\_CFG\_REG\_PARITY\_MASK**](#define-ef_uart_cfg_reg_parity_mask)  0xe0<br> |
| define  | [**EF\_UART\_CFG\_REG\_STP2\_BIT**](#define-ef_uart_cfg_reg_stp2_bit)  4<br> |
| define  | [**EF\_UART\_CFG\_REG\_STP2\_MASK**](#define-ef_uart_cfg_reg_stp2_mask)  0x10<br> |
| define  | [**EF\_UART\_CFG\_REG\_TIMEOUT\_BIT**](#define-ef_uart_cfg_reg_timeout_bit)  8<br> |
| define  | [**EF\_UART\_CFG\_REG\_TIMEOUT\_MASK**](#define-ef_uart_cfg_reg_timeout_mask)  0x3f00<br> |
| define  | [**EF\_UART\_CFG\_REG\_WLEN\_BIT**](#define-ef_uart_cfg_reg_wlen_bit)  0<br> |
| define  | [**EF\_UART\_CFG\_REG\_WLEN\_MASK**](#define-ef_uart_cfg_reg_wlen_mask)  0xf<br> |
| define  | [**EF\_UART\_CTRL\_REG\_EN\_BIT**](#define-ef_uart_ctrl_reg_en_bit)  0<br> |
| define  | [**EF\_UART\_CTRL\_REG\_EN\_MASK**](#define-ef_uart_ctrl_reg_en_mask)  0x1<br> |
| define  | [**EF\_UART\_CTRL\_REG\_GFEN\_BIT**](#define-ef_uart_ctrl_reg_gfen_bit)  4<br> |
| define  | [**EF\_UART\_CTRL\_REG\_GFEN\_MASK**](#define-ef_uart_ctrl_reg_gfen_mask)  0x10<br> |
| define  | [**EF\_UART\_CTRL\_REG\_LPEN\_BIT**](#define-ef_uart_ctrl_reg_lpen_bit)  3<br> |
| define  | [**EF\_UART\_CTRL\_REG\_LPEN\_MASK**](#define-ef_uart_ctrl_reg_lpen_mask)  0x8<br> |
| define  | [**EF\_UART\_CTRL\_REG\_RXEN\_BIT**](#define-ef_uart_ctrl_reg_rxen_bit)  2<br> |
| define  | [**EF\_UART\_CTRL\_REG\_RXEN\_MASK**](#define-ef_uart_ctrl_reg_rxen_mask)  0x4<br> |
| define  | [**EF\_UART\_CTRL\_REG\_TXEN\_BIT**](#define-ef_uart_ctrl_reg_txen_bit)  1<br> |
| define  | [**EF\_UART\_CTRL\_REG\_TXEN\_MASK**](#define-ef_uart_ctrl_reg_txen_mask)  0x2<br> |
| define  | [**EF\_UART\_FE\_FLAG**](#define-ef_uart_fe_flag)  0x40<br> |
| define  | [**EF\_UART\_MATCH\_FLAG**](#define-ef_uart_match_flag)  0x20<br> |
| define  | [**EF\_UART\_OR\_FLAG**](#define-ef_uart_or_flag)  0x100<br> |
| define  | [**EF\_UART\_PRE\_FLAG**](#define-ef_uart_pre_flag)  0x80<br> |
| define  | [**EF\_UART\_RTO\_FLAG**](#define-ef_uart_rto_flag)  0x200<br> |
| define  | [**EF\_UART\_RXA\_FLAG**](#define-ef_uart_rxa_flag)  0x8<br> |
| define  | [**EF\_UART\_RXF\_FLAG**](#define-ef_uart_rxf_flag)  0x2<br> |
| define  | [**EF\_UART\_RX\_FIFO\_FLUSH\_REG\_FLUSH\_BIT**](#define-ef_uart_rx_fifo_flush_reg_flush_bit)  0<br> |
| define  | [**EF\_UART\_RX\_FIFO\_FLUSH\_REG\_FLUSH\_MASK**](#define-ef_uart_rx_fifo_flush_reg_flush_mask)  0x1<br> |
| define  | [**EF\_UART\_RX\_FIFO\_LEVEL\_REG\_LEVEL\_BIT**](#define-ef_uart_rx_fifo_level_reg_level_bit)  0<br> |
| define  | [**EF\_UART\_RX\_FIFO\_LEVEL\_REG\_LEVEL\_MASK**](#define-ef_uart_rx_fifo_level_reg_level_mask)  0xf<br> |
| define  | [**EF\_UART\_RX\_FIFO\_THRESHOLD\_REG\_THRESHOLD\_BIT**](#define-ef_uart_rx_fifo_threshold_reg_threshold_bit)  0<br> |
| define  | [**EF\_UART\_RX\_FIFO\_THRESHOLD\_REG\_THRESHOLD\_MASK**](#define-ef_uart_rx_fifo_threshold_reg_threshold_mask)  0xf<br> |
| define  | [**EF\_UART\_TXB\_FLAG**](#define-ef_uart_txb_flag)  0x4<br> |
| define  | [**EF\_UART\_TXE\_FLAG**](#define-ef_uart_txe_flag)  0x1<br> |
| define  | [**EF\_UART\_TX\_FIFO\_FLUSH\_REG\_FLUSH\_BIT**](#define-ef_uart_tx_fifo_flush_reg_flush_bit)  0<br> |
| define  | [**EF\_UART\_TX\_FIFO\_FLUSH\_REG\_FLUSH\_MASK**](#define-ef_uart_tx_fifo_flush_reg_flush_mask)  0x1<br> |
| define  | [**EF\_UART\_TX\_FIFO\_LEVEL\_REG\_LEVEL\_BIT**](#define-ef_uart_tx_fifo_level_reg_level_bit)  0<br> |
| define  | [**EF\_UART\_TX\_FIFO\_LEVEL\_REG\_LEVEL\_MASK**](#define-ef_uart_tx_fifo_level_reg_level_mask)  0xf<br> |
| define  | [**EF\_UART\_TX\_FIFO\_THRESHOLD\_REG\_THRESHOLD\_BIT**](#define-ef_uart_tx_fifo_threshold_reg_threshold_bit)  0<br> |
| define  | [**EF\_UART\_TX\_FIFO\_THRESHOLD\_REG\_THRESHOLD\_MASK**](#define-ef_uart_tx_fifo_threshold_reg_threshold_mask)  0xf<br> |
| define  | [**IO\_TYPES**](#define-io_types)  <br> |
| define  | [**\_\_R**](#define-__r)  volatile const unsigned int<br> |
| define  | [**\_\_RW**](#define-__rw)  volatile       unsigned int<br> |
| define  | [**\_\_W**](#define-__w)  volatile       unsigned int<br> |

## Structures and Types Documentation

### typedef `EF_UART_TYPE`

```c
typedef struct _EF_UART_TYPE_ EF_UART_TYPE;
```

### struct `_EF_UART_TYPE_`


Variables:

-  [**\_\_W**](#define-__w) CFG  

-  [**\_\_W**](#define-__w) CTRL  

-  [**\_\_W**](#define-__w) GCLK  

-  [**\_\_W**](#define-__w) IC  

-  [**\_\_RW**](#define-__rw) IM  

-  [**\_\_W**](#define-__w) MATCH  

-  [**\_\_R**](#define-__r) MIS  

-  [**\_\_W**](#define-__w) PR  

-  [**\_\_R**](#define-__r) RIS  

-  [**\_\_R**](#define-__r) RXDATA  

-  [**\_\_W**](#define-__w) RX_FIFO_FLUSH  

-  [**\_\_R**](#define-__r) RX_FIFO_LEVEL  

-  [**\_\_W**](#define-__w) RX_FIFO_THRESHOLD  

-  [**\_\_W**](#define-__w) TXDATA  

-  [**\_\_W**](#define-__w) TX_FIFO_FLUSH  

-  [**\_\_R**](#define-__r) TX_FIFO_LEVEL  

-  [**\_\_W**](#define-__w) TX_FIFO_THRESHOLD  

-  [**\_\_R**](#define-__r) reserved_0  

-  [**\_\_R**](#define-__r) reserved_1  

-  [**\_\_R**](#define-__r) reserved_2  

-  [**\_\_R**](#define-__r) reserved_3  



## Macros Documentation

### define `EF_UART_BRK_FLAG`

```c
#define EF_UART_BRK_FLAG 0x10
```

### define `EF_UART_CFG_REG_PARITY_BIT`

```c
#define EF_UART_CFG_REG_PARITY_BIT 5
```

### define `EF_UART_CFG_REG_PARITY_MASK`

```c
#define EF_UART_CFG_REG_PARITY_MASK 0xe0
```

### define `EF_UART_CFG_REG_STP2_BIT`

```c
#define EF_UART_CFG_REG_STP2_BIT 4
```

### define `EF_UART_CFG_REG_STP2_MASK`

```c
#define EF_UART_CFG_REG_STP2_MASK 0x10
```

### define `EF_UART_CFG_REG_TIMEOUT_BIT`

```c
#define EF_UART_CFG_REG_TIMEOUT_BIT 8
```

### define `EF_UART_CFG_REG_TIMEOUT_MASK`

```c
#define EF_UART_CFG_REG_TIMEOUT_MASK 0x3f00
```

### define `EF_UART_CFG_REG_WLEN_BIT`

```c
#define EF_UART_CFG_REG_WLEN_BIT 0
```

### define `EF_UART_CFG_REG_WLEN_MASK`

```c
#define EF_UART_CFG_REG_WLEN_MASK 0xf
```

### define `EF_UART_CTRL_REG_EN_BIT`

```c
#define EF_UART_CTRL_REG_EN_BIT 0
```

### define `EF_UART_CTRL_REG_EN_MASK`

```c
#define EF_UART_CTRL_REG_EN_MASK 0x1
```

### define `EF_UART_CTRL_REG_GFEN_BIT`

```c
#define EF_UART_CTRL_REG_GFEN_BIT 4
```

### define `EF_UART_CTRL_REG_GFEN_MASK`

```c
#define EF_UART_CTRL_REG_GFEN_MASK 0x10
```

### define `EF_UART_CTRL_REG_LPEN_BIT`

```c
#define EF_UART_CTRL_REG_LPEN_BIT 3
```

### define `EF_UART_CTRL_REG_LPEN_MASK`

```c
#define EF_UART_CTRL_REG_LPEN_MASK 0x8
```

### define `EF_UART_CTRL_REG_RXEN_BIT`

```c
#define EF_UART_CTRL_REG_RXEN_BIT 2
```

### define `EF_UART_CTRL_REG_RXEN_MASK`

```c
#define EF_UART_CTRL_REG_RXEN_MASK 0x4
```

### define `EF_UART_CTRL_REG_TXEN_BIT`

```c
#define EF_UART_CTRL_REG_TXEN_BIT 1
```

### define `EF_UART_CTRL_REG_TXEN_MASK`

```c
#define EF_UART_CTRL_REG_TXEN_MASK 0x2
```

### define `EF_UART_FE_FLAG`

```c
#define EF_UART_FE_FLAG 0x40
```

### define `EF_UART_MATCH_FLAG`

```c
#define EF_UART_MATCH_FLAG 0x20
```

### define `EF_UART_OR_FLAG`

```c
#define EF_UART_OR_FLAG 0x100
```

### define `EF_UART_PRE_FLAG`

```c
#define EF_UART_PRE_FLAG 0x80
```

### define `EF_UART_RTO_FLAG`

```c
#define EF_UART_RTO_FLAG 0x200
```

### define `EF_UART_RXA_FLAG`

```c
#define EF_UART_RXA_FLAG 0x8
```

### define `EF_UART_RXF_FLAG`

```c
#define EF_UART_RXF_FLAG 0x2
```

### define `EF_UART_RX_FIFO_FLUSH_REG_FLUSH_BIT`

```c
#define EF_UART_RX_FIFO_FLUSH_REG_FLUSH_BIT 0
```

### define `EF_UART_RX_FIFO_FLUSH_REG_FLUSH_MASK`

```c
#define EF_UART_RX_FIFO_FLUSH_REG_FLUSH_MASK 0x1
```

### define `EF_UART_RX_FIFO_LEVEL_REG_LEVEL_BIT`

```c
#define EF_UART_RX_FIFO_LEVEL_REG_LEVEL_BIT 0
```

### define `EF_UART_RX_FIFO_LEVEL_REG_LEVEL_MASK`

```c
#define EF_UART_RX_FIFO_LEVEL_REG_LEVEL_MASK 0xf
```

### define `EF_UART_RX_FIFO_THRESHOLD_REG_THRESHOLD_BIT`

```c
#define EF_UART_RX_FIFO_THRESHOLD_REG_THRESHOLD_BIT 0
```

### define `EF_UART_RX_FIFO_THRESHOLD_REG_THRESHOLD_MASK`

```c
#define EF_UART_RX_FIFO_THRESHOLD_REG_THRESHOLD_MASK 0xf
```

### define `EF_UART_TXB_FLAG`

```c
#define EF_UART_TXB_FLAG 0x4
```

### define `EF_UART_TXE_FLAG`

```c
#define EF_UART_TXE_FLAG 0x1
```

### define `EF_UART_TX_FIFO_FLUSH_REG_FLUSH_BIT`

```c
#define EF_UART_TX_FIFO_FLUSH_REG_FLUSH_BIT 0
```

### define `EF_UART_TX_FIFO_FLUSH_REG_FLUSH_MASK`

```c
#define EF_UART_TX_FIFO_FLUSH_REG_FLUSH_MASK 0x1
```

### define `EF_UART_TX_FIFO_LEVEL_REG_LEVEL_BIT`

```c
#define EF_UART_TX_FIFO_LEVEL_REG_LEVEL_BIT 0
```

### define `EF_UART_TX_FIFO_LEVEL_REG_LEVEL_MASK`

```c
#define EF_UART_TX_FIFO_LEVEL_REG_LEVEL_MASK 0xf
```

### define `EF_UART_TX_FIFO_THRESHOLD_REG_THRESHOLD_BIT`

```c
#define EF_UART_TX_FIFO_THRESHOLD_REG_THRESHOLD_BIT 0
```

### define `EF_UART_TX_FIFO_THRESHOLD_REG_THRESHOLD_MASK`

```c
#define EF_UART_TX_FIFO_THRESHOLD_REG_THRESHOLD_MASK 0xf
```

### define `IO_TYPES`

```c
#define IO_TYPES 
```

### define `__R`

```c
#define __R volatile const unsigned int
```

### define `__RW`

```c
#define __RW volatile       unsigned int
```

### define `__W`

```c
#define __W volatile       unsigned int
```



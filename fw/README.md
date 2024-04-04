## APIs Documentation

### EF_UART_enable

```cpp
void EF_UART_enable(
    uint32_t uart_base
)
```

enables using uart by setting "en" bit in the control register to 1 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


### EF_UART_disable

```cpp
void EF_UART_disable(
    uint32_t uart_base
)
```

disables using uart by clearing "en" bit in the control register 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


### EF_UART_enableRx

```cpp
void EF_UART_enableRx(
    uint32_t uart_base
)
```

enables using uart RX by setting uart "rxen" bit in the control register to 1 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


### EF_UART_disableRx

```cpp
void EF_UART_disableRx(
    uint32_t uart_base
)
```

disables using uart RX by clearing uart "rxen" bit in the control register 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


### EF_UART_enableTx

```cpp
void EF_UART_enableTx(
    uint32_t uart_base
)
```

enables using uart TX by setting uart "txen" bit in the control register to 1 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


### EF_UART_disableTx

```cpp
void EF_UART_disableTx(
    uint32_t uart_base
)
```

disables using uart TX by clearing uart "txen" bit in the control register 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


### EF_UART_enableLoopBack

```cpp
void EF_UART_enableLoopBack(
    uint32_t uart_base
)
```

enables loopback (connecting TX to RX signal) by setting "lpen" bit in the control register to 1 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


### EF_UART_disableLoopBack

```cpp
void EF_UART_disableLoopBack(
    uint32_t uart_base
)
```

disables loopback (connecting TX to RX signal) by clearing "lpen" bit in the control register 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


### EF_UART_enableGlitchFilter

```cpp
void EF_UART_enableGlitchFilter(
    uint32_t uart_base
)
```

enables glitch filter (filter out noise or glitches on the received signal) by setting "gfen" bit in the control register to 1 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


### EF_UART_disableGlitchFilter

```cpp
void EF_UART_disableGlitchFilter(
    uint32_t uart_base
)
```

disables glitch filter (filter out noise or glitches on the received signal) by clearing "gfen" bit in the control register 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


### EF_UART_setCTRL

```cpp
void EF_UART_setCTRL(
    uint32_t uart_base,
    int value
)
```


**Parameters**: 

  * **uart_base** The base memory address of UART registers. 
  * **value** The value of the control register 


sets the control register to a certain value where

* bit 0: UART enable
* bit 1: UART Transmitter enable
* bit 2: UART Receiver enable
* bit 3: Loopback (connect RX and TX pins together) enable
* bit 4: UART Glitch Filer on RX enable


### EF_UART_getCTRL

```cpp
int EF_UART_getCTRL(
    uint32_t uart_base
)
```

returns the value of the control register 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


**Return**: control register value 

### EF_UART_setPrescaler

```cpp
void EF_UART_setPrescaler(
    uint32_t uart_base,
    int prescaler
)
```

sets the prescaler to a certain value where Baud_rate = Bus_Clock_Freq/((Prescaler+1)*16) 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 
  * **prescaler** The value of the required prescaler 


### EF_UART_getPrescaler

```cpp
int EF_UART_getPrescaler(
    uint32_t uart_base
)
```

returns the value of the prescaler 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


**Return**: prescaler register value 

### EF_UART_setDataSize

```cpp
void EF_UART_setDataSize(
    uint32_t uart_base,
    int value
)
```

sets the Data Size (Data word length: 5-9 bits ) by setting the "wlen" field in configuration register 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 
  * **value** The value of the required data word length 


### EF_UART_setTwoStopBitsSelect

```cpp
void EF_UART_setTwoStopBitsSelect(
    uint32_t uart_base,
    bool is_two_bits
)
```

sets the "stp2" bit in configuration register (whether the stop bits are two or one) 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 
  * **is_two_bits** bool value, if "true", the stop bits are two and if "false", the stop bit is one 


### EF_UART_setParityType

```cpp
void EF_UART_setParityType(
    uint32_t uart_base,
    enum parity_type parity
)
```

sets the "parity" field in configuration register (could be none, odd, even, sticky 0 or sticky 1) 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 
  * **parity** enum parity_type could be "NONE" , "ODD" , "EVEN" , "STICKY_0" , or "STICKY_1" 


### EF_UART_setTimeoutBits

```cpp
void EF_UART_setTimeoutBits(
    uint32_t uart_base,
    int value
)
```

sets the "timeout" field in configuration register which is receiver timeout measured in number of bits at which the timeout flag will be raised 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 
  * **value** timeout bits value 


### EF_UART_setConfig

```cpp
void EF_UART_setConfig(
    uint32_t uart_base,
    int config
)
```


**Parameters**: 

  * **uart_base** The base memory address of UART registers. 
  * **config** The value of the configuration register 


sets the configuration register to a certain value where

* bit 0-3: Data word length: 5-9 bits
* bit 4: Two Stop Bits Select
* bit 5-7: Parity Type: 000: None, 001: odd, 010: even, 100: Sticky 0, 101: Sticky 1
* bit 8-13: Receiver Timeout measured in number of bits


### EF_UART_getConfig

```cpp
int EF_UART_getConfig(
    uint32_t uart_base
)
```

returns the value of the configuration register 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


**Return**: configuration register value 

### EF_UART_setRxFIFOThreshold

```cpp
void EF_UART_setRxFIFOThreshold(
    uint32_t uart_base,
    int threshold
)
```

sets the RX FIFO threshold to a certain value at which "RXA" interrupt will be raised 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 
  * **threshold** The value of the required threshold 


### EF_UART_getRxFIFOThreshold

```cpp
int EF_UART_getRxFIFOThreshold(
    uint32_t uart_base
)
```

returns the current value of the RX FIFO threshold 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


**Return**: RX FIFO threshold register 

### EF_UART_setTxFIFOThreshold

```cpp
void EF_UART_setTxFIFOThreshold(
    uint32_t uart_base,
    int threshold
)
```

sets the TX FIFO threshold to a certain value at which "TXB" interrupt will be raised 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 
  * **threshold** The value of the required threshold 


### EF_UART_getTxFIFOThreshold

```cpp
int EF_UART_getTxFIFOThreshold(
    uint32_t uart_base
)
```

returns the current value of the TX FIFO threshold 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


**Return**: TX FIFO threshold register 

### EF_UART_setFIFOControl

```cpp
void EF_UART_setFIFOControl(
    uint32_t uart_base,
    int value
)
```


**Parameters**: 

  * **uart_base** The base memory address of UART registers. 
  * **config** The value of the FIFO control register 


sets the FIFO control register to a certain value where

* bit 0-3: Transmit FIFO Level Threshold
* bit 8-11: Receive FIFO Level Threshold


### EF_UART_getFIFOControl

```cpp
int EF_UART_getFIFOControl(
    uint32_t uart_base
)
```

returns the value of the FIFO control register 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


**Return**: FIFO control register value 

### EF_UART_getTxCount

```cpp
int EF_UART_getTxCount(
    uint32_t uart_base
)
```

returns the current level of the TX FIFO (the number of bytes in the FIFO) 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


**Return**: TX FIFO level register 

### EF_UART_getRxCount

```cpp
int EF_UART_getRxCount(
    uint32_t uart_base
)
```

returns the current level of the RX FIFO (the number of bytes in the FIFO) 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


**Return**: RX FIFO level register 

### EF_UART_getFIFOStatus

```cpp
int EF_UART_getFIFOStatus(
    uint32_t uart_base
)
```


**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


**Return**: FIFO status register value 

returns the value of the FIFO status register where

* bit 0-3: Receive FIFO Level
* bit 8-11: Transmit FIFO Level


### EF_UART_setMatchData

```cpp
void EF_UART_setMatchData(
    uint32_t uart_base,
    int matchData
)
```

sets the matchData to a certain value at which "MATCH" interrupt will be raised 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 
  * **matchData** The value of the required match data 


### EF_UART_getMatchData

```cpp
int EF_UART_getMatchData(
    uint32_t uart_base
)
```

returns the value of the match data register 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


**Return**: match data register value 

### EF_UART_getRIS

```cpp
int EF_UART_getRIS(
    uint32_t uart_base
)
```


**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


**Return**: RIS register value 

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


### EF_UART_getMIS

```cpp
int EF_UART_getMIS(
    uint32_t uart_base
)
```


**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


**Return**: MIS register value 

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


### EF_UART_setIM

```cpp
void EF_UART_setIM(
    uint32_t uart_base,
    int mask
)
```


**Parameters**: 

  * **uart_base** The base memory address of UART registers. 
  * **mask** The required mask value 


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


### EF_UART_getIM

```cpp
int EF_UART_getIM(
    uint32_t uart_base
)
```


**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


**Return**: IM register value 

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


### EF_UART_setICR

```cpp
void EF_UART_setICR(
    uint32_t uart_base,
    int mask
)
```


**Parameters**: 

  * **uart_base** The base memory address of UART registers. 
  * **mask** The required mask value 


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


### EF_UART_writeChar

```cpp
void EF_UART_writeChar(
    uint32_t uart_base,
    char data
)
```

transmit a single character through uart 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 
  * **data** The character or byte required to send 


### EF_UART_writeCharArr

```cpp
void EF_UART_writeCharArr(
    uint32_t uart_base,
    const char * char_arr
)
```

transmit an array of characters through uart 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 
  * **char_arr** An array of characters to send 


### EF_UART_readChar

```cpp
int EF_UART_readChar(
    uint32_t uart_base
)
```

receive a single character through uart 

**Parameters**: 

  * **uart_base** The base memory address of UART registers. 


**Return**: the byte received 

-------------------------------
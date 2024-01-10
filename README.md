# EF_UART

A universal Asynchronous Receiver/Transmitter (UART) Soft IP with the following features:
- A configurable frame format
    - Data bits could vary from 5 to 9 bits
    - Even, odd, stick, or no-parity bit generation/detection
    - One or Two stop bit generation
- Line-break detection
- Configurable receiver timeout
- Loopback capability for testing/debugging
- Glitch Filter on RX enable
- Matching received data detection 
- 16-byte TX and RX FIFOs with programmable thresholds
- 16-bit prescaler (PR) for programable baud rate generation
- Ten Interrupt Sources:
    + RX FIFO is full
    + TX FIFO is empty
    + RX FIFO level is above the set threshold
    + TX FIFO level is below the set threshold
    + Line break detection
    + Receiver data match
    + Frame Error
    + Parity Error
    + Overrun
    + Receiver timeout 

## Registers

|register name|offset|size|mode|description|
|---|---|---|---|---|
|rxdata|0000|9|r|RX Data register|
|txdata|0004|9|w|TX Data register|
|prescaler|000c|16|w|Prescaler|
|control|0008|5|w|UART Control Register|
|config|0010|14|w|UART Configuration Register|
|fifo_control|0014|16|w|FIFO Control Register|
|fifo_status|0018|16|r|FIFO Status Register|
|match|001c|9|w|Match Register|
|IM|0f00|10|w|Interrupt Mask Register; check the flags table for more details|
|RIS|0f08|10|w|Raw Interrupt Status; check the flags table for more details|
|MIS|0f04|10|w|Masked Interrupt Status; check the flags table for more details|
|IC|0f0c|10|w|Interrupt Clear Register; check the flags table for more details|

### RX Data register [Offset: 0x0, mode: r]

RX Data register.

### TX Data register [Offset: 0x4, mode: w]

TX Data register

### Prescaler [Offset: 0xc, mode: w]

Prescaler

### UART Control Register [Offset: 0x8, mode: w]

UART Control Register

|bit|field name|width|description|
|---|---|---|---|
|0|en|1|UART enable|
|1|txen|1|UART Transmitter enable|
|2|rxen|1|UART Receiver enable|
|3|lpen|1|Loopback (connect RX and TX pins together) enable|
|4|gfen|1|UART Glitch Filer on RX enable|

### UART Configuration Register [Offset: 0x10, mode: w]

UART Configuration Register

|bit|field name|width|description|
|---|---|---|---|
|0|wlen|4|Data word length: 5-9 bits|
|4|stp2|1|Two Stop Bits Select|
|5|parity|3|Parity Type: 000: None, 001: odd, 010: even, 100: Sticky 0, 101: Sticky 1|
|8|timeout|6|Receiver Timeout measured in number of bits|

### FIFO Control Register [Offset: 0x14, mode: w]

FIFO Control Register

<img src="https://svg.wavedrom.com/{reg:[{name:'txfifotr', bits:4},{bits: 4},{name:'rxfifotr', bits:4},{bits: 20}], config: {lanes: 2, hflip: true}} "/>

|bit|field name|width|description|
|---|---|---|---|
|0|txfifotr|4|Transmit FIFO Level Threshold|
|8|rxfifotr|4|Receive FIFO Level Threshold|

### FIFO Status Register [Offset: 0x18, mode: r]

FIFO Status Register

|bit|field name|width|description|
|---|---|---|---|
|0|rx_level|4|Receive FIFO Level|
|8|tx_level|4|Transmit FIFO Level|

### Match Register [Offset: 0x1c, mode: w]

Match Register

## Interrupt Flags

|bit|flag|width|
|---|---|---|
|0|TX_EMPTY|1|
|1|RX_FULL|1|
|2|TX_LEVEL_BELOW|1|
|3|RX_LEVEL_ABOVE|1|
|4|LINE_BREAK|1|
|5|MATCH|1|
|6|FRAME_ERROR|1|
|7|PARITY_ERROR|1|
|8|OVERRUN|1|
|9|TIMEOUT|1|

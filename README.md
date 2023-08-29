# EF_UART
A universal Asynchronous Receiver/Transmitter (UART) Soft IP with the following features:
- A fixed fram format (8N1)
- 16-byte TX and RX FIFOs with programmable thresholds
- 16-bit prescaler (PR) for programable baud rate generation
- Four Interrupt Sources:
    + RX Fifo is full
    + TX Fifo is empty
    + RX Fifo level is above the set threshold
    + TX Fifo level is below the set threshold

The IP has a generic bus interface. Bus wrappers for AHB-Lite, APB and WB are provided; they are auto-generated using wrapper_gen.py 


## I/O Registers
| Register | Offset | Mode         | Size | Description |
| -------- | ------ | ------------ | ------|----- |
| TX Data      | 0x000  | W        | 8|Write data to TX FIFO   |
| RX Data      | 0x004  | R        | 8|Read data from RX FIFO  |
| Prescaler | 0x008  | RW        | 16| ```Baud_rate = Bus_Clock_Freq/((Prescaler+1)*16)```|
| TX FIFO Level      | 0x00C  | R |4       | The TX FIFO data level (number of bytes in the FIFO) |
| RX FIFO Level      | 0x010  | R |4       | The RX FIFO data level (number of bytes in the FIFO) |
| TX FIFO Level Threshold| 0x014   | RW| 4|TX FIFO: fire an interrupt if level < threshold |
| RX FIFO Level Threshold| 0x018   | RW| 4|RX FIFO: fire an interrupt if level > threshold |
| Control| 0x01C| RW | 3|Control; Bit 0: UART Enable, Bit 1: TX Enable, Bit 2: RX Enable |
| RIS | 0xF00 | R | 4|Raw Status Register |
| MIS | 0xF04 | R |  4|Masked Status Register |
| IM | 0xF08 | RW |  4|Interrupts Masking Register; enable and disables interrupts |
| IC | 0xF0C | W |  4|Interrupts Clear Register; write 1 to clear the flag |

## Interrupt flags 
The following applies to registers: RIS, MIS, IM and IC.
|bit|flag|
|---|----|
|0| TX FIFO is Empty |
|1| TX FIFO level is below the value in the TX FIFO Level Threshold Register |
|2| RX FIFO is Full |
|3| RX FIFO level is above the value in the RX FIFO Level Threshold Register |

## Control Register fields
|Bit|Function|
|---|----|
|0| UART Enable |
|1| Transmitter Enable |
|2| Receiver Enable |

# EF_UART
A universal Asynchronous Receiver/Transmitter (UART) Soft IP with the following features:
- A fixed fram format (8N1)
- 16-byte TX and RX FIFOs with programmable thresholds
- 16-bit prescaler (PR) for programable baud rate generation
- Programmable baud rate, ```Baud_rate = CLK/((PR+1)*16)```
- Four Interrupt Sources:
    + RX Fifo is full
    + TX Fifo is empty
    + RX Fifo level is above the set level
    + TX Fifo level is below the set level

The IP comes with wrappers for both the Wishbone (classical) and APB buses.

## The Interface
### EF_UART
<img src="./doc/EF_UART.svg" alt= “” width="60%" height="60%">

### EF_UART_wb
<img src="./doc/EF_UART_wb.svg" alt= “” width="60%" height="60%">

### EF_UART_apb
<img src="./doc/EF_UART_apb.svg" alt= “” width="60%" height="60%">

## I/O Registers
| Register | Offset | Mode         | Description |
| -------- | ------ | ------------ | ----------- |
| Data      | 0x000  | RW        | Read data from RX FIFO or write data tp TX FIFO   |
| Prescaler | 0x004  | RW        | ```Baud_rate = Bus_Clock_Freq/((Prescale+1)*16)```|
| TXFILS| 0x008   | RW| TX FIFO Interrupt Level Select|
| RXFILS| 0x00C   | RW| RX FIFO Interrupt Level Select|
| CTRL| 0x100 | RW | Control; Bit 0: UART Enable, Bit 1: TX Enable, Bit 2: RX Enable |
| RIS | 0x200 | R | Raw Status Register |
| MIS | 0x204 | R | Masked Status Register |
| IM | 0x208 | RW | Interrupts Masking Register; enable and disables interrupts |
| ICR | 0x20C | W | Interrupts Clear Register; write 1 to clear the flag |
### Data Register [offset: 0x000, RW]
![Diagram](./doc/data.svg "Diagram")
### Prescaler Register [offset: 0x004, RW]
![Diagram](./doc/prescaler.svg "Diagram")
### TXFILS (TX FIFO Interrupt Level Select) [offset: 0x008, RW]
![Diagram](./doc/txifls.svg "Diagram")
### RXFILS (RX FIFO Interrupt Level Select) [offset: 0x00c, RW]
![Diagram](./doc/rxifls.svg "Diagram")
### CTRL (Control Register) [offset: 0x100, R]
![Diagram](./doc/ctrl.svg "Diagram")
### RIS (Raw Interrupts Status Register) [offset: 0x200, R]
Reflects the status of interrupts trigger conditions detected (raw, prior to masking). 
![Diagram](./doc/flags.svg "Diagram")
- TXFE: TX FIFO is empty
- TXFL: TX FIFO Level is below the set level
- RXFF: RX FIFO is full
- RXFL: RX FIFO Level is above the set level

### RIS (Masked Interrupts Status Register) [offset: 0x204, R]
Similar to RIS but shows the state of the interrupt after masking. MIS register is hardwired to: ```RIS & IM```.
![Diagram](./doc/flags.svg "Diagram")

### IM (Interrupts Mask Register) [offset: 0x208, RW]
Disabling/Enabling an interrupt source.
![Diagram](./doc/flags.svg "Diagram")

### ICR (Interrupts Clear Register) [offset: 0x20c, W]
Writing a 1 to a bit in this register clears the corresponding interrupt flag in the RIS Register. 
![Diagram](./doc/flags.svg "Diagram")

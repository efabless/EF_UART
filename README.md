# ms_uart
A universal Asynchronous Receiver/Transmitter (UART) Soft IP with the following features:
- A fixed fram format (8N1)
- 16-byte TX and RX FIFOs with programmable thresholds
- 16-bit prescaler (PR) for programable baud rate generation
- Programmable baud rate, ```Baud_rate = CLK/((PR+1)*16)```
- Four Interrupt Sources:
    + RX Fifo is full
    + TX Fifo is empty
    + RX Fifo level is above the set threshold
    + TX Fifo level is below the set threshold

The IP comes with wrappers for both the WB (classical) and APB buses.
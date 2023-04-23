# ms_uart
A universal Asynchronous Receiver/Transmitter (UART) IP with the following features:
- A fixed fram format (8N1)
- 16-byte TX and RX FIFOs with programmable thresholds
- 16-bit prescaler (PR) for programable baud rate generation
- Programmable baud rate, ```Baud_rate = CLK/((PR+1)*16)```
- Four Interrupt Sources:
    + TX Fifo not full
    + RX Fifo not empty
    + RX Fifo level exceeded the threshold
    + TX Fifo level is below the threshold
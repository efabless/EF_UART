#ifndef EF_UART_C
#define EF_UART_C

#include <EF_UART.h>


void EF_UART_enable(uint32_t uart_base){
   
    EF_UART_TYPE* uart = (EF_UART_TYPE*)uart_base;
    uart->control |= 0x1;
}

void EF_UART_disable(uint32_t uart_base){
   
    EF_UART_TYPE* uart = (EF_UART_TYPE*)uart_base;
    uart->control &= 0xFFFFFFFE;
}

void EF_UART_enableRx(uint32_t uart_base){
    
    EF_UART_TYPE* uart = (EF_UART_TYPE*)uart_base;
    uart->control |= 0x4;
}

void EF_UART_disableRx(uint32_t uart_base){
    
    EF_UART_TYPE* uart = (EF_UART_TYPE*)uart_base;
    uart->control  &= 0xFFFFFFFB;
}

void EF_UART_enableTx(uint32_t uart_base){
    
    EF_UART_TYPE* uart = (EF_UART_TYPE*)uart_base;
    uart->control |= 0x2;
}

void EF_UART_disableTx(uint32_t uart_base){
    
    EF_UART_TYPE* uart = (EF_UART_TYPE*)uart_base;
    uart->control  &= 0xFFFFFFFD;
}

int EF_UART_getTxFifoLevel(uint32_t uart_base){

    EF_UART_TYPE* uart = (EF_UART_TYPE*)uart_base;
    return (uart->TXFIFOLEVEL);
}

int EF_UART_getRxFifoLevel(uint32_t uart_base){

    EF_UART_TYPE* uart = (EF_UART_TYPE*)uart_base;
    return (uart->RXFIFOLEVEL);
}

void EF_UART_setPrescaler(uint32_t uart_base, int prescaler){

    EF_UART_TYPE* uart = (EF_UART_TYPE*)uart_base;
    uart->prescale = prescaler;
}

int EF_UART_getPrescaler(uint32_t uart_base){

   EF_UART_TYPE* uart = (EF_UART_TYPE*)uart_base;
    return (uart->prescale);
}

 // Interrupts bits in RIS, MIS, IM, and ICR
 // bit 0: TX FIFO is Empty
 // bit 1: TX FIFO level is below the value in the TX FIFO Level Threshold Register
 // bit 2: RX FIFO is Full
 // bit 3: RX FIFO level is above the value in the RX FIFO Level Threshold Register

int EF_UART_getRIS(uint32_t uart_base){

    EF_UART_TYPE* uart = (EF_UART_TYPE*)uart_base;
    return (uart->ris);
}

int EF_UART_getMIS(uint32_t uart_base){

    EF_UART_TYPE* uart = (EF_UART_TYPE*)uart_base;
    return (uart->mis);
}

void EF_UART_setIM(uint32_t uart_base, int mask){
   
    EF_UART_TYPE* uart = (EF_UART_TYPE*)uart_base;
    uart->im = mask;
}

int EF_UART_getIM(uint32_t uart_base){

   EF_UART_TYPE* uart = (EF_UART_TYPE*)uart_base;
    return (uart->im);
}

void EF_UART_setICR(uint32_t uart_base, int mask){

    EF_UART_TYPE* uart = (EF_UART_TYPE*)uart_base;
    (uart->icr) = mask;
}
void EF_UART_clearIrqRxLevel(uint32_t uart_base){

    EF_UART_TYPE* uart = (EF_UART_TYPE*)uart_base;
    uart->icr |= 0x8;
}


void EF_UART_writeData(uint32_t uart_base, const char *p){

    EF_UART_TYPE* uart = (EF_UART_TYPE*)uart_base;
    while (*p)
        uart->txdata = (*(p++));
    EF_UART_setICR(uart_base, 0x1);
    while((EF_UART_getRIS(uart_base) & 0x1) == 0x0); // wait over TX empty  
}

void EF_UART_writeInt(uint32_t uart_base, int data){

    EF_UART_TYPE* uart = (EF_UART_TYPE*)uart_base;
    while((EF_UART_getRIS(uart_base) & 0x1) == 0x0); // wait over TX empty  
    uart->txdata = data;
    EF_UART_setICR(uart_base, 0x1);
}

int EF_UART_readData(uint32_t uart_base){

    EF_UART_TYPE* uart = (EF_UART_TYPE*)uart_base;
    while((EF_UART_getRIS(uart_base) & 0x8) == 0x0); // wait over RX fifo is empty Flag to unset  
    int data = uart->rxdata;
    EF_UART_clearIrqRxLevel(uart_base);
    return data;
}

#endif // EF_UART_C
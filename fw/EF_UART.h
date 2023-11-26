#ifndef EF_UART_H
#define EF_UART_H

#include <EF_UART_regs.h>
#include <stdint.h>

void EF_UART_enable(uint32_t uart_base);

void EF_UART_disable(uint32_t uart_base);

void EF_UART_enableRx(uint32_t uart_base);

void EF_UART_disableRx(uint32_t uart_base);

void EF_UART_enableTx(uint32_t uart_base);

void EF_UART_disableTx(uint32_t uart_base);

int EF_UART_getTxFifoLevel(uint32_t uart_base);

int EF_UART_getRxFifoLevel(uint32_t uart_base);

void EF_UART_setPrescaler(uint32_t uart_base, int prescaler);

int EF_UART_getPrescaler(uint32_t uart_base);

int EF_UART_getRIS(uint32_t uart_base);

int EF_UART_getMIS(uint32_t uart_base);

void EF_UART_setIM(uint32_t uart_base, int mask);

int EF_UART_getIM(uint32_t uart_base);

void EF_UART_setICR(uint32_t uart_base, int mask);

void EF_UART_clearIrqRxLevel(uint32_t uart_base);

void EF_UART_writeData(uint32_t uart_base, const char *p);

void EF_UART_writeInt(uint32_t uart_base, int data);

int EF_UART_readData(uint32_t uart_base);

#endif
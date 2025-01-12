#include "EF_UART.h"

#define Example_UART_BASE_ADDRESS 0x40000000
#define UART0 ((EF_UART_TYPE_PTR)Example_UART_BASE_ADDRESS)

// Example usage
int main() {
    EF_DRIVER_STATUS status;

    // Initialize UART with required configurations
    status = UART_Init(UART0, 9600, 16000000, 8, false, EVEN, 10, 4, 4);
    if (status != EF_DRIVER_OK) {
        return -1;
    }

    // Transmit a message
    const char *message = "Hello, UART!\n";
    status = EF_UART_writeCharArr(UART0, message);
    if (status != EF_DRIVER_OK) {
        // Handle transmission error
        return -1;
    }

    // Receive a message
    char buffer[100];
    status = UART_Receive(UART0, buffer, sizeof(buffer));
    if (status == EF_DRIVER_OK) {
        // Print received message
        printf("Received: %s\n", buffer);
    } else {
        // Handle reception error
        return -1;
    }

    return 0;
}

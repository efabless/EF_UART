#include "EF_UART.h"

// Function to initialize and configure the UART
EF_DRIVER_STATUS UART_Init(EF_UART_TYPE_PTR uart, uint32_t baud_rate, uint32_t bus_clock, uint32_t data_bits, bool two_stop_bits, enum parity_type parity, uint32_t timeout, uint32_t rx_threshold, uint32_t tx_threshold) {
    EF_DRIVER_STATUS status;

    // Calculate and set the prescaler
    uint32_t prescaler = (bus_clock / (baud_rate * 16)) - 1;
    status = EF_UART_setPrescaler(uart, prescaler);
    if (status != EF_DRIVER_OK) return status;

    // Configure data bits, stop bits, and parity

    // Set data bits (5-9 bits)
    status = EF_UART_setDataSize(uart, data_bits);
    if (status != EF_DRIVER_OK) return status;

    // Set stop bits (1 or 2)
    status = EF_UART_setTwoStopBitsSelect(uart, two_stop_bits);
    if (status != EF_DRIVER_OK) return status;

    // Set parity type
    status = EF_UART_setParityType(uart, parity);
    if (status != EF_DRIVER_OK) return status;

    // Set the receiver timeout value
    status = EF_UART_setTimeoutBits(uart, timeout);
    if (status != EF_DRIVER_OK) return status;

    // Set RX and TX FIFO thresholds
    status = EF_UART_setRxFIFOThreshold(uart, rx_threshold);
    if (status != EF_DRIVER_OK) return status;
    status = EF_UART_setTxFIFOThreshold(uart, tx_threshold);
    if (status != EF_DRIVER_OK) return status;

    // Enable the UART and both RX and TX
    status = EF_UART_enable(uart);
    if (status != EF_DRIVER_OK) return status;
    status = EF_UART_enableRx(uart);
    if (status != EF_DRIVER_OK) return status;
    status = EF_UART_enableTx(uart);
    if (status != EF_DRIVER_OK) return status;

    // Optionally enable glitch filter and loopback for testing
    status = EF_UART_enableGlitchFilter(uart);
    if (status != EF_DRIVER_OK) return status;
    status = EF_UART_enableLoopBack(uart);
    if (status != EF_DRIVER_OK) return status;

    return EF_DRIVER_OK;
}

// Function to transmit a string using UART
EF_DRIVER_STATUS UART_Transmit(EF_UART_TYPE_PTR uart, const char *data) {
    EF_DRIVER_STATUS status;
    while (*data) {
        bool space_available = false;
        status = EF_UART_spaceAvailable(uart, &space_available);
        if (status != EF_DRIVER_OK || !space_available) {
            // Wait or handle FIFO full case
            continue;
        }
        status = EF_UART_writeChar(uart, *data++);
        if (status != EF_DRIVER_OK) return status;
    }
    return EF_DRIVER_OK;
}

// Function to receive a string using UART
EF_DRIVER_STATUS UART_Receive(EF_UART_TYPE_PTR uart, char *buffer, size_t buffer_size) {
    EF_DRIVER_STATUS status;
    size_t index = 0;

    while (index < buffer_size - 1) {
        bool data_available = false;
        status = EF_UART_charsAvailable(uart, &data_available);
        if (status != EF_DRIVER_OK || !data_available) {
            // Wait or handle no data case
            continue;
        }
        char received_char;
        status = EF_UART_readChar(uart, &received_char);
        if (status != EF_DRIVER_OK) return status;

        buffer[index++] = received_char;
        if (received_char == '\n') break; // Stop at newline
    }
    buffer[index] = '\0'; // Null-terminate the string
    return EF_DRIVER_OK;
}


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
    status = UART_Transmit(UART0, message);
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

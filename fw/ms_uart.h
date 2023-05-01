#define MS_UART_BASE                0x10000000

#define MS_UART_DATA_REG_ADDR       (MS_UART_BASE +  0x00)
#define MS_UART_PRESCALE_REG_ADDR   (MS_UART_BASE +  0x04)
#define MS_UART_TXFIFOTR_REG_ADDR   (MS_UART_BASE +  0x08)
#define MS_UART_RXFIFOTR_REG_ADDR   (MS_UART_BASE +  0x0C)
#define MS_UART_CTRL_REG_ADDR       (MS_UART_BASE +  0x100)
#define MS_UART_RIS_REG_ADDR        (MS_UART_BASE +  0x200)
#define MS_UART_MIS_REG_ADDR        (MS_UART_BASE +  0x204)
#define MS_UART_IM_REG_ADDR         (MS_UART_BASE +  0x208)
#define MS_UART_ICR_REG_ADDR        (MS_UART_BASE +  0x20C)

#define MS_UART_CTRL_EN             0x1

#define MS_UART_TX_FIFO_FULL        0x01
#define MS_UART_TX_FIFO_EMPTY       0x02
#define MS_UART_TX_FIFO_BELOW       0x04
#define MS_UART_RX_FIFO_FULL        0x08
#define MS_UART_RX_FIFO_EMPTY       0x10
#define MS_UART_RX_FIFO_ABOVE       0x20


volatile unsigned int * ms_uart_data_reg        = (volatile unsigned int *) (MS_UART_DATA_REG_ADDR    );
volatile unsigned int * ms_uart_prescale_reg    = (volatile unsigned int *) (MS_UART_PRESCALE_REG_ADDR);
volatile unsigned int * ms_uart_txfifotr_reg    = (volatile unsigned int *) (MS_UART_TXFIFOTR_REG_ADDR);
volatile unsigned int * ms_uart_rxfifotr_reg    = (volatile unsigned int *) (MS_UART_RXFIFOTR_REG_ADDR);
volatile unsigned int * ms_uart_ctrl_reg        = (volatile unsigned int *) (MS_UART_CTRL_REG_ADDR    );
volatile unsigned int * ms_uart_ris_reg         = (volatile unsigned int *) (MS_UART_RIS_REG_ADDR     );
volatile unsigned int * ms_uart_mis_reg         = (volatile unsigned int *) (MS_UART_MIS_REG_ADDR     );
volatile unsigned int * ms_uart_im_reg          = (volatile unsigned int *) (MS_UART_IM_REG_ADDR      );
volatile unsigned int * ms_uart_icr_reg         = (volatile unsigned int *) (MS_UART_ICR_REG_ADDR     );
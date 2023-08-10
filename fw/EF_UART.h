#define EF_UART_BASE                0x10000000

#define EF_UART_DATA_REG_ADDR       (EF_UART_BASE +  0x00)
#define EF_UART_PRESCALE_REG_ADDR   (EF_UART_BASE +  0x04)
#define EF_UART_TXFIFOTR_REG_ADDR   (EF_UART_BASE +  0x08)
#define EF_UART_RXFIFOTR_REG_ADDR   (EF_UART_BASE +  0x0C)
#define EF_UART_CTRL_REG_ADDR       (EF_UART_BASE +  0x100)
#define EF_UART_RIS_REG_ADDR        (EF_UART_BASE +  0x200)
#define EF_UART_MIS_REG_ADDR        (EF_UART_BASE +  0x204)
#define EF_UART_IM_REG_ADDR         (EF_UART_BASE +  0x208)
#define EF_UART_ICR_REG_ADDR        (EF_UART_BASE +  0x20C)

#define EF_UART_CTRL_EN             0x1
#define EF_UART_CTRL_TXEN           0x2
#define EF_UART_CTRL_TXEN           0x4

#define EF_UART_TX_FIFO_FULL        0x01
#define EF_UART_TX_FIFO_EMPTY       0x02
#define EF_UART_TX_FIFO_BELOW       0x04
#define EF_UART_RX_FIFO_FULL        0x08
#define EF_UART_RX_FIFO_EMPTY       0x10
#define EF_UART_RX_FIFO_ABOVE       0x20


volatile unsigned int * EF_UART_data_reg        = (volatile unsigned int *) (EF_UART_DATA_REG_ADDR    );
volatile unsigned int * EF_UART_prescale_reg    = (volatile unsigned int *) (EF_UART_PRESCALE_REG_ADDR);
volatile unsigned int * EF_UART_txfifotr_reg    = (volatile unsigned int *) (EF_UART_TXFIFOTR_REG_ADDR);
volatile unsigned int * EF_UART_rxfifotr_reg    = (volatile unsigned int *) (EF_UART_RXFIFOTR_REG_ADDR);
volatile unsigned int * EF_UART_ctrl_reg        = (volatile unsigned int *) (EF_UART_CTRL_REG_ADDR    );
volatile unsigned int * EF_UART_ris_reg         = (volatile unsigned int *) (EF_UART_RIS_REG_ADDR     );
volatile unsigned int * EF_UART_mis_reg         = (volatile unsigned int *) (EF_UART_MIS_REG_ADDR     );
volatile unsigned int * EF_UART_im_reg          = (volatile unsigned int *) (EF_UART_IM_REG_ADDR      );
volatile unsigned int * EF_UART_icr_reg         = (volatile unsigned int *) (EF_UART_ICR_REG_ADDR     );
from EF_UVM.ip_env.ip_logger.ip_logger import ip_logger
import cocotb 
from uvm.macros import uvm_component_utils
from uart_item.uart_item import uart_item

class uart_logger(ip_logger):
    def __init__(self, name="ip_logger", parent=None):
        super().__init__(name, parent)
        self.header = ['Time (ns)', 'Char', "Direction", "Word Length", "Parity"]
        self.col_widths = [10]* len(self.header)

    def logger_formatter(self, transaction):
        sim_time = f"{cocotb.utils.get_sim_time(units='ns')} ns"
        char = f"{chr(transaction.char)}({hex(transaction.char)})"
        direction = f"{'RX' if transaction.direction == uart_item.RX else 'TX'}"
        word_length = f"{transaction.word_length}"
        parity = f"{transaction.parity}"
        return [sim_time, char, direction, word_length, parity]


uvm_component_utils(uart_logger)

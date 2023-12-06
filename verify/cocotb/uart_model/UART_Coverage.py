from cocotb_coverage.coverage import CoverPoint
from cocotb_coverage.coverage import CoverCross


class UART_Coverage():
    def __init__(self, cov_hierarchy="uart") -> None:
        self.cov_hierarchy = cov_hierarchy
        # initialize coverage no covearge happened just sample nothing so the coverge is initialized
        self.uart_cov(None, do_sampling=False)

    def uart_cov(self, operation, do_sampling=True):
        prescale_size = 16
        @CoverPoint(
            f"{self.cov_hierarchy}.traffic.type",
            xf=lambda operation: operation.type,
            bins=["rx", "tx"]
        )
        @CoverPoint(
            f"{self.cov_hierarchy}.traffic.char",
            xf=lambda operation: ord(operation.char),
            bins=[(0x0, 0x10), (0x10, 0x20), (0x20, 0x30), (0x30, 0x40), (0x40, 0x50), (0x50, 0x60), (0x60, 0x70), (0x70, 0x80)],
            bins_labels=["0 to 0x10", "0x10 to 0x20", "0x20 to 0x30", "0x30 to 0x40", "0x40 to 0x50", "0x50 to 0x60", "0x60 to 0x70", "0x70 to 0x80"],
            rel=lambda val, b: b[0] <= val <= b[1]
        )
        @CoverPoint(
            f"{self.cov_hierarchy}.traffic.prescale_tx",
            xf=lambda operation: (operation.type ,operation.prescale),
            bins=[("tx", 1 << i, (1 << i + 1) - 1) if i != 0 else ("tx", 0, 1) for i in range(prescale_size)],
            bins_labels=[f"from {hex(1 << i)} to {hex((1 << i + 1) - 1)}" if i != 0 else f"from {hex(0)} to {hex(1)}" for i in range(prescale_size)],
            rel=lambda val, b: b[0] == val[0] and b[1] <= val[1] <= b[2]
        )
        @CoverPoint(
            f"{self.cov_hierarchy}.traffic.prescale_rx",
            xf=lambda operation: (operation.type ,operation.prescale),
            bins=[("rx", 1 << i, (1 << i + 1) - 1) if i != 0 else ("rx", 0, 1) for i in range(prescale_size)],
            bins_labels=[f"from {hex(1 << i)} to {hex((1 << i + 1) - 1)}" if i != 0 else f"from {hex(0)} to {hex(1)}" for i in range(prescale_size)],
            rel=lambda val, b: b[0] == val[0] and b[1] <= val[1] <= b[2]
        )
        @CoverCross(
            f"{self.cov_hierarchy}.traffic.cc_char_type",
            items=[
                f"{self.cov_hierarchy}.traffic.char",
                f"{self.cov_hierarchy}.traffic.type",
            ],
        )
        def sample(operation):
            pass
        if do_sampling:
            sample(operation)

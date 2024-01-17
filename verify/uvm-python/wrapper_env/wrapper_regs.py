import json
from uvm.macros.uvm_message_defines import uvm_info, uvm_error
from uvm.base.uvm_object_globals import UVM_HIGH, UVM_LOW
import yaml


class wrapper_regs():
    """
    The wrapper_regs class is used to initialize and manage a set of registers specified in a JSON or YAML file.
    """
    def __init__(self, design_file) -> None:
        self.tag = "wrapper_regs"
        with open(design_file, 'r') as file:
            if design_file.endswith('.json'):
                self.data = json.load(file)
            elif design_file.endswith('.yaml') or design_file.endswith('.yml'):
                self.data = yaml.safe_load(file)
        parameter_values = {param["name"]: param["default"] for param in self.data["parameters"]}
        self.replace_parameters(self.data, parameter_values)
        self.init_regs()
        uvm_info(self.tag, f"Regs: {self.data['registers']}", UVM_HIGH)

    def init_regs(self):
        regs = {}
        address = 0
        self.irq_exist = False
        if "flags" in self.data:
            size = len(self.data["flags"])
            reg_im = {'name': 'im', "offset" : 0xf00,'size': size, 'mode': 'w', 'fifo': "no","bit_access": "no", "val": 0}
            reg_mis = {'name': 'mis', "offset" : 0xf04,'size': size, 'mode': 'r', 'fifo': "no","bit_access": "no", "val": 0}
            reg_ris = {'name': 'ris', "offset" : 0xf08,'size': size, 'mode': 'r', 'fifo': "no","bit_access": "no", "val": 0}
            reg_icr = {'name': 'icr', "offset" : 0xf0c, 'size': size, 'mode': 'wo', 'fifo': "no","bit_access": "no", "val": 0}
            address = 0xf00
            self.data["registers"].append(reg_im)
            self.data["registers"].append(reg_mis)
            self.data["registers"].append(reg_ris)
            self.data["registers"].append(reg_icr)
            self.irq_exist = True
        for reg in self.data["registers"]:
            if "init" not in reg:
                reg["val"] = 0
            else:
                reg["val"] = int(reg["init"][2:], 16)
            regs[int(reg["offset"])] = reg
        self.regs = regs
        self.reg_name_to_address = {info['name']: address for address, info in self.regs.items()}

    def get_regs(self):
        return self.regs

    def get_irq_exist(self):
        return self.irq_exist

    def write_reg_value(self, reg, value):
        """
            Writes a value to a register.
            Parameters:
                reg (int or str): The register to write to. If an integer is provided, it is treated as the address of the register. If a string is provided, it is treated as the name of the register and converted to its corresponding address using the `reg_name_to_address` dictionary.
                value: The value to write to the register.
            Returns:
                None
        """
        if type(reg) is int:
            address = reg
        elif type(reg) is str:
            address = self.reg_name_to_address[reg]
        else: 
            uvm_error(self.tag, f"Invalid reg type: {type(reg)} for write value: {value}")
        address = address & 0xffff
        if address in self.regs:
            uvm_info(self.tag, f"value before write {value} to address {hex(address)}: {hex(self.regs[address]['val'])}", UVM_HIGH)
            if "w" in self.regs[address]["mode"]:
                self.regs[address]["val"] = value & ((1 << int(self.regs[address]["size"])) - 1)
            uvm_info(self.tag, f"value after write to address {hex(address)}: {hex(self.regs[address]['val'])}", UVM_HIGH)

    def read_reg_value(self, reg):
        if type(reg) is int:
            address = reg
        elif type(reg) is str:
            address = self.reg_name_to_address[reg]
        else: 
            uvm_error(self.tag, f"Invalid reg type: {type(reg)} for read")
        address = address & 0xffff
        return self.regs[address]["val"]
    
    # Function to replace parameter values in the data
    def replace_parameters(self, data, parameter_values):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and value in parameter_values:
                    data[key] = parameter_values[value]
                else:
                    self.replace_parameters(value, parameter_values)
        elif isinstance(data, list):
            for item in data:
                self.replace_parameters(item, parameter_values)


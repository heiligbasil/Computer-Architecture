"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.HLT = 0b00000001
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.MUL = 0b10100010
        self.branch_table = dict()
        self.branch_table[self.HLT] = self.fun_hlt
        self.branch_table[self.LDI] = self.fun_ldi
        self.branch_table[self.PRN] = self.fun_prn
        self.branch_table[self.MUL] = self.fun_mul

    def load(self, program_file):
        """Load a program into memory."""
        address = 0
        try:
            with open(program_file) as file:
                for each_line in file:
                    broken_line = each_line.split('#')
                    instruction = broken_line[0].strip()
                    if instruction != '':
                        self.ram[address] = int(instruction, 2)
                        address += 1
        except FileNotFoundError:
            print(f"File '{program_file}' not found")
            sys.exit(2)

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def alu(self, op, reg_a, reg_b):
        """ALU operations"""
        if op == 'ADD':
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """Handy function to print out the CPU state. You might want to call this from run() if you need help debugging"""
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')
        for i in range(8):
            print(" %02X" % self.reg[i], end='')
        print()

    def run(self):
        """Run the CPU"""
        # self.trace()
        while self.pc < len(self.ram):
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            try:
                self.branch_table[ir](operand_a, operand_b)
                self.pc += (ir >> 6) + 1
            except KeyError:
                print(f'Unknown instruction: {ir}')
                exit(2)

    @staticmethod
    def fun_hlt(operand_a, operand_b):
        print('HLT encountered... exiting.')
        exit(1)

    def fun_ldi(self, operand_a, operand_b):
        print('LDI encountered... registering...')
        self.reg[operand_a] = operand_b

    def fun_prn(self, operand_a, operand_b):
        print('PRN encountered... printing...')
        print(self.reg[operand_a])

    def fun_mul(self, operand_a, operand_b):
        print('MUL encountered... multiplying...')
        self.alu('MUL', operand_a, operand_b)

"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.isr = 6
        self.sp = 7
        self.fl = 0b00000000
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.reg[self.sp] = 0xF4
        self.HLT = 0b00000001
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.PRA = 0b01001000
        self.ADD = 0b10100000
        self.MUL = 0b10100010
        self.PUS = 0b01000101
        self.POP = 0b01000110
        self.CAL = 0b01010000
        self.RET = 0b00010001
        self.CMP = 0b10100111
        self.JMP = 0b01010100
        self.JEQ = 0b01010101
        self.JNE = 0b01010110
        self.ST = 0b10000100
        self.branch_table = dict()
        self.branch_table[self.HLT] = self.fun_hlt
        self.branch_table[self.LDI] = self.fun_ldi
        self.branch_table[self.PRN] = self.fun_prn
        self.branch_table[self.PRA] = self.fun_pra
        self.branch_table[self.ADD] = self.fun_add
        self.branch_table[self.MUL] = self.fun_mul
        self.branch_table[self.PUS] = self.fun_pus
        self.branch_table[self.POP] = self.fun_pop
        self.branch_table[self.CAL] = self.fun_cal
        self.branch_table[self.RET] = self.fun_ret
        self.branch_table[self.CMP] = self.fun_cmp
        self.branch_table[self.JMP] = self.fun_jmp
        self.branch_table[self.JEQ] = self.fun_jeq
        self.branch_table[self.JNE] = self.fun_jne
        self.branch_table[self.ST] = self.fun_st

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
        elif op == 'CMP':
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b1
            else:
                self.fl = 0b0
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
                if ir not in [self.CAL, self.RET, self.JMP, self.JEQ, self.JNE]:
                    self.pc += ((ir >> 6) & 0xFF) + 1
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

    def fun_pra(self, operand_a, operand_b):
        print('PRA encountered... printing...')
        print(self.reg[operand_a])

    def fun_add(self, operand_a, operand_b):
        print('ADD encountered... adding...')
        self.alu('ADD', operand_a, operand_b)

    def fun_mul(self, operand_a, operand_b):
        print('MUL encountered... multiplying...')
        self.alu('MUL', operand_a, operand_b)

    def fun_pus(self, operand_a, operand_b):
        print('PUSH encountered... pushing to stack...')
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.reg[operand_a]

    def fun_pop(self, operand_a, operand_b):
        print('POP encountered... popping from stack...')
        self.reg[operand_a] = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1

    def fun_cal(self, operand_a, operand_b):
        print('CALL encountered... skipping to subroutine...')
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.pc + 2
        self.pc = self.reg[operand_a]

    def fun_ret(self, operand_a, operand_b):
        print('RET encountered... returning from subroutine...')
        self.pc = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1

    def fun_cmp(self, operand_a, operand_b):
        print('CMP encountered... comparing register values...')
        self.alu('CMP', operand_a, operand_b)

    def fun_jmp(self, operand_a, operand_b):
        print('JMP encountered... jumping...')
        self.pc = self.reg[operand_a]

    def fun_jeq(self, operand_a, operand_b):
        print('JEQ encountered... jumping if equal...')
        if self.fl == 0b1:
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2

    def fun_jne(self, operand_a, operand_b):
        print('JNE encountered... jumping if not equal...')
        if self.fl == 0b0:
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2

    def fun_st(self, operand_a, operand_b):
        print('ST encountered... registering...')
        self.ram_write(self.reg[operand_a], self.reg[operand_b])

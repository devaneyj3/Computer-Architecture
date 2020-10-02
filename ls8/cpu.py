"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.reg[7] = 0xf4
        self.halted = False

    # writing
    def ram_read(self, address):
        """accept the address to read and return the value stored there"""
        return self.ram[address]

    def ram_write(self, address, value):
        """accept a value to write, and the address to write it to"""
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0, 8  130
            0b00000000, # 0
            0b00001000, # 8
            0b01000111, # PRN R0 71
            0b00000000, # 0
            0b00000001, # HLT #1
        ]

        for instruction in program:
            self.ram[address] = instruction
            print(f'self.ram[address]:{self.ram[address]} = instruction: {instruction}')
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD": # 160
            print(reg_a, reg_b)
            print(self.reg)
            # indexes
            self.reg[reg_a] += self.reg[reg_b]
            return self.reg[reg_a]
            

        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # Instruction Register, contains a copy of the currently executing instruction
        # if at 160

        LDI = 130
        HLT = 1
        PRN = 71

        while not self.halted:

            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == LDI:
                print("in here")
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == HLT:
                self.halted = True
                sys.exit(1)
            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2
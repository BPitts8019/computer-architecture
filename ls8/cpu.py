"""CPU functionality."""

import sys

### Registers ###
R0 = 0x00
R1 = 0x01
R2 = 0x02
R3 = 0x03
R4 = 0x04
R5 = 0x05
R6 = 0x06
R7 = 0x07

### OP-Codes ###
# ALU
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100
INC = 0b01100101
DEC = 0b01100110
CMP = 0b10100111
AND = 0b10101000
NOT = 0b01101001
OR = 0b10101010
XOR = 0b10101011
SHL = 0b10101100
SHR = 0b10101101

# PC Mutators
CALL = 0b01010000
RET = 0b00010001
INT = 0b01010010
IRET = 0b00010011
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
JGT = 0b01010111
JLT = 0b01011000
JLE = 0b01011001
JGE = 0b01011010

# Other
NOP = 0b00000000
HLT = 0b00000001
LDI = 0b10000010
LD = 0b10000011
ST = 0b10000100
PUSH = 0b01000101
POP = 0b01000110
PRN = 0b01000111
PRA = 0b01001000


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0

        self.perform_op = dict()
        self.perform_op[LDI] = self.ldi
        self.perform_op[PRN] = self.prn
        self.perform_op[HLT] = self.hlt
        self.perform_op[MUL] = self.mul

        self.is_running = False

    def ldi(self, *operands):
        self.reg[operands[0]] = operands[1]
        self.pc += 3

    def prn(self, *operands):
        print(self.reg[operands[0]])
        self.pc += 2

    def hlt(self, *operands):
        self.is_running = False
        self.pc += 1

    def mul(self, *operands):
        self.alu("MUL", *operands)
        self.pc += 3

    def load(self, program_path):
        """Load a program into memory."""
        address = 0

        try:
            with open(program_path) as program:
                for line in program:
                    split_line = line.split("#")
                    instruction = split_line[0].strip()
                    if instruction != "":
                        self.ram[address] = int(instruction, 2)
                        address += 1
        except:
            print(f"Cannot open file at \"{program_path}\"")
            self.shutdown(2)

    def shutdown(self, exit_code=0):
        print("Shutting Down...")
        exit(exit_code)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

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

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def run(self):
        """Run the CPU."""
        print("Running...")
        self.is_running = True
        while self.is_running:
            instruction_reg = self.ram_read(self.pc)
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)
            # print("--- Before OP ---")
            # self.trace()
            if instruction_reg in self.perform_op:
                self.perform_op[instruction_reg](op_a, op_b)
            else:
                print(f"Unknown Instruction {instruction_reg}")
                self.shutdown(1)
            # print("--- After OP ---")
            # self.trace()

        self.shutdown()

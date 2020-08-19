"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0]*256
        self.reg = [0]*8

    def load(self, file):
        """Load a program into memory."""

        address = 0
        # For now, we've just hardcoded a program:
        with open(file) as f:
            for line in f:
                instruction = line.split("#")
                n = instruction[0].strip()
                if n=="":
                    continue
                self.ram[address] = int(n,2)
                address+=1
            f.close()


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self,MAR):
        return self.ram[MAR]
    
    def ram_write(self,MAR,MDR):
        self.ram[MAR]=MDR

    def run(self):
        """Run the CPU."""
        running=True
        while running:
            # self.trace()
            IR = self.ram_read(self.pc) # insertion register
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if IR == HLT:
                running=False
            elif IR == LDI:
                self.reg[self.ram_read(self.pc+1)] = self.ram_read(self.pc+2)
                self.pc += 3
            elif IR == PRN:
                print("--",self.reg[self.ram_read(self.pc+1)])
                self.pc += 2
            elif IR == MUL:
                reg_a =  self.ram_read(self.pc + 1)
                self.alu("MUL",reg_a,reg_a+1)
                self.pc += 3






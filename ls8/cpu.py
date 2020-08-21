"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET  = 0b00010001
JMP  = 0b01010100
JNE  = 0b01010110
JEQ  = 0b01010101
MUL = 0b10100010
CMP  = 0b10100111
AND  = 0b10100000
OR   = 0b10101010
XOR  = 0b10101011
NOT  = 0b01101001
SHL  = 0b10101100
SHR  = 0b10101101
MOD  = 0b10100100

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0]*256
        self.reg = [0]*8 
        self.reg[7] = 0xF4 # SP
        self.sp = self.reg[7]

        self.L = 0
        self.G = 0
        self.E = 0


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
        elif op == "CMP":
            if self.reg[reg_a]>self.reg[reg_b]:
                self.G=1
            elif self.reg[reg_a]<self.reg[reg_b]:
                self.L=1
            else:
                self.E = 1
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
            elif IR == PUSH:
                self.sp -= 1
                reg_a = self.ram_read(self.pc+1)
                value = self.reg[reg_a]
                self.reg[reg_a] -= 1
                self.ram[self.sp]=value
                self.pc += 2
            elif IR == POP:
                reg_a = self.ram_read(self.pc+1)
                self.reg[reg_a] = self.ram[self.sp]
                self.sp += 1
                self.pc+=2
            elif IR == CALL:
                value = self.pc + 2
                self.pc -= 1
                self.ram[self.sp] = value
                value = self.ram[self.pc+1]
                self.pc = self.reg[value]
            elif IR == RET:
                value = self.ram[self.sp]
                self.sp += 1
                self.pc = value
            elif IR == CMP:
                reg_a = self.ram_read(self.pc+1)
                self.alu("CMP",reg_a,reg_a+1)
                self.pc+=3
            elif IR == JMP:
                value = self.ram[self.pc+1] # Jump to the address stored in the given register.
                self.pc = self.reg[value] # Set the `PC` to the address stored in the given register.
            elif IR == JNE:
                # If `E` flag is clear (false, 0), jump to the address stored in the given register.
                if self.E == 0:
                    value = self.ram[self.pc+1]
                    self.pc = self.reg[value]
                else:
                    self.pc += 2
            elif IR == JEQ:
                if self.E == 1:
                    value = self.ram[self.pc+1]
                    self.pc = self.reg[value]
                else:
                    self.pc += 2







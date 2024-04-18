# Calculator Program using PyASM

# Declare computer memory
DECLARE 0x0000 0xffff; # Clear all memory
SETBYTE 0xffff 0x0000; # Set debug breakpoint disable
DEBUGPT 0xffff;

# Commands list
STRINGV 0x0062 exit;
STRINGV 0x0067 add;
STRINGV 0x006b sub;
STRINGV 0x006f mul;
STRINGV 0x0073 div;
STRINGV 0x0077 mod;
STRINGV 0x007b pow;
STRINGV 0x007f sqr;

SECTION input;
STRINGV 0x0001 Enter your operation (exit, add, sub, mul, div, mod, pow, sqr):;
SYSCALL 0x0001 0x0001 0x0000;                      # Print prompt message (instruction, data sect, exit address)
DECLARE 0x0041 0x0049;                             # Declare variable to store user input
SYSCALL 0x0006 0x0041 0x0000;                      # Read user input as string

COMPARE 0x0041 0x0062;                             # Compare user input with exit command
SECTJMP end;                                       # Exit if user input is exit command
                                                   # Continue if user input is not exit command

DECLARE 0x004a 0x005e;                             # Declare variable to store user input
STRINGV 0x004a Enter first number: ;
SYSCALL 0x0001 0x004a 0x0000;                      # Print prompt message (instruction, data sect, exit address)
DECLARE 0x0082 0x008a;                             # Declare variable to store user input
SYSCALL 0x0004 0x0082 0x0000;                      # Read user input as int

STRINGV 0x004a Enter second number: ;
SYSCALL 0x0001 0x004a 0x0000;                      # Print prompt message (instruction, data sect, exit address)
DECLARE 0x008b 0x008e;                             # Declare variable to store user input
SYSCALL 0x0004 0x008b 0x0000;                      # Read user input as int

# Nested conditional statement
# Compare user input with specified command
COMPARE 0x0041 0x0067;                             # add
SECTJMP add;
COMPARE 0x0041 0x006b;                             # sub
SECTJMP sub;
COMPARE 0x0041 0x006f;                             # mul
SECTJMP mul;
COMPARE 0x0041 0x0073;                             # div
SECTJMP div;
COMPARE 0x0041 0x0077;                             # mod
SECTJMP mod;
COMPARE 0x0041 0x007b;                             # pow
SECTJMP pow;
COMPARE 0x0041 0x007f;                             # sqr
SECTJMP sqr;
DECLARE 0x0001 0x0040;
STRINGV 0x0001 Unknown operation!;
SYSCALL 0x0001 0x0001 0x0000;                      # Print prompt message (instruction, data sect, exit address)
DECLARE 0x0091 0x0093;
SETBYTE 0x0091 0x000d;
SETBYTE 0x0092 0x000a;
SETBYTE 0x0093 0x0000;
SYSCALL 0x0001 0x0091 0x0000;                      # Print newline
SECTJMP input;                                     # Continue if user input is not any
SECTEND input;

SECTION add;
calcadd 0x0082 0x008b;
SECTJMP result;
SECTEND add;

SECTION sub;
calcsub 0x0082 0x008b;
SECTJMP result;
SECTEND sub;

SECTION mul;
calcmul 0x0082 0x008b;
SECTJMP result;
SECTEND mul;

SECTION div;
calcdiv 0x0082 0x008b;
SECTJMP result;
SECTEND div;

SECTION mod;
calcmod 0x0082 0x008b;
SECTJMP result;
SECTEND mod;

SECTION pow;
calcpow 0x0082 0x008b;
SECTJMP result;
SECTEND pow;

SECTION sqr;
calcsqr 0x0082;
SECTJMP result;
SECTEND sqr;

SECTION result;
STRINGV 0x0090 Result: ;
SYSCALL 0x0001 0x0090 0x0000;                      # Print prompt message (instruction, data sect, exit address)
SYSCALL 0x0002 0x0082 0x0000;                      # Print result
DECLARE 0x0091 0x0093;
SETBYTE 0x0091 0x000d;
SETBYTE 0x0092 0x000a;
SETBYTE 0x0093 0x0000;
SYSCALL 0x0001 0x0091 0x0000;                      # Print newline
SECTJMP input;
SECTEND result;

SECTION end;
DECLARE 0x0000 0x0001;
SETBYTE 0x0000 0x0000;
SYSCALL 0x0000 0x0000 0x0000;
SECTEND end;

SECTJMP input;
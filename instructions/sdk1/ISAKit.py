import sys

import instructions.sdk1.compile as Compiler

from instructions.sdk1.Heap import Heap
from instructions.sdk1.Stack import Stack
from instructions.sdk1.DebugUtil import DebugUtil

def nextInstruction() -> str:
    DebugUtil.debugLine(f"Reading instruction at {Stack.ptr:04x} of {(len(Stack.data)-1):04x}...", end="")
    val = Stack.read(Stack.ptr)
    Stack.ptr += 1
    return val


def run(script: str, debugModeParameter: bool = False):
    DebugUtil.setDebugMode(debugModeParameter)
    scriptLinesPreprocess: list = Compiler.createHeader(script).strip().split("\n")
    scriptLines: list = []
    for line in scriptLinesPreprocess:
        scriptLines.extend(line.strip().split(";"))
    for line in scriptLines:
        if line.strip() == "":
            scriptLines.remove(line)
    stackSize = 0
    heapSize = 0
    isaversion = 0

    scriptLinesPreprocess = []
    for idx, line in enumerate(scriptLines):
        if line.startswith("VARSIZE "):
            # Get number of bytes
            heapSize = int(line.split(" ")[1], 16)
        elif line.startswith("EXESIZE "):
            # Get number of bytes
            stackSize = int(line.split(" ")[1], 16)
        elif line.startswith("ISAVERS "):
            # Get ISAVersion
            isaversion = int(line.split(" ")[1], 16)
        else:
            scriptLinesPreprocess.append(line)

    DebugUtil.debugLine(f"ISAVersion: {isaversion}")
    DebugUtil.debugLine(f"Stack size: {stackSize} bytes")
    DebugUtil.debugLine(f"Heap size: {heapSize} bytes")

    Stack.init(stackSize)
    for line in scriptLinesPreprocess:
        DebugUtil.debugLine(f"Pushing {len(line)} bytes, remaining {Stack.size - Stack.dataBytes} bytes of {Stack.size} bytes")
        Stack.push(line)

    # Execute the line
    DebugUtil.debugLine("==================STACK DUMP==================")
    DebugUtil.debugLine(Stack.dump())
    if DebugUtil.isDebugMode():
        with open("stackdump.txt", "w") as f:
            f.write(Stack.dump())
    DebugUtil.debugLine("================STACK DUMP END================")
    Heap.init(heapSize)

    while Stack.read(0) == 256 and Stack.ptr < len(Stack.data):
        instruction = nextInstruction()
        command = instruction.split(" ")[0].upper()
        parameter = instruction[len(command):].strip()

        DebugUtil.debugLine(f"[{command}]: {parameter}: ", end="")

        # Since section is declared, skip the instructions until SECTEND
        if command == "SECTION":
            DebugUtil.debugLine("Section started")
            while True:
                instruction = nextInstruction()
                if instruction.split(" ")[0] == "SECTEND":
                    DebugUtil.debugLine("Section ended")
                    break
            continue

        elif command == "SECTEND":
            DebugUtil.debugLine("Section ended")
            continue

        # Declare memory block
        elif command == "DECLARE":
            addresses = parameter.split(" ")
            dataBeginning = addresses[0]
            dataEnding = addresses[1]
            DebugUtil.debugLine(f"Declared memory block from {dataBeginning} to {dataEnding}")
            for i in range(int(dataBeginning, 16), int(dataEnding, 16) + 1):
                Heap.writeAt(i, 0)

        # Set memory block
        elif command == "SETBYTE":
            parameters = parameter.split(" ")
            address = parameters[0]
            data = parameters[1]
            DebugUtil.debugLine(f"Set memory block at {address}: {data}")
            Heap.writeAt(int(address, 16), int(data, 16))

        # Set memory block as string
        elif command == "STRINGV":
            parameters = parameter.split(" ")
            address = parameters[0]
            data = " ".join(parameters[1:])
            DebugUtil.debugLine(f"Set memory block at {address}: {data}", end="")
            Heap.writeAsString(int(address, 16), data)
            endPoint = int(address, 0) + len(data)
            DebugUtil.debugLine(f" (Ends at {endPoint:04x})")


        # Set memory block as integer
        elif command == "INT64VV":
            parameters = parameter.split(" ")
            address = parameters[0]
            data = int(parameters[1], 0)
            DebugUtil.debugLine(f"Set memory block at {address}: {data}")
            Heap.writeAsInt64(int(address, 16), data)

        # Jump to section
        elif command == "SECTJMP":
            section = int(parameter, 16)
            DebugUtil.debugLine(f"Jumping to section {section:04x}")
            Stack.ptr = section
            continue

        # String compare
        elif command == "COMPARE":
            parameters = parameter.split(" ")
            address1 = int(parameters[0], 16)
            address2 = int(parameters[1], 16)
            DebugUtil.debugLine(f"Comparing string at {address1} with {address2}")
            if Heap.readAsString(address1) == Heap.readAsString(address2):
                continue
            else:
                Stack.ptr += 1
                continue

        # Compare memory block (greater than)
        elif command == "CMPGRTR":
            parameters = parameter.split(" ")
            address1 = parameters[0]
            address2 = parameters[1]
            DebugUtil.debugLine(f"Comparing memory block at {address1} with {address2}")
            if Heap.readAsInt64(int(address1, 16)) > Heap.readAsInt64(int(address2, 16)):
                continue
            else:
                Stack.ptr += 1
                continue

        # Compare memory block (less than)
        elif command == "CMPLESS":
            parameters = parameter.split(" ")
            address1 = parameters[0]
            address2 = parameters[1]
            DebugUtil.debugLine(f"Comparing memory block at {address1} with {address2}")
            if Heap.readAsInt64(int(address1, 16)) < Heap.readAsInt64(int(address2, 16)):
                continue
            else:
                Stack.ptr += 1
                continue

        # Compare memory block (equal)
        elif command == "CMPEQUL":
            parameters = parameter.split(" ")
            address1 = parameters[0]
            address2 = parameters[1]
            DebugUtil.debugLine(f"Comparing memory block at {address1} with {address2}")
            if Heap.readAsInt64(int(address1, 16)) == Heap.readAsInt64(int(address2, 16)):
                continue
            else:
                Stack.ptr += 1
                continue

        # Compare memory block (not equal)
        elif command == "CMPNOTE":
            parameters = parameter.split(" ")
            address1 = parameters[0]
            address2 = parameters[1]
            DebugUtil.debugLine(f"Comparing memory block at {address1} with {address2}")
            if Heap.readAsInt64(int(address1, 16)) != Heap.readAsInt64(int(address2, 16)):
                continue
            else:
                Stack.ptr += 1
                continue

        # Compare memory block (greater than or equal)
        elif command == "CMPGREQ":
            parameters = parameter.split(" ")
            address1 = parameters[0]
            address2 = parameters[1]
            DebugUtil.debugLine(f"Comparing memory block at {address1} with {address2}")
            if Heap.readAsInt64(int(address1, 16)) >= Heap.readAsInt64(int(address2, 16)):
                continue
            else:
                Stack.ptr += 1
                continue

        # Compare memory block (less than or equal)
        elif command == "CMPLEEQ":
            parameters = parameter.split(" ")
            address1 = parameters[0]
            address2 = parameters[1]
            DebugUtil.debugLine(f"Comparing memory block at {address1} with {address2}")
            if Heap.readAsInt64(int(address1, 16)) <= Heap.readAsInt64(int(address2, 16)):
                continue
            else:
                Stack.ptr += 1
                continue

        # Incrementor
        elif command == "CALCADD":
            parameters = parameter.split(" ")
            address = parameters[0]
            value = Heap.readAsInt64(int(parameters[1], 16))
            DebugUtil.debugLine(f"Incrementing memory block at {address} by {value}")
            Heap.writeAsInt64(int(address, 16), Heap.readAsInt64(int(address, 16)) + value)
            DebugUtil.debugLine(f"New value: {Heap.readAsInt64(int(address, 16))}")

        # Decrementor
        elif command == "CALCSUB":
            parameters = parameter.split(" ")
            address = parameters[0]
            value = Heap.readAsInt64(int(parameters[1], 16))
            DebugUtil.debugLine(f"Decrementing memory block at {address} by {value}")
            Heap.writeAsInt64(int(address, 16), Heap.readAsInt64(int(address, 16)) - value)
            DebugUtil.debugLine(f"New value: {Heap.readAsInt64(int(address, 16))}")

        # Multiplication
        elif command == "CALCMUL":
            parameters = parameter.split(" ")
            address = parameters[0]
            value = Heap.readAsInt64(int(parameters[1], 16))
            DebugUtil.debugLine(f"Multiplying memory block at {address} by {value}")
            Heap.writeAsInt64(int(address, 16), Heap.readAsInt64(int(address, 16)) * value)
            DebugUtil.debugLine(f"New value: {Heap.readAsInt64(int(address, 16))}")

        # Division
        elif command == "CALCDIV":
            parameters = parameter.split(" ")
            address = parameters[0]
            value = Heap.readAsInt64(int(parameters[1], 16))
            DebugUtil.debugLine(f"Dividing memory block at {address} by {value}")
            Heap.writeAsInt64(int(address, 16), Heap.readAsInt64(int(address, 16)) // value)
            DebugUtil.debugLine(f"New value: {Heap.readAsInt64(int(address, 16))}")

        # Modulus
        elif command == "CALCMOD":
            parameters = parameter.split(" ")
            address = parameters[0]
            value = Heap.readAsInt64(int(parameters[1], 16))
            DebugUtil.debugLine(f"Modulus memory block at {address} by {value}")
            Heap.writeAsInt64(int(address, 16), Heap.readAsInt64(int(address, 16)) % value)
            DebugUtil.debugLine(f"New value: {Heap.readAsInt64(int(address, 16))}")

        # Power
        elif command == "CALCPOW":
            parameters = parameter.split(" ")
            address = parameters[0]
            value = Heap.readAsInt64(int(parameters[1], 16))
            DebugUtil.debugLine(f"Power memory block at {address} by {value}")
            Heap.writeAsInt64(int(address, 16), Heap.readAsInt64(int(address, 16)) ** value)
            DebugUtil.debugLine(f"New value: {Heap.readAsInt64(int(address, 16))}")

        # Square root
        elif command == "CALCSQR":
            parameters = parameter.split(" ")
            address = parameters[0]
            DebugUtil.debugLine(f"Square root memory block at {address}")
            Heap.writeAsFloat(int(address, 16), Heap.readAsInt64(int(address, 16)) ** 0.5)
            DebugUtil.debugLine(f"New value: {Heap.readAsFloat(int(address, 16))}")

        # Absolute value
        elif command == "CALCABS":
            parameters = parameter.split(" ")
            address = parameters[0]
            DebugUtil.debugLine(f"Absolute value memory block at {address}")
            Heap.writeAsInt64(int(address, 16), abs(Heap.readAsInt64(int(address, 16))))
            DebugUtil.debugLine(f"New value: {Heap.readAsInt64(int(address, 16))}")

        # Negation
        elif command == "CALCNEG":
            parameters = parameter.split(" ")
            address = parameters[0]
            DebugUtil.debugLine(f"Negation memory block at {address}")
            Heap.writeAsInt64(int(address, 16), -Heap.readAsInt64(int(address, 16)))
            DebugUtil.debugLine(f"New value: {Heap.readAsInt64(int(address, 16))}")

        # Copy
        elif command == "MEMCOPY":
            parameters = parameter.split(" ")
            startAddress = int(parameters[0], 16)
            endAddress = int(parameters[1], 16)
            target = int(parameters[2], 16)
            DebugUtil.debugLine(f"Copying memory block from {startAddress} to {endAddress} -> {target}")
            for i in range(startAddress, endAddress + 1):
                Heap.writeAt(target + (i - startAddress), Heap.readAt(i))

        # Memory dump
        elif command == "MEMDUMP":
            if DebugUtil.isDebugMode():
                parameters = parameter.split(" ")
                startAddress = int(parameters[0], 16)
                endAddress = int(parameters[1], 16)
                DebugUtil.debugLine(f"Memory dump from {startAddress} to {endAddress}")
                for i in range(startAddress, endAddress + 1):
                    DebugUtil.debugLine(f"{i:04x}: {Heap.readAt(i):02x} ({Heap.readAt(i)})")

        elif command == "STRDUMP":
            if DebugUtil.isDebugMode():
                addresses = parameter.split(" ")
                DebugUtil.debugLine(f"Memory dump for string from {addresses[0]} to {addresses[1]}")
                # for i in range(int(addresses[0], 16), int(addresses[1], 16) + 1):
                i = int(addresses[0], 16)
                while True:
                    if i >= int(addresses[1], 16):
                        break
                    DebugUtil.debugLine(f"{i:04x}: {Heap.readAsString(i)}<NullTerminator>")
                    shiftSize = len(Heap.readAsString(i)) + 1
                    i += shiftSize

        elif command == "INTDUMP":
            DebugUtil.debugLine(f"Memory dump for integer at {int(parameter, 16)}: {Heap.readAsInt64(int(parameter, 16))}")

        elif command == "FLTDUMP":
            DebugUtil.debugLine(f"Memory dump for float at {int(parameter, 16)}: {Heap.readAsFloat(int(parameter, 16))}")

        elif command == "BREAKPT":
            if Heap.readAt(int(parameter, 16)) == 1:
                DebugUtil.debugLine("Breakpoint reached")
                input("Press Enter to continue...")

        elif command == "DEBUGPT":
            val: int = Heap.readAt(int(parameter, 16))
            if val == 0:
                DebugUtil.debugLine("Debug point reached - Disabling debug mode")
                DebugUtil.setDebugMode(False)
            elif val == 1:
                DebugUtil.debugLine("Debug point reached - Enabling debug mode")
                DebugUtil.setDebugMode(True)
            else:
                raise Exception(f"Unknown debug point value: {val}")

        # Syscall action
        elif command == "SYSCALL":
            parameters = parameter.split(" ")
            instructionValue = int(parameters[0], 0)
            dataSector = int(parameters[1], 0)
            exitCodeLocation = int(parameters[2], 0)
            exitCode = 0

            if instructionValue == 0:
                # Exit
                DebugUtil.debugLine(f"Syscall exit ({instructionValue:04x}). Exit code at {exitCodeLocation:04x} is {Heap.readAt(exitCodeLocation)}")
                exitCode = Heap.readAt(exitCodeLocation)
                DebugUtil.debugLine(f"Exiting with code {exitCode}")
                Stack.data[0] = exitCode

            elif instructionValue == 1:
                # Print without linebreak
                DebugUtil.debugLine(f"Syscall stdout ({instructionValue:04x}) with data block at {dataSector:04x}. Exit code at {exitCodeLocation:04x} is {Heap.readAt(exitCodeLocation)}")
                print(Heap.readAsString(dataSector), end="")
                exitCode = 0

            elif instructionValue == 2:
                # Print with linebreak
                DebugUtil.debugLine(f"Syscall stdout(int) ({instructionValue:04x}) with data block at {dataSector:04x}. Exit code at {exitCodeLocation:04x} is {Heap.readAt(exitCodeLocation)}")
                print(Heap.readAsInt64(dataSector), end="")
                exitCode = 0

            elif instructionValue == 3:
                # Print with linebreak
                DebugUtil.debugLine(f"Syscall stdout(float) ({instructionValue:04x}) with data block at {dataSector:04x}. Exit code at {exitCodeLocation:04x} is {Heap.readAt(exitCodeLocation)}")
                print(Heap.readAsFloat(dataSector), end="")
                exitCode = 0

            elif instructionValue == 4:
                # Read integer
                DebugUtil.debugLine(f"Syscall stdin(int) ({instructionValue:04x}) with data block at {dataSector:04x}. Exit code at {exitCodeLocation:04x} is {Heap.readAt(exitCodeLocation)}")
                userIn = int(input(""))
                Heap.writeAsInt64(dataSector, userIn)

            elif instructionValue == 5:
                # Read float
                DebugUtil.debugLine(f"Syscall stdin(float) ({instructionValue:04x}) with data block at {dataSector:04x}. Exit code at {exitCodeLocation:04x} is {Heap.readAt(exitCodeLocation)}")
                userIn = float(input(""))
                Heap.writeAsFloat(dataSector, userIn)

            elif instructionValue == 6:
                # Read string
                DebugUtil.debugLine(f"Syscall stdin(str) ({instructionValue:04x}) with data block at {dataSector:04x}. Exit code at {exitCodeLocation:04x} is {Heap.readAt(exitCodeLocation)}")
                userIn = input("")
                Heap.writeAsString(dataSector, userIn)

            else:
                DebugUtil.debugLine(f"Syscall {instructionValue:04x} ({instructionValue:04x}) with data block at {dataSector:04x}. Exit code at {exitCodeLocation:04x} is {Heap.readAt(exitCodeLocation)}")
                raise Exception(f"Unknown syscall {instructionValue}")
                # exitCode = 1

            Heap.writeAt(exitCodeLocation, exitCode)

        else:
            raise Exception(f"Unknown instruction: {command}")
    sys.exit(Stack.data[0])


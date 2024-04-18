class Heap:
    size = 0
    data = [0] * size

    def init(size: int):
        if size <= 0:
            raise Exception("Invalid memory size")
        if Heap.size != 0:
            raise Exception("Memory already initialized")

        Heap.size = size
        Heap.data = [0] * size

    def writeAt(address: int, value: int):
        if address < 0 or address >= Heap.size:
            raise Exception("Invalid memory address")
        if value < 0 or value > 255:
            raise Exception("Invalid memory value")
        Heap.data[address] = value

    def writeAsInt64(address: int, value: int):
        # Signed integer 64 bits (8 bytes)
        if address < 0 or address + 7 >= Heap.size:
            raise Exception("Invalid memory address")
        if value < 0:
            raise Exception("Invalid memory value")

        # Convert int to bytes list
        data = value.to_bytes(8, "big")
        for i in range(8):
            Heap.data[address + i] = data[i]

    def writeAsFloat(address: int, value: float):
        # Signed float 64 bits (8 bytes)
        if address < 0 or address + 7 >= Heap.size:
            raise Exception("Invalid memory address")
        if value < 0:
            raise Exception("Invalid memory value")

        # Convert float to bytes list
        data = bytearray.fromhex(format(value, "a"))
        for i in range(8):
            Heap.data[address + i] = data[i]

    def writeAsString(address: int, value: str):
        if address < 0 or address >= Heap.size:
            raise Exception("Invalid memory address")
        if len(value) >= Heap.size:
            raise Exception("String too long")
        # Convert string to bytes list
        data = value.encode("utf-8")
        for i in range(len(data)):
            Heap.data[address + i] = data[i]

    def readAt(address: int) -> int:
        if address < 0 or address >= Heap.size:
            raise Exception("Invalid memory address")
        return Heap.data[address]

    def readAsInt64(address: int) -> int:
        if address < 0 or address + 7 >= Heap.size:
            raise Exception("Invalid memory address")
        data: list = Heap.data[address:address + 8]
        return int.from_bytes(data, "big")

    def readAsFloat(address: int) -> float:
        if address < 0 or address + 7 >= Heap.size:
            raise Exception("Invalid memory address")
        data: list = Heap.data[address:address + 8]
        return float.fromhex("".join([format(i, "02x") for i in data]))

    def readAsString(address: int) -> str:
        if address < 0 or address >= Heap.size:
            raise Exception("Invalid memory address")
        stringBuilder = ""
        ptr = address
        while Heap.data[ptr] != 0:
            stringBuilder += chr(Heap.data[ptr])
            ptr += 1
        return stringBuilder

    def dump() -> str:
        str = ""
        for i in range(len(Heap.data)):
            str += f"{i:04x}: {Heap.data[i]}\n"
        return str
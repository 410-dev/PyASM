
class Stack:
    size = 0
    ptr = 1
    data = [256]
    dataBytes = 1

    def init(size: int):
        if size <= 0:
            raise Exception("Invalid stack size")
        if Stack.size != 0:
            raise Exception("Stack already initialized")

        Stack.size = size

    def read(index: int):
        if index < 0 or index >= len(Stack.data):
            raise Exception("Invalid stack index")
        return Stack.data[index]

    def write(index: int, value: str):
        if index < 0 or index >= len(Stack.data):
            raise Exception("Invalid stack index")
        Stack.data[index] = value

    def push(value: str):
        Stack.dataBytes += len(value)
        if Stack.dataBytes >= Stack.size:
            raise Exception("Stack overflow: Accessed " + str(Stack.dataBytes + len(Stack.data)) + " bytes of " + str(Stack.size) + " bytes")
        Stack.data.append(value)

    def dump() -> str:
        str = ""
        for i in range(len(Stack.data)):
            str += f"{i:04x}: {Stack.data[i]}\n"
        return str
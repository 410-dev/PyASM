import sys
import traceback


def scriptCompress(lines: list):
    newLines = []
    for line in lines:

        # Skip comments
        if line.strip().startswith("#"):
            continue

        # Skip empty lines
        if line.strip() == "":
            continue

        # Remove after last # sign
        if "#" in line:
            line = line[:line.rfind("#")]

        # Split by last semicolon and keep only the first part
        if ";" in line:
            line = line[:line.rfind(";")]

        newLines.append(line + ";")

    return newLines


def createHeader(script: str):
    lines = script.split("\n")
    # Syntax checking without code modification
    try:
        sections = {}
        for idx, line in enumerate(lines):
            command = line.split(" ")[0].upper()
            if command == "SECTION":
                sectionName = line.split(" ")[1].replace(";", "")
                sectionLoc = idx - 1
                if sectionName in sections.keys():
                    raise Exception(f"Syntax error: Section redefinition at line {idx+1} (compressed): {line}")
                sections[sectionName] = {"address": sectionLoc, "closed": False}
            elif command == "SECTEND":
                sectionName = line.split(" ")[1].replace(";","")
                if sectionName in sections.keys():
                    sections[sectionName]["closed"] = True
                else:
                    raise Exception(f"Syntax error: Section ended without definition at line {idx+1} (compressed): {line}")

        for idx, line in enumerate(lines):
            command = line.split(" ")[0].upper()
            if command == "SECTJMP":
                sectionName = line.split(" ")[1].replace(";", "")
                if sectionName in sections.keys():
                    pass
                else:
                    raise Exception(f"Syntax error: Section jump to undefined section at line {idx+1} (compressed): {line}")

        for sectionName in sections:
            if not sections[sectionName]["closed"]:
                raise Exception(f"Syntax error: Section never closed: {sectionName}")
    except Exception as e:
        print(e)
        # traceback.print_exc()
        sys.exit(0)

    lines = scriptCompress(lines)

    maxHeapMemorySize: int = 0
    for line in lines:
        if line.startswith("DECLARE ") or line.startswith("declare "):
            # Convert hex string to int
            addresses: list = line.replace(";", "").split(" ")
            for address in addresses:
                if address.startswith("0x"):
                    val = int(address[2:], 16)
                    maxHeapMemorySize = max(maxHeapMemorySize, val)

    # Get bytes of compressed script
    numBytesExec = len(script.encode("utf-8"))
    maxHeapMemorySize += 1

    # Insert "EXESIZE 0x0000" format, where 0x0000 is the number of bytes in hex
    compressed = f"ISAVERS 0x0001;\nEXESIZE 0x{numBytesExec:04x};\nVARSIZE 0x{maxHeapMemorySize:04x};\n" + "\n".join(lines)
    lines = compressed.split("\n")

    try:
        sections = {}
        for idx, line in enumerate(lines):
            command = line.split(" ")[0].upper()
            if command == "SECTION":
                sectionName = line.split(" ")[1].replace(";", "")
                sectionLoc = idx - 1
                if sectionName in sections:
                    raise Exception(f"Syntax error: Section redefinition at line {idx+1} (compressed): {line}")
                # for sectionObj in sections:
                #     if not sections[sectionObj]["closed"]:
                #         raise Exception(f"Syntax error: Section-beginning inside another section at line {idx}: {line}")
                lines[idx] = f"SECTION 0x{sectionLoc:04x};"
                sections[sectionName] = {"address": sectionLoc, "closed": False}
            elif command == "SECTEND":
                sectionName = line.split(" ")[1].replace(";", "")
                if sectionName in sections:
                    lines[idx] = f"SECTEND 0x{sections[sectionName]['address']:04x};"
                    sections[sectionName]["closed"] = True
                else:
                    raise Exception(f"Syntax error: Section ended without definition at line {idx+1} (compressed): {line}")

        for idx, line in enumerate(lines):
            command = line.split(" ")[0].upper()
            if command == "SECTJMP":
                sectionName = line.split(" ")[1].replace(";", "")
                if sectionName in sections:
                    lines[idx] = f"SECTJMP 0x{sections[sectionName]['address']:04x};"
                else:
                    raise Exception(f"Syntax error: Section jump to undefined section at line {idx+1} (compressed): {line}")

        for sectionName in sections:
            if not sections[sectionName]["closed"]:
                raise Exception(f"Syntax error: Section never closed: {sectionName}")
    except Exception as e:
        print(e)
        # traceback.print_exc()
        sys.exit(0)

    compressed = "\n".join(lines)
    return compressed

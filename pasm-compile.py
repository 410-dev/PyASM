import sys
defaultSdk="1"

if len(sys.argv) < 2:
    print("Usage: python3 pasm-compile.py <file>")
    sys.exit(1)

# Check if args contain --sdk
if "--sdk" in sys.argv:
    # Get the index of --sdk
    index = sys.argv.index("--sdk")
    # Check if the value of --sdk is not the last argument
    if index + 1 < len(sys.argv):
        # Get the value of --sdk
        defaultSdk = sys.argv[index + 1]

# Get last index of args
lastIndex = len(sys.argv) - 1
script = sys.argv[lastIndex]

sdkPath = f"instructions/sdk{defaultSdk}/"

if not script.endswith(".pasm"):
    print("Invalid file type. Only .pasm files are supported.")
    sys.exit(1)

if defaultSdk == "1":
    import instructions.sdk1.compile as Compiler
    converted: str = Compiler.createHeader(open(script).read())
    with open(f"{".".join(script.split(".")[:-1])}.pasmc", "w") as f:
        f.write(converted)

    print(f"File {script} converted to {".".join(script.split(".")[:-1])}.pasmc")
else:
    print("Invalid SDK version.")
    sys.exit(1)





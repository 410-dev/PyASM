import sys
import traceback
defaultSdk="1"

if len(sys.argv) < 2:
    print("Usage: python3 pasm.py <file> [--sdk <version>]")
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

if not script.endswith(".pasm") and not script.endswith(".pasmc"):
    print("Invalid file type. Only .pasm and .pasmc files are supported.")
    sys.exit(1)

if defaultSdk == "1":
    import instructions.sdk1.ISAKit as SDK
    with open(script, "r") as f:
        try:
            SDK.run(f.read(), True if "--debug" in sys.argv else False)
        except Exception as e:
            # If message starts with "Unknown", don't print the message
            if str(e).startswith("Unknown"):
                print(f"\nPROGRAM TERMINATED WITH INTERNAL ERROR: {e}")
            else:
                print(f"SDK Error: {e}")
                traceback.print_exc()
else:
    print("Invalid SDK version.")
    sys.exit(1)

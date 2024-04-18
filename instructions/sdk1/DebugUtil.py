
class DebugUtil:
    debugMode = False
    lastEndWasNewLine = False
    def debugLine(line: str, end="\n"):
        if DebugUtil.debugMode:
            if DebugUtil.lastEndWasNewLine:
                print(f"[DEBUG] {line}", end=end)
            else:
                print(f"{line}", end=end)
            DebugUtil.lastEndWasNewLine = end == "\n"
            pass


    def setDebugMode(mode: bool):
        DebugUtil.debugMode = mode


    def isDebugMode():
        return DebugUtil.debugMode

from typing import Any, Never
from rich.console import Console
from enum import Enum
import sys

global_console = Console()
global_stderr = Console(file=sys.stderr)

class PanicCode(Enum):
    PCORE_ERROR = (1, "-PCORE_ERROR")
    PrintAlreadyInit = (2, "-PPRINT_ALREADY_INIT")
    InvalidExecContext = (3, "-PINVALID_EXEC_CONTEXT")

    def __init__(self, code: int, label: str):
        self.code = code
        self.label = label

def panic(code: PanicCode, msg: str, *objects: Any) -> Never:
    panic_id = f"(-0x{hex(code.code)}) PANIC {code.label}"
    global_stderr.print(f"[bold red]{panic_id}:  {msg}[/]")
    sys.exit(1 + code.code)

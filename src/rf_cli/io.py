from typing import Any
import threading
from threading import Event
from asyncio import Task
import asyncio as aio
import queue
from .internal import global_console, panic, PanicCode

__io_data: queue.Queue[PrintItem] = queue.Queue()

from dataclasses import dataclass
@dataclass
class PrintItem:
    objects: tuple[Any]
    sep: str
    end: str

def print(*objects: Any, sep: str = ' ', end: str = '\n') -> Task:
    async def __inner_print():
        __io_data.put(PrintItem(objects=objects,sep=sep,end=end))

    return aio.create_task(__inner_print())

def __internal_print_thread() -> None:
    while True:
        pi = __io_data.get()

        try:
            global_console.print(*pi.objects, sep = pi.sep, end = pi.end)
        except BaseException as e:
            panic(PanicCode.PCORE_ERROR, str(e))

_initialised: bool = False

def _internal_init_print_thread():
    global _initialised

    if _initialised:
        panic(PanicCode.PrintAlreadyInit)

    __print_thread = threading.Thread(
        target=__internal_print_thread,
        name="print-thread",
        daemon=True,
    )

    __print_thread.start()

    _initialised = True

__all__ = ('print', '_internal_init_print_thread')

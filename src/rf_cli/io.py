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
    done: threading.Event

def print(*objects: Any, sep: str = ' ', end: str = '\n') -> Task:
    async def __inner_print():
        done = threading.Event()

        __io_data.put(PrintItem(objects=objects,sep=sep,end=end,done=done))

        await aio.to_thread(done.wait)

    return aio.create_task(__inner_print())

def __internal_print_thread() -> None:
    while True:
        pi = __io_data.get()

        try:
            global_console.print(*pi.objects, sep = pi.sep, end = pi.end)
        except BaseException as e:
            panic(PanicCode.PCORE_ERROR, str(e))
        finally:
            pi.done.set()
            __io_data.task_done()

_initialised: bool = False

async def _internal_init_print_thread():
    global _initialised

    if _initialised:
        panic(PanicCode.PrintAlreadyInit)

    __print_thread = threading.Thread(
        target=__internal_print_thread,
        name="rf-cli:print-thread",
        daemon=True,
    )

    __print_thread.start()
    await aio.sleep(0.1)

    _initialised = True

async def _read_line(prompt: str = "") -> str:
    return await aio.to_thread(input, prompt)

class ReadType:
    def __await__(self):
        return _read_line().__await__()

    def __iter__(self):
        while True:
            line = input()

            if not line:
                break

            yield line

    async def __aiter__(self):
        while True:
            line = await _read_line()

            if not line:
                break

            yield line

def read():
    return ReadType()

__all__ = ('print', '_internal_init_print_thread', 'read')

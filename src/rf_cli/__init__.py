import asyncio
from asyncio import iscoroutine, sleep
from .io import _internal_init_print_thread
from typing import Literal, Callable
from .internal import panic, PanicCode, global_console
from .io import print, read
from rich.spinner import Spinner

async def start() -> None:
    with global_console.status("Starting rf-cli:print-thread thread", spinner="line") as status:
        await _internal_init_print_thread()

async def _async_mainfn(name: Literal['__main__'] | str = "__main__", main: Callable | None = None):
    if name != '__main__':
        panic(PanicCode.InvalidExecContext, f"This script is not importable, and is intended to be executed directly.")

    await start()

    if main is not None:
        try:
            p = main()
            if iscoroutine(p):
                await p
        except BaseException as e:
            panic(PanicCode.ProgramError, str(e), e)

        loop = asyncio.get_running_loop()

        current = asyncio.current_task()

        tasks = [
            task
            for task in asyncio.all_tasks(loop)
            if task is not current and not task.done()
        ]

        if tasks:
            await asyncio.gather(*tasks)

def mainfn(name: Literal['__main__'] | str, main: Callable | None = None):
    asyncio.run(_async_mainfn(name, main))

__all__ = ('start', 'mainfn', 'print', 'read')

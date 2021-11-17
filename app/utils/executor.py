import asyncio
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from functools import partial


class Executor:

    def __init__(self, pool, loop=None):
        if loop is None:
            loop = asyncio.get_running_loop()
        self.pool = pool
        self.loop = loop

    async def run(self, function, *args, **kwargs):
        task = partial(function, *args, **kwargs)
        return await self.loop.run_in_executor(self.pool, task)


def init_process_pool():
    process_pool = ProcessPoolExecutor()
    yield process_pool
    process_pool.shutdown(wait=True)


def init_thread_pool():
    thread_pool = ThreadPoolExecutor()
    yield thread_pool
    thread_pool.shutdown(wait=True)

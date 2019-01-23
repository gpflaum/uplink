# Third-party imports
import asyncio

# Local models
from uplink.clients.io import interfaces

__all__ = ["AsyncioStrategy"]


class AsyncioStrategy(interfaces.IOStrategy):
    """A non-blocking execution strategy using asyncio."""

    @asyncio.coroutine
    def invoke(self, func, args, kwargs, callback):
        try:
            response = yield from func(*args, **kwargs)
        except Exception as error:
            # TODO: Include traceback
            response = yield from callback.on_failure(type(error), error, None)
        else:
            response = yield from callback.on_success(response)
        return response

    @asyncio.coroutine
    def sleep(self, duration, callback):
        yield from asyncio.sleep(duration)
        response = yield from callback.on_success()
        return response

    @asyncio.coroutine
    def finish(self, response):
        yield
        return response

    @asyncio.coroutine
    def execute(self, executable):
        response = yield from executable.next()
        return response

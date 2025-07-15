import collections

from asyncio import mixins, exceptions


class Lock(mixins._LoopBoundMixin):
    def __init__(self, *, loop=mixins._marker):
        super().__init__(loop=loop)
        self._waiters = None
        self._locked = False

    def __repr__(self):
        res = super().__repr__()
        extra = 'locked' if self._locked else 'unlocked'
        if self._waiters:
            extra = f'{extra}, waiters:{len(self._waiters)}'
        return f'<{res[1:-1]} [{extra}]>'

    def locked(self):
        return self._locked

    async def acquire(self):
        if (not self._locked and (self._waiters is None or
                all(w.cancelled() for w in self._waiters))):
            self._locked = True
            return True

        if self._waiters is None:
            self._waiters = collections.deque()
        fut = self._get_loop().create_future()
        self._waiters.append(fut)

        try:
            try:
                await fut
            finally:
                self._waiters.remove(fut)
        except exceptions.CancelledError:
            if not self._locked:
                self._wake_up_first()
            raise

        self._locked = True
        return True

    def release(self):
        if self._locked:
            self._locked = False
            self._wake_up_first()
        else:
            raise RuntimeError('Lock is not acquired.')

    def _wake_up_first(self):
        if not self._waiters:
            return
        try:
            fut = next(iter(self._waiters))
        except StopIteration:
            return
        if not fut.done():
            fut.set_result(True)

    async def __aexit__(self, exc_type, exc, tb):
        self.release()

    async def __aenter__(self):
        await self.acquire()
        return None


from greenlet import greenlet

class _GreenletIterator(object):
    """Iterator that switches to a target greenlet to get the next value."""
    _REQUEST_NEXT = object
    def __init__(self, target_greenlet):
        super().__init__()
        self.target_greenlet = target_greenlet

    def __iter__(self):
        return self

    def __next__(self):
        return self.target_greenlet.switch(self._REQUEST_NEXT)


class SendGenerator(object):
    """Wrapper around a generator that takes in a single iterable.

    Allows data to be sent into the generator instead of requiring the
    input iterator to be specified at call time.
    """
    def __init__(self, generator):
        super().__init__()
        self.started = False
        self.main_greenlet = greenlet.getcurrent()
        self.result_iterator = generator(_GreenletIterator(self.main_greenlet))
        self.iterator_greenlet = greenlet(lambda s: s.get_next_result())

    def get_next_result(self):
        while True:
            result = next(self.result_iterator)
            self.main_greenlet.switch(result)

    def send(self, value):
        if not self.started:
            self.started = True
            yield from self.send(self)

        result = self.iterator_greenlet.switch(value)
        while result is not _GreenletIterator._REQUEST_NEXT:
            yield result
            result = self.iterator_greenlet.switch()

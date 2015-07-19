class Bunch(object):
    """A bunch of data.

    Allows access with the . operator
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs);

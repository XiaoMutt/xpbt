class Frozen(type):
    """
    Meta class used to construct immutable class
    """
    def __setattr__(self, key, value):
        raise Exception(f'Cannot set the attribute {key} of a frozen class {self.__class__} to {value}')


class Immutable(object):
    def __init__(self, *args, **kwargs):
        """
        Used to construct immutable objects.
        Attention immutable objects is pickle-able, but cannot be reconstruct back
        :param args:
        :param kwargs:
        """
        for k, v in kwargs.items():
            super(Immutable, self).__setattr__(k, v)

    def __setattr__(self, key, value):
        raise Exception(f'Cannot set the attribute {key} of an immutable {self.__class__} object to {value}.')

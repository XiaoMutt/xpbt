class Frozen(type):
    """
    Meta class used to construct immu
    """

    def __setattr__(self, key, value):
        raise Exception(f'Cannot set the attribute {key} of a frozen class {self.__class__} to {value}')


class Immutable(object):
    def __setattr__(self, key, value):
        # block changing of the attributes
        if key in self.__dict__:
            raise Exception(f'Cannot set the attribute {key} of an immutable {self.__class__} object to {value}.')
        else:
            super(Immutable, self).__setattr__(key, value)


from random import randint
import typing as tp


class ReservoirSampler(object):
    def __init__(self, reservoirSize: int):
        """
        A class performs reservoir sampling.
        Reservoir sampling is a cool little useful algorithm that picks n samples from a source with the probability of
        n/totalSampleProcessed for each picked sample, without knowing the total sample size of the source beforehand
        (n is the reservoirSize).

        :param reservoirSize: the size of the reservoir.
        """
        self.__size = reservoirSize
        self.__list = []
        self.__total = 0

    def add(self, item: tp.Any):
        """
        Add an item to the reservoir. "Add" means sample it, but not add the item for sure in to the reservoir.
        :param item: the item to be sampled
        :return:
        """
        if len(self.__list) < self.__size:
            # reservoir is not full; add item
            self.__list.append(item)
        else:
            # ATTENTION: randint is right boarder inclusive, so __total+=1 is delayed to the end.
            r = randint(0, self.__total)
            if r < self.__size:
                # let n= current total items
                # size/n probability to add the new item
                # probability of old item stay is
                # size/(n-1)[(n-size)/n+(size-1)/size]=size/n
                self.__list[r] = item

        self.__total += 1

    def sample(self, items: tp.Iterable):
        """
        Sample the items by reservoir sampling
        :param items: the items to be sampled
        :return:
        """
        for i in items:
            self.add(i)

    def __iter__(self):
        return self.__list.__iter__()

    def __getitem__(self, item):
        return self.__list.__getitem__(item)

    def __len__(self):
        return len(self.__list)

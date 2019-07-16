from sort.counting_sort import Sorter
from unittest import TestCase, main as umain
from random import sample


INPUT_VALUES = sample(range(100), 10)


class TestSort(TestCase):
    __sorter = Sorter(INPUT_VALUES)

    def test_sort(self, reverse=False) -> bool:
        self.__sorter.counting_sort(reverse)
        self.assertIsNotNone(self.__sorter.val)
        if reverse:
            for i, v in enumerate(self.__sorter.val[1:], start=1):
                self.assertLessEqual(v, self.__sorter.val[i-1])
        else:
            for i, v in enumerate(self.__sorter.val[1:], start=1):
                self.assertGreaterEqual(v, self.__sorter.val[i-1])
        return True


if __name__ == '__main__':
    umain()

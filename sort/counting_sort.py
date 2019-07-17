class Sorter:
    def __init__(self, values: list):
        self.__val = values

    @property
    def val(self):
        return self.__val

    @val.setter
    def val(self, val: list):
        self.__val = val

    def counting_sort(self, reverse=False):
        mx = max(self.__val) + 1
        counts = [0]*mx
        for v in set(self.__val):
            counts[v] += 1
        i = 0
        for num in range(mx):
            for c in range(counts[num]):
                self.__val[i] = num
                i += 1
        if reverse:
            self.__val = self.__val[::-1]


def main():
    from random import sample
    input_values = sample(range(100), 10)
    print('Unsorted: ', input_values)
    sorter = Sorter(input_values)
    sorter.counting_sort()
    print('Sorted: ', sorter.val)


if __name__ == '__main__':
    main()

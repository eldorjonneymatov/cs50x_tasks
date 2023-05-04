class Jar:
    def __init__(self, capacity=12):
        if capacity < 0:
            raise ValueError
        self._capacity = capacity
        self._size = 0

    def __str__(self):
        return '0' * self.size

    def deposit(self, n):
        self._size += n
        if self._size > self.capacity:
            raise ValueError

    def withdraw(self, n):
        if self._size < n:
            raise ValueError
        self._size -= n

    @property
    def capacity(self):
        return self._capacity

    @property
    def size(self):
        return self._size


def main():
    jar = Jar()
    jar.deposit(7)
    print(str(jar))

    jar.withdraw(1)
    print(str(jar))

if __name__ == "__main__":
    main()
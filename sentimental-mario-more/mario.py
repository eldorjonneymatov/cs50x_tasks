# get pyramid`s height
while True:
    try:
        h = int(input("What`s the height of pyramid? "))
        if h >= 1 and h <= 8:
            break
    except ValueError:
        pass

# create pyramid
for i in range(1, h + 1):
    for j in range(1, h + i + 3):
        if (j - h + i - 1) * (j - h) <= 0 or j >= h + 3:
            print('#', end='')
        else:
            print(' ', end='')
    print()
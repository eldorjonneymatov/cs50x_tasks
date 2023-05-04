def checksum(number):
    if number <= 10**12:
        return False

    # variables for calculating the checksum
    temp = sum = 0
    other = False

    # loop through each digit of the number and calculate the checksum
    while number > 0:
        temp = number % 10
        number //= 10

        if other:
            temp *= 2
            sum += temp // 10 + temp % 10
        else:
            sum += temp
        other = not other

    # return true if the checksum is valid (sum divisible by 10)
    return sum % 10 == 0


def get_type(number):
    valid = checksum(number)
    type = "INVALID"

    if valid:
        code = str(number)
        digits = len(code)

        if digits == 15 and code[:2] in ['34', '37']:
            type = "AMEX"
        elif digits == 16 and code[:2] in [str(x) for x in range(51, 56)]:
            type = "MASTERCARD"
        elif (digits in [13, 16]) and code[0] == '4':
            type = "VISA"
    return type


def main():
    # prompt the user for card number
    while True:
        try:
            number = int(input("Number: "))
            break
        except ValueError:
            pass

    # check the checksum and if valid, determine the credit card type
    type = get_type(number)
    print(type)


if __name__ == "__main__":
    main()
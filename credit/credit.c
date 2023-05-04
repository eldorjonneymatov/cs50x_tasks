#include <cs50.h>
#include <stdio.h>

// function to check if the checksum of a credit card number is valid
bool checksum(long number);

// function to determine the type of credit card based on its number
string get_type(long number);

int main(void)
{
    // prompt the user for card number
    long number = get_long("Number: ");

    // check the checksum and if valid, determine the credit card type
    string type = get_type(number);
    printf("%s\n", type);
}

bool checksum(long number)
{
    // check if the number is at leas 13 digits long
    if (number <= 1000000000000)
    {
        return false;
    }

    // variables for calculating the checksum
    int temp = 0, sum = 0;
    bool other = false;

    // loop through each digit of the number and calculate the checksum
    while (number > 0)
    {
        temp = number % 10;
        number /= 10;

        if (other)
        {
            temp *= 2;
            sum += (temp < 10) ? temp : temp / 10 + temp % 10;
        }
        else
        {
            sum += temp;
        }
        other = ! other;
    }

    // return true if the checksum is valid (sum divisible by 10)
    return sum % 10 == 0;
}

string get_type(long number)
{
    bool valid = checksum(number);
    string type = "INVALID";
    if (valid)
    {
        int digits = 0;
        int begin = 0;
        while (number >= 100)
        {
            digits++;
            number /= 10;
        }

        if ((number == 34 || number == 37) && (digits == 13))
        {
            type = "AMEX";
        }
        else if ((number >= 51 && number <= 55) && (digits == 14))
        {
            type = "MASTERCARD";
        }
        else if ((number / 10 == 4) && (digits == 11 || digits == 14))
        {
            type = "VISA";
        }
    }
    return type;
}
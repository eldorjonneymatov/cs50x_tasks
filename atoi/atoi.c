#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int convert(string input);

int main(void)
{
    string input;
    do
    {
        input = get_string("Enter a positive integer: ");
    }
    while (input[0] == '\0');

    for (int i = 0, n = strlen(input); i < n; i++)
    {
        if (!isdigit(input[i]))
        {
            printf("Invalid Input!\n");
            return 1;
        }
    }

    // Convert string to int
    printf("%i\n", convert(input));
}

int convert(string input)
{
    // get the length of the string
    int len = strlen(input);

    // get the last character of the string as an integer
    int last = input[len - 1] - '0';

    // if the string has length 1, return its last character as an integer
    if (len == 1)
    {
        return last;
    }
    // Recursive case: remove the last character from the string,
    // multiply the result of converting the reduced string by 10,
    // then add the last digitelse
    {
        input[len - 1] = '\0';
        return 10 * convert(input) + last;
    }
}
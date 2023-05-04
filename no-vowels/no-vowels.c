#include <cs50.h>
#include <stdio.h>
#include <string.h>

// replace vowels in a given string with numbers
string replace(string str);

int main(int argc, string argv[])
{
    if (argc == 2)
    {
        // pass the user input to replace function and print the resulting string
        printf("%s\n", replace(argv[1]));
    }
    else
    {
        // print error message if user inputs an incorrect number of arguments
        printf("Usage: %s string\n", argv[0]);
        return 1;
}

// implementation of the replace function
string replace(string str)
{
    // loop through every character of string and replace vowels with numbers
    for (int i = 0, n = strlen(str); i < n; i++)
    {
        switch (str[i])
        {
            case 'a':
                str[i] = '6';
                break;
            case 'e':
                str[i] = '3';
                break;
            case 'i':
                str[i] = '1';
                break;
            case 'o':
                str[i] = '0';
                break;
            default:
                break;
        }
    }
    return str;
}
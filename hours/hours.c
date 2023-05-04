#include <cs50.h>
#include <ctype.h>
#include <stdio.h>

float calc_hours(int hours[], int weeks, char output);

int main(void)
{
    // Get the number of weeks taking CS50
    int weeks = get_int("Number of weeks taking CS50: ");
    // Create an array of hours
    int hours[weeks];

    // Get the hours for each week
    for (int i = 0; i < weeks; i++)
    {
        hours[i] = get_int("Week %i HW Hours: ", i);
    }

    // Prompt the user to select output type
    char output;
    do
    {
        output = toupper(get_char("Enter T for total hours, A for average hours per week: "));
    }
    while (output != 'T' && output != 'A');

    printf("%.1f hours\n", calc_hours(hours, weeks, output));
}


float calc_hours(int hours[], int weeks, char output)
{
    int total = 0; // to calculate total hours

    // Calculate the total hours
    for (int i = 0; i < weeks; i++)
    {
        total += hours[i];
    }

    // Return the total or average hours
    return output == 'T' ? total : total / (float) weeks;
}
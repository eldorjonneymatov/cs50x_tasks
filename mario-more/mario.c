#include <cs50.h>
#include <stdio.h>

int get_height(void);
void create_pyramid(int height);

int main(void)
{
    // get pyramid's height
    int height = get_height();

    // create pyramid
    create_pyramid(height);

}

int get_height(void)
{
    // prompt user to enter a number between 1 and 8
    int height;
    do
    {
        height = get_int("What's the height of pyramid? ");
    }
    while (height < 1 || height > 8); // check if the number is correct range
    return height;
}

void create_pyramid(int h)
{
    for (int i = 1; i <= h; i++)
    {
        for (int j = 1; j <= h + i + 2; j++)
        {
            if ((j - h + i - 1) * (j - h) <= 0 || j >= h + 3)
            {
                printf("#");
            }
            else
            {
                printf(" ");
            }
        }
        printf("\n");
    }
}
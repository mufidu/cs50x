#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n > 8 || n < 1);

    for (int i = 1; i <= n; i++)
    {
        for (int j = 0; j < (n - i); j++)
        {
            printf(" ");
        }
        for (int h = 0; h < i; h++)
        {
            printf("#");
        }
        printf("\n");
    }

}
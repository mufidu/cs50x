#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float dollar;
    do
    {
        dollar = get_float("Change owed: ");
    }
    while (dollar <= 0);
    int cents = round(dollar * 100);

    int n = 0;

    if (cents >= 25)
    {
        n += cents / 25;
        cents = cents % 25;
    }

    if (cents < 25 && cents >= 10)
    {
        n += cents / 10;
        cents = cents % 10;
    }

    if (cents < 10 && cents >= 5)
    {
        n += cents / 5;
        cents = cents % 5;
    }

    if (cents < 5 && cents >= 1)
    {
        n += cents / 1;
        cents = cents % 1;
    }

    printf("%i\n", n);
}
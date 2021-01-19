#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float dollars;
    do
    {
        dollars = get_float("Change owed: ");
    }
    while (dollars < 0);
    int cents = round(dollars * 100);
    int coins = 0;
    // figures out the amount of quarters needed first
    while (cents >= 25)
    {
        cents = cents - 25;
        coins++; 
    }
    // figures out the amount of dimes needed second
    while (cents >= 10)
    {
        cents = cents - 10;
        coins++; 
    }
    // figures out the amount of nickels needed
    while (cents >= 5)
    {
        cents = cents - 5;
        coins++; 
    }
    // figures out the amount of pennies needed
    while (cents >= 1)
    {
        cents = cents - 1;
        coins++; 
    }
    printf("%i\n", coins);
}
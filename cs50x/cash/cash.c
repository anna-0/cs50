#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    float dollars; 
    int coins = 0;
    // Prompt for change owed in dollars
    do 
    {
        dollars = get_float("Change owed: ");
    }
    while (dollars < 0.0);

    // Convert to cents
    int cents = round(dollars * 100);

    // Decrease by coin increments if possible and add number of coins used
    while (cents >= 25)
    {
        cents -= 25;
        coins++;
    }
    while (cents >= 10)
    {
        cents -= 10;
        coins++;
    }
    while (cents >= 5)
    {
        cents -= 5;
        coins++;
    }
    while (cents >= 1)
    {
        cents -= 1;
        coins++;
    }

    // Print answer 
    printf("%i\n", coins);
}

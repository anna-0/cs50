#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int h;
    // Prompt for height
    do 
    {
        h = get_int("Height: ");
    }
    while (h < 1 || h > 8);
    
    // Make pyramid
    for (int i = 1; i <= h; i++)
    {
        // Left spaces
        for (int j = i - h; j < 0; j++)
        {
            printf(" ");
        }
        // Left hashes
        for (int k = 1; k < i + 1; k++)
        {
            printf("#");
        }
        // Middle spaces
        printf("  ");
        // Right hashes
        for (int k = 1; k < i + 1; k++)
        {
            printf("#");
        }

        printf("\n");

    }
}

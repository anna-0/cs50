#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    // Prompt for height
    do 
    {
        height = get_int("Height: "); 
    }
    // Reject numbers other than 1-8
    while (height < 1 | height > 8);
   
    // Print pyramid
    for (int row = 0; row < height; row++)
    {
        // Spaces
        for (int spaces = row - height; spaces < -1; spaces++) 
        {
            printf(" ");
        }
        // Hashes
        for (int hashes = 0; hashes < row + 1; hashes++)
        {
            printf("#");
        }
        
        printf("\n");
    }
}

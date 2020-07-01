#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    // Check for command line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    
    // Check all characters are digits
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (isdigit(argv[1][i]) == false)
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    // Check command argument is positive integer
    if (argc == 2 && isdigit(*argv[1]) && argc > 0)
    {
        // Convert command string to integer
        int k = atoi(argv[1]);
        if (k < 0)
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }

        printf("Success\n");

        // Get plaintext to cipher
        string text = get_string("plaintext: ");
        printf("ciphertext: ");

        // Iterate through characters and get ASCII values
        for (int i = 0, n = strlen(text); i < n; i++)
        {
            // Find and convert lowercase letters to/from ASCII/alphabetic index
            if (text[i] >= 'a' && text[i] <= 'z')
            {
                printf("%c", (((text[i] - 'a') + k) % 26) + 'a');
            }
            
            // Find and convert uppercase letters to/from ASCII/alphabetic index
            else if (text[i] >= 'A' && text[i] <= 'Z')
            {
                printf("%c", (((text[i] - 'A') + k) % 26) + 'A');
            }
            
            // Print non-alphabetic characters normally
            else
            {
                printf("%c", text[i]);
            }
        }
        printf("\n");
    }
    
    // Return if not digit
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
}
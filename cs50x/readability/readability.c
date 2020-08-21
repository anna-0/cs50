#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    // Prompts user for text
    string text = get_string("Text: ");

    // Counts letters, words and sentences
    float letters = 0, words = 1, sentences = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
        if (isspace(text[i]))
        {
            words++;
        }
        if (text[i] == '!' || text[i] == '.' || text[i] == '?')
        {
            sentences++;
        }
    }

    // Calculate Coleman-Liau index
    float L = letters / words * 100;
    float S = sentences / words * 100;
    float index = 0.0588 * L - 0.296 * S - 15.8;
    int grade = round(index);

    //Print results
    if (grade > 1 && grade < 16)
    {
        printf("Grade %i\n", grade);
    }
    //Print results if below grade 1 or above grade 16
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    if (grade > 16)
    {
        printf("Grade 16+\n");
    }
}
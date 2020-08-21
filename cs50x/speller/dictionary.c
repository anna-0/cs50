// Implements a dictionary's functionality
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <stdbool.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Hash function prototype
unsigned long hash(char *str);

// Number of buckets in hash table
const unsigned int N = 1000;

// Hash table
node *hashtable[N];

// Initialise word count
int wordcount = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Converts word to lowercase using copy
    int n = strlen(word);
    char copy[n + 1];
    
    // Add null character to copy
    copy[n] = '\0';
    
    for (int i = 0; i < n; i++)
    {
        copy[i] = tolower(word[i]);
    }
    
    // Put lowercase word copy into hashtable to get index
    int index = hash(copy) % N;

    // Return false if no index
    if (hashtable[index] == NULL)
    {
        return false;
    }

    else if (hashtable[index] != NULL)
    {
        // Points cursor to index
        node *cursor = hashtable[index];

        while (cursor != NULL)
        {
            // Check if cursor word is in dictionary
            if (strcasecmp(cursor->word, copy) == 0)
            {
                return true;
            }
            else
            {
                // Else move cursor to next word
                cursor = cursor->next;
            }
        }
    }

    return false;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Open dictionary
    FILE *file = fopen(dictionary, "r");

    // Return false if null file
    if (file == NULL)
    {
        return false;
    }

    // Initialise dictionary word including null character
    char word[LENGTH + 1];

    // Loop until end of file
    while (fscanf(file, "%s", word) != EOF)
    {
        // Allocate memory for node 
        node *n = malloc(sizeof(node));

        // Check node isn't null
        if (n == NULL)
        {
            unload();
            return false;
        }
        
        // Gather index number using hash function for each word
        int index = hash(word);

        // Move to next node
        strcpy(n->word, word);
        n->next = hashtable[index];
        hashtable[index] = n;
        
        // Count
        wordcount++;
    }

    // Close file 
    fclose(file);
    return true;

}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return wordcount;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // Iterate through hashtable with cursor node
    for (int i = 0; i < N; i++)
    {
        node *cursor = hashtable[i];
        
        while (cursor != NULL)
        {
            // Make temporary node while cursor moves to next node
            node *tmp = cursor;
            cursor = cursor->next;
            
            // Free temporary node
            free(tmp);
        }
    }
    
    return true;
}

// Hash function (http://www.cse.yorku.ca/~oz/hash.html)
unsigned long hash(char *str)
{
    unsigned long hash = 5381;
    int c;

    while ((c = *str++))
    {    
        hash = ((hash << 5) + hash) + c;    /* hash * 33 + c */
    }
    
    return hash % N;
}

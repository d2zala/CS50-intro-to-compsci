// Implements a dictionary's functionality

#include <stdbool.h>

#include <stdio.h>

#include <stdlib.h>

#include "dictionary.h"

#include <strings.h>

#include <string.h>

#include <ctype.h>


// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 1000000;

// Hash table
node *table[N];

// counter to keep track of number of words in dictionary
int word_counter = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    int hash_index = hash(word);
    node *tmp = table[hash_index];
    int comparison = 0;
    while (tmp != NULL)
    {
        comparison = strcasecmp(tmp->word, word);
        if (comparison == 0)
        {
            return true;
        }
        else
        {
            tmp = tmp->next;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    // got the following hash function from the website: https://stackoverflow.com/questions/8317508/hash-function-for-a-string
    int seed = 131;
    unsigned int hash_index = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        hash_index = (hash_index * seed) + tolower(word[i]);
    }
    return hash_index % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // TODO
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
        word_counter = 0;
    }
    char word[LENGTH + 1];
    while (fscanf(file, "%s", word) != EOF)
    {
        node *input_word = malloc(sizeof(node));

        if (input_word == NULL)
        {
            return false;
        }
        strcpy(input_word->word, word);

        int index = hash(input_word->word);
        input_word->next = table[index];
        table[index] = input_word;
        word_counter++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return word_counter;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO

    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        node *tmp = cursor;
        while (cursor != NULL)
        {
            cursor = cursor->next;
            free(tmp);
            tmp = cursor;
        }
    }
    return true;
}

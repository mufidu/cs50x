// Implements a dictionary's functionality

#include <stdbool.h>
#include <ctype.h>
#include <string.h>
#include <strings.h>
#include <stdio.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
//Change it to 26 asto fit the alphabets
const unsigned int N = 26;

// Hash table
node *table[N];
int jumlah_kata = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    node *p = table[hash(word)];
    //compare strings case-insensitively
    if (strcasecmp(p->word, word) == 0)
    {
        return true;
    }

    //searching for the word
    while (p->next == NULL)
    {
        p = p->next;
        if (strcasecmp(p->word, word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    int n = (int) tolower(word[0]) - 97;
    return n;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *d = fopen(dictionary, "r");
    char *word = malloc(LENGTH);
    if (word == NULL)
    {
        return false;
    }

    while (fscanf(d, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }

        strcpy(n->word, word);
        jumlah_kata++;

        n->next = table[hash(word)];
        table[hash(word)] = n;
    }

    fclose(d);
    free(word);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return jumlah_kata;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    node *tmp;
    node *tmpp;

    for (int i = 0; i < N; i++)
    {
        if (table[i] == NULL)
        {
            //its okay
            continue;
        }

        tmp = table[i];
        tmpp = tmp;

        while (tmp->next != NULL)
        {
            tmp = tmp->next;
            free(tmpp);
            tmpp = tmp;
        }

        free(tmp);
    }

    return true;
}

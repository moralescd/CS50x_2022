// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// for size function; count as loaded
int dict_count = 0;

// TODO: Choose number of buckets in hash table
// 26 buckets can use start letter to organize
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int start = hash(word);

    node *new = table[start];

    while (new != NULL)
    {
        if (strcasecmp(word, new->word) == 0)
        {
            return true;
        }
        new = new->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        fclose(dict);
        return false;
    }
    char word[LENGTH + 1];
    while ((fscanf(dict, "%s", word)) != EOF)
    {
        // count dictionary words
        dict_count++;
        // allocate memory for node
        node *new = malloc(sizeof(node));
        if (new == NULL)
        {
            return false;
        }
        strcpy(new->word, word);

        // Hash for start letter index
        int start = hash(word);

        new->next = table[start];
        table[start] = new;

    }
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (dict_count != 0)
    {
        return dict_count;
    }
    else
    {
        return 0;
    }
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *tmp = table[i];
        while (tmp != NULL)
        {
            node *move = tmp->next;
            free(tmp);
            tmp = move;
        }
    }
    return true;
}

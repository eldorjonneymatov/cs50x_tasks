// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <math.h>
#include "dictionary.h"
#include <stdio.h>
#include <strings.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 27945;

// Hash table
node *table[N];

bool checkllist(node *node_ptr, const char *word);
void prepare_table(void);
void unload_llist(node *ptr);

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    unsigned int index = hash(word);
    return checkllist(table[index], word);
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int result = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        result += abs('A' - toupper(word[0])) * i;
    }
    return result;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    char c, word[LENGTH + 1];
    unsigned int hashcode;
    int index = 0;

    node *temp;

    prepare_table();

    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        return false;
    }

    while (fread(&c, sizeof(char), 1, dict))
    {
        if (c != '\n')
        {
            // Append character to word
            word[index] = c;
            index++;
        }
        else
        {
            temp = malloc(sizeof(node));
            if (temp == NULL)
            {
                return false;
            }

            for (int i = 0; i < index; i++)
            {
                temp->word[i] = word[i];
            }
            temp->word[index] = '\0';
            temp->next = NULL;

            hashcode = hash(temp->word);

            temp->next = table[hashcode];
            table[hashcode] = temp;

            index = 0;
        }
    }
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    int number = 0;
    node *tmp;

    for (int i = 0; i < N; i++)
    {
        tmp = table[i];
        while (tmp != NULL)
        {
            number++;
            tmp = tmp->next;
        }
    }

    return number;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        unload_llist(table[i]);
    }
    return true;
}

bool checkllist(node *node_ptr, const char *word)
{
    // Traverse the linked list until the end is reached or the word is found.
    while (node_ptr != NULL)
    {
        if (strcasecmp(node_ptr->word, word) == 0)
        {
            return true;
        }
        node_ptr = node_ptr->next;
    }

    return false;
}

void prepare_table(void)
{
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }
}

void unload_llist(node *ptr)
{
    node* temp;
    while (ptr != NULL)
    {
        temp = ptr;
        ptr = ptr->next;
        free(temp);
    }
}
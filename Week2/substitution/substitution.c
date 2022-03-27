#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

bool valid_key(string key);
void cipher(string input, string key);

int main(int argc, string argv[])
{
    //incorrect command line arguments
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else
    {
        string key = argv[1];
        //check key validity
        bool valid = valid_key(key);
        if (valid == 0)
        {
            return 1;
        }
        else
        {
            //use cipher on input text
            string input = get_string("plaintext: ");
            printf("ciphertext: ");
            cipher(input, key);
            return 0;
        }
    }
}

bool valid_key(string key)
{
    //check number of chars in key
    if (strlen(key) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 0;
    }
    else
    {
        int count = 0;
        for (int i = 0; i < strlen(key); i++)
        {
            int c = key[i];
            //check that chars in key are letters
            if (isalpha(c))
            {
                c = toupper(c);
                //add uppercase ascii code to countto check for duplicates
                count += c;
            }
            else
            {
                printf("Key must contain only alphabetic characters\n");
                return 0;
                break;
            }
        }
        //total if all uppercase letters once == 2015
        if (count == 2015)
        {
            return 1;
        }
        else
        {
            printf("Key may not contain repeated characters.\n");
            return 0;
        }
    }
}

void cipher(string input, string key)
{
    for (int i = 0; i < strlen(input); i++)
    {
        //check if char is a letter
        int c = input[i];
        int index = 0;
        if (isalpha(c))
        {
            //preserve capitilization
            if (isupper(c))
            {
                index = c - 65;
                c = toupper(key[index]);
                printf("%c", c);
            }
            else
            {
                index = c - 97;
                c = key[index];
                c = tolower(key[index]);
                printf("%c", c);
            }
        }
        //print non-letters as inputed
        else
        {
            printf("%c", input[i]);
        }
    }
    printf("\n");
}
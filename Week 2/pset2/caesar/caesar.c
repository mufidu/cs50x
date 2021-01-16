#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    //Check if there is a key (second input)
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    //Check if the command line input (the key) is positive int
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        char x = argv[1][i];
        if ((x >= 0 && x <= 47) || (x >= 58 && x <= 127))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    //Start encrypting

    //Input the key to variable
    int key = atoi(argv[1]);
    key = key % 26;
    //Getting plaintext
    string plain = get_string("plaintext: ");
    //Start printing ciphertext
    printf("ciphertext: ");
    for (int i  = 0, n = strlen(plain); i < n; i++)
    {
        char x = plain[i] + key;
        if (x > 90 && x < 97)
        {
            char y = 'A' + (key - (90 - plain[i]) - 1);
            printf("%c", y);
        }
        else if (x > 122)
        {
            char y = 'a' + (key - (122 - plain[i]) - 1);
            printf("%c", y);
        }
        else
        {
            plain[i] += key;
            printf("%c", plain[i]);
        }
    }
    printf("\n");
}
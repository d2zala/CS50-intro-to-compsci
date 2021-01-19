#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

// defines a main function that asks for a string and outputs an integer
int main(int argc, string argv[])
{
    // return 1 causes it to terminate
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    // makes sure the input is a digit number
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (argv[1][i] < 48 || argv[1][i] > 57)
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    int v = atoi(argv[1]);
    string s = get_string("Plaintext: ");
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (isupper(s[i]))
        {
            s[i] = (((s[i] - 65) + v) % 26) + 65;
        }
        else if (islower(s[i]))
        {
            s[i] = (((s[i] - 97) + v) % 26) + 97;
        }
    }
    printf("ciphertext: %s\n", s);
}

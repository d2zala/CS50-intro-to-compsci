#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int main(void)
{
    string s = get_string("Text: ");
    int letters = 0;
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if isupper((s[i]))
        {
            letters += 1;
        }
        if islower((s[i]))
        {
            letters += 1;
        }
    }
    int words = 1;
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if isspace((s[i]))
        {
            words += 1;
        }
    }
    int sentences = 0;
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (s[i] == '.' ||  s[i] == '!' || s[i] == '?')
        {
            sentences += 1;
        }
    }
    float L = (float) letters * 100 / (float) words;
    float S = (float) sentences * 100 / (float) words;
    float index;
    index = (0.0588 * (float) L) - (0.296 * (float) S) - 15.8;
    if (index >= 16)
    {
        printf("Grade 16+");
    }
    else if (index < 1)
    {
        printf("Before Grade 1");
    }
    else
    {
        printf("Grade %.f", round(index));
    }
    printf("\n");
}
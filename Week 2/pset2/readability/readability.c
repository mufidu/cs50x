#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int main(void)
{
    string Text = get_string("Text: ");
    int letters = 0;
    int words = 0;
    int sentences = 0;
    float formula[] = {0.0588, 0.296};

    //Hitung jumlah huruf
    for (int i = 0, n = strlen(Text); i < n; i++)
    {
        if (('a' <= Text[i] && Text[i] <= 'z') || ('A' <= Text[i] && Text[i] <= 'Z'))
        {
            letters++;
        }
    }

    //Hitung jumlah kata
    for (int i = 0, n = strlen(Text); i < n; i++)
    {
        if (Text[i] == 32)
        {
            words++;
        }
    }
    words++;

    //Hitung jumlah kalimat
    for (int i = 0, n = strlen(Text); i < n; i++)
    {
        if (Text[i] == 33 || Text[i] == 46 || Text[i] == 63)
        {
            sentences++;
        }
    }

    //Hitung index Coleman-Liau
    float L = letters * 100 / words;
    float S = sentences * 100 / words;

    int index = round(formula[0] * L - formula[1] * S - 15.8);

    //Print kelas
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }


}
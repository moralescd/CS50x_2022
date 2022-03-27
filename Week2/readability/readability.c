#include <cs50.h>
#include <stdio.h>
#include <string.h>

float count_letters(string text);
float count_words(string text);
float count_sentences(string text);
int cl_index(float letters, float words, float sentences);

int main(void)
{
    //Prompt for text with get_string
    string text = get_string("Text: ");
    float letters = count_letters(text);
    float words = count_words(text);
    float sentences = count_sentences(text);
    int grade = cl_index(letters, words, sentences);
//    printf("Letters: %f\n", letters);
//    printf("Words: %f\n", words);
//    printf("Sentences: %f\n", sentences);
//    printf("Grade %i\n", grade);

    //output == "Grade X"
    //if output > 16, output "Grade 16+"
    //if output < 1, output "Before Grade 1"
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    if (grade >= 1 && grade < 16)
    {
        printf("Grade %i\n", grade);
    }
}

//count the number of letters, words, and sentences
//letter == any lowercase character from a to z or any uppercase character from A to Z
float count_letters(string text)
{
    float letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if ((text[i] >= 'A' && text[i] <= 'Z') || (text[i] >= 'a' && text[i] <= 'z'))
        {
            letters++;
        }
        else
        {
            letters += 0;
        }
    }
    return letters;
}

//any sequence of characters separated by spaces should count as a word
float count_words(string text)
{
    float words = 1;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == 32)
        {
            words++;
        }
        else
        {
            words += 0;
        }
    }
    return words;
}

//any occurrence of a period, exclamation point, or question mark indicates the end of a sentence
//. == 46; ! == 33; ? == 63
float count_sentences(string text)
{
    float sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == 46 || text[i] == 33 || text[i] == 63)
        {
            sentences++;
        }
        else
        {
            sentences += 0;
        }
    }
    return sentences;
}
//index = 0.0588 * L - 0.296 * S - 15.8
//L is the average number of letters per 100 words in the text
//S is the average number of sentences per 100 words in the text.
int cl_index(float letters, float words, float sentences)
{
    float L = letters / words * 100;
    float S = sentences / words * 100;
    float grade = (0.0588 * L) - (0.296 * S) - 15.8;
    if (grade - (int)grade < .5)
    {
        grade = (int)grade;
    }
    else
    {
        grade = (int)grade + 1;
    }
    return grade;
}


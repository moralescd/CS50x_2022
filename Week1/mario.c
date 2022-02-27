#include <cs50.h>
#include <stdio.h>
// input height of pyramid
// reprompt if int not between 1 and 8
// 2 spaces between pyramids
int main(void)
{
    //Input must be between 1 and 8
    int n;
    do
    {
        n = get_int("Height: ");
//        printf("%i\n", n);
    }
    while (n < 1 || n > 8);

    //loop to print n times
    //for each row
    for (int i = 0; i < n; i++)
    {
        // for each column
        for (int k = i + 1; k < n; k++)
        {
            printf(" ");
        }
        for (int j = n - i; j <= n; j++)
        {
            printf("#");
        }
        for (int s = 0; s < 2; s++)
        {
            printf(" ");
        }
        for (int j = n - i; j <= n; j++)
        {
            printf("#");
        }
        // move to next row
        printf("\n");
    }
}
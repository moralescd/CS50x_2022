#include <cs50.h>
#include <stdio.h>

long credit_card(void);
int get_digit(long card, int digit_num, int count);
int count_digits(long card);
bool valid_check(long card, int count);

int main(void)
{
    //get credit card number
    long card = credit_card();

    //get count
    int count = count_digits(card);

    //test valid card
    bool valid = valid_check(card, count);

    if (valid == 0)
    {
        printf("INVALID\n");
    }

    //Find card type
    if (valid == 1)
    {
        //American Express == 15 digits, start with 34 or 37
        if (count == 15)
        {
            if (get_digit(card, 15, count) == 3)
            {
                if (get_digit(card, 14, count) == 4 || get_digit(card, 14, count) == 7)
                {
                    printf("AMEX\n");
                }
                else
                {
                    printf("INVALID\n");
                }
            }
        }
        //MasterCard == 16 digits, start with 51, 52, 53, 54, or 55
        if (count == 16)
        {
            if (get_digit(card, 16, count) == 4)
            {
                printf("VISA\n");
            }
            if (get_digit(card, 16, count) == 5)
            {
                if (get_digit(card, 15, count) == 1 || get_digit(card, 15, count) == 2 || get_digit(card, 15, count) == 3
                || get_digit(card, 15, count) == 4 || get_digit(card, 15, count) == 5)
                {
                    printf("MASTERCARD\n");
                }
                else
                {
                    printf("INVALID\n");
                }
            }
        }
        //Visa == 13 & 16 digits, start with 4
        if (count == 13)
        {
            if (get_digit(card, 13, count) == 4)
            {
                printf("VISA\n");
            }
            else
            {
            printf("INVALID\n");
            }
        }
    }

//get specific digit
//    int digit_num = 3;
//    int digit = get_digit(card, digit_num, count);
//    printf("%i\n", digit);

}

//////////////////////

long credit_card(void)
{
    long number;
    number = get_long("Enter credit card number: ");
    return number;
}

int get_digit(long card, int digit_num, int count)
{
    long place = 1;
    for (int i = 1; i < count; i++)
    {
        if (i == digit_num)
        {
            break;
        }
        place = place * 10;
    }
    int digit = (card / place) % 10;
    return digit;
}

int count_digits(long card)
{
    long place = 1;
    int count;
    for (count = 0; count <= 16; count++)
    {
        if (card / place < 1)
        {
            break;
        }
        place = place * 10;
    }
    return count;
}

//start w 2nd-to-last digit, multiply every other by 2
//add those products DIGITS together
//add the unmulitplied digits together, add to other sum
//if totals last digit is 0, number is valid

bool valid_check(long card, int count)
{
    int sum1 = 0;
    int prod = 0;
    int sum2 = 0;
    int sum3 = 0;

    for (int digit_num = 2; digit_num <= count; digit_num += 2)
    {
        if (card < 1000000000000 || card > 9999999999999999)
        {
            return 0;
        }
        int digit = get_digit(card, digit_num, count);
//        printf("digit num: %i\n", digit_num);
//        printf("digit: %i\n", digit);
        prod = digit * 2;
//        printf("prod: %i\n", prod);
        if (prod < 10)
        {
            sum1 += prod;
        }
        else
        {
            sum1 += ((prod % 10) + ((prod / 10) % 10));
        }
//        printf("sum1: %i\n", sum1);
    }
    for (int digit_num = 1; digit_num <= count; digit_num += 2)
    {
        sum2 += get_digit(card, digit_num, count);
//        printf("sum2: %i\n", sum2);
    }
    sum3 = sum1 + sum2;
//    printf("%i %i %i\n", sum1, sum2, sum3);
    return sum3 % 10 == 0;
}


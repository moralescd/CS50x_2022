# TODO
from cs50 import get_string


def main():
    # Get credit card number
    cc_num = get_string("Enter credit card number: ")

    # Count digits in cc number
    count = 0
    for num in cc_num:
        count += 1

    # Test if valid card
    valid = valid_check(cc_num, count)
    if valid == True:
        card_type(cc_num, count)
    else:
        print("INVALID")


def valid_check(cc_num, count):
    # Card cant be too short or long
    if int(cc_num) < 1000000000000 or int(cc_num) > 9999999999999999:
        return False
    # start w 2nd-to-last digit, multiply every other by 2
    # add those products DIGITS together
    if int(count % 2) == 0:
        digs = int(count / 2)
    else:
        digs = int((count - 1) / 2)

    digit = count - 2
    sum1 = 0
    for i in range(digs):
        prod = int(cc_num[digit]) * 2
        sum1 += int((prod % 10) + ((prod / 10) % 10))
        digit -= 2

    # add the unmulitplied digits together, add to other sum
    if int(count % 2) == 0:
        digs = int(count / 2)
    else:
        digs = int((count + 1) / 2)

    digit = count - 1
    sum2 = 0
    for i in range(digs):
        sum2 += int(cc_num[digit])
        digit -= 2

    sum3 = sum1 + sum2

    # if totals last digit is 0, number is valid
    return sum3 % 10 == 0


def card_type(cc_num, count):
    # American Express == 15 digits, start with 34 or 37
    if count == 15:
        if cc_num[0] == "3":
            if cc_num[1] == "4" or cc_num[1] == "7":
                print("AMEX")
            else:
                print("INVALID")
    # MasterCard == 16 digits, start with 51, 52, 53, 54, or 55
    if count == 16:
        if cc_num[0] == "4":
            print("VISA")
        if cc_num[0] == "5":
            MC_digit2 = ["1", "2", "3", "4", "5"]
            if cc_num[1] in MC_digit2:
                print("MASTERCARD")
            else:
                print("INVALID")
    # Visa == 13 or 16 digits, start with 4
    if count == 13:
        if cc_num == "4":
            print("VISA")
        else:
            print("INVALID")


main()
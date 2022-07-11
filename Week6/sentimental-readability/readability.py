# TODO
from cs50 import get_string


def main():
    # Prompt for text
    text = get_string("Text: ")

    # Get counts
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # Calculate grade level, print results
    grade = cl_index(letters, words, sentences)
    if grade < 1:
        print("Before Grade 1")
    if grade >= 16:
        print("Grade 16+")
    if grade >= 1 and grade < 16:
        print(f"Grade {grade}")


abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
       "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
symbols = [".", "!", "?"]


def count_letters(text):
    # letter == any lowercase character from a to z or any uppercase character from A to Z
    letters = 0
    for char in text:
        if char.upper() in abc:
            letters += 1
    return letters


def count_words(text):
    # any sequence of characters separated by spaces should count as a word
    words = 1
    for char in text:
        if char == " ":
            words += 1
    return words


def count_sentences(text):
    # any occurrence of a period, exclamation point, or question mark indicates the end of a sentence
    # . == 46; ! == 33; ? == 63
    sentences = 0
    for char in text:
        if char in symbols:
            sentences += 1
    return sentences


def cl_index(letters, words, sentences):
    # index = 0.0588 * L - 0.296 * S - 15.8
    # L is the average number of letters per 100 words in the text
    # S is the average number of sentences per 100 words in the text.
    L = letters / words * 100
    S = sentences / words * 100
    grade = round((0.0588 * L) - (0.296 * S) - 15.8)
    return grade


main()
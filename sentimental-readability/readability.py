def calculate_index(text):
    # variables to count number of letters, words and sentences in the text
    letters, words, sentences = 0, 1, 0

    # loop through every character in the text
    for c in text:
        # if the character is letter, increase letters to one
        if c.isalpha():
            letters += 1
        # if the character is a space, it marks the end of a word
        elif c == ' ':
            words += 1
        # if the character is a period, exclamation point, or question mark, it's the end of a sentence
        elif c in ['.', '!', '?']:
            sentences += 1

    # calculate the average number of letters per 100 words
    L = letters / words * 100

    # calculate average number of sentences per 100 words
    S = sentences / words * 100

    # calculate and return the index
    return 0.0588 * L - 0.296 * S - 15.8


# This function calculates the approximate grade level of a text based on its index and prints it
def print_grade(index):
    grade = round(index)

    if grade < 1:
        print("Before Grade 1")
    elif grade >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {grade}")


def main():
    # Get text from user
    text = input("Text: ")

    # Calculate the index of the text
    index = calculate_index(text)

    print_grade(index)


if __name__ == "__main__":
    main()
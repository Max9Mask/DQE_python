"""
This script consists of various functions aimed at text editing and analysis.
These functions perform operations like capitalizing sentences, extracting the last word from each sentence,
adding text to existing strings, replacing mistakes in the text, and counting the number of white spaces in the text.
"""


def capitalize_sentences(text: str, splitting_line_char='\n') -> str:
    # function capitalizes the sentences in a string
    # parameters: text - input string
    #             splitting_char - is a character which will be used for splitting a text

    records = []
    lines = text.split(splitting_line_char)

    for line in lines:
        # split lines by ". " for cases when a line has several sentences
        line_sentences = line.split('. ')
        # capitalize first words
        line_sentences = [sentence.capitalize() for sentence in line_sentences]
        # join sentences into one line like it was before
        line_sentences = '. '.join(line_sentences)
        # append lines in the result list
        records.append(line_sentences)

    # join all lines into a single string with the given splitting character
    fixed_text = splitting_line_char.join(records)

    return fixed_text


def collect_last_words(text: str) -> str:
    # function collects the last word from each sentence in a text
    # parameters: text - input string

    last_words = []
    # split fixed text by lines
    for line in text.splitlines():
        # remove \n, \t, whitespaces from lines and split by "." to catch all sentences
        for word in line.strip().split("."):
            # skip empty sentences
            if word:
                # append last words from sentences in the result list
                last_words.append((word.split()[-1]))

    # remove word 'Homework:' from last words
    if 'Homework:' in last_words:
        last_words.remove('Homework:')

    # create sentence
    last_sentence = " ".join(last_words).capitalize()

    return last_sentence


def add_string(text: str, adding_text: str, separator_char='\n') -> str:
    # function adds a text to the given string
    # parameters: text - text where additional string will be inserted
    #             adding_text - string that will be added to the text
    #             separator_char - separator for adding new string

    updated_text = f"{text}{separator_char}{adding_text}."

    return updated_text


def correct_mistakes(text, mistake: str, replace: str) -> str:
    # function corrects mistakes in the text by replacing a given string (mistake) with another (replace)
    # parameters: text - input string
    #             mistake - mistaken string
    #             replace - correct string

    corrected_text = text.replace(mistake, replace)

    return corrected_text


def count_whitespaces(text: str) -> int:
    # function counts the number of whitespaces in the text
    # parameters: text - input string

    count_spaces = 0
    for char in text:
        if char.isspace():
            count_spaces += 1

    return count_spaces

from string_operations import *


hw_string = """homEwork:
	tHis iz your homeWork, copy these Text to variable. 

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE. 

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""

if __name__ == '__main__':
    # PART 1
    hw_fixed_text = capitalize_sentences(hw_string, '\t')
    last_words = collect_last_words(hw_fixed_text)
    updated_text = add_string(hw_fixed_text, last_words, '\n\t')
    print(f"***** PART 1 *****\n{updated_text}\n")

    # PART 2
    corrected_text = correct_mistakes(updated_text, ' iz ', ' is ')
    corrected_text = correct_mistakes(corrected_text, ' iZ ', ' is ')
    corrected_text = correct_mistakes(corrected_text, ' Iz ', ' is ')
    print(f"***** PART 2 *****\n{corrected_text}\n")

    # PART 3
    number = count_whitespaces(hw_string)
    if number == 87:
        print(f"***** PART 3 *****\nPASSED: number of whitespaces is {number}")
    else:
        print(f"***** PART 3 *****\nFAILED: number of whitespaces is {number}")

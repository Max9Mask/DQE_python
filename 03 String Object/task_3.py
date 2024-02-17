hw_string = """homEwork:
	tHis iz your homeWork, copy these Text to variable. 

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE. 

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""

# PART 1
# split text by character "\t" and capitalize first word
lines = hw_string.split('\t')
lines = [line.capitalize() for line in lines]

# process cases when one line has several sentences
# split line by characters ". " and capitalize first word
records = []

for line in lines:
    # split lines by ". "
    line_sentences = line.split('. ')
    # capitalize first word
    line_sentences = [sentence.capitalize() for sentence in line_sentences]
    # join sentences in one line like it was before
    line_sentences = '. '.join(line_sentences)
    # append lines in the result list
    records.append(line_sentences)

# join sentences in one text like it was before
fixed_text = '\t'.join(records)


# collect last words from the sentences
last_words = []
# split fixed text by lines
for line in fixed_text.splitlines():
    # remove \n, \t, whitespaces from lines and split by "." to catch all sentences
    for word in line.strip().split("."):
        # skip empty sentences
        if word:
            # append last words from sentences in the result list
            last_words.append((word.split()[-1]))

# remove word 'Homework:' from last words
last_words.remove('Homework:')

# create sentence
last_sentence = " ".join(last_words).capitalize()

# add new sentence into the text
updated_text = f"{fixed_text}\n\t{last_sentence}."

print(f"***** PART 1 *****\n{updated_text}\n")

# PART 2
# fix mistakes in the text
fixed_text = (updated_text
              .replace(' iz ', ' is ')
              .replace(' iZ ', ' is ')
              .replace(' Iz ', ' is ')
              )

print(f"***** PART 2 *****\n{fixed_text}\n")

# PART 3
# count the number of whitespaces in the text
count_spaces = 0

for char in hw_string:
    if char.isspace():
        count_spaces += 1

if count_spaces == 87:
    print(f"***** PART 3 *****\nPASSED: number of whitespaces is {count_spaces}")
else:
    print(f"***** PART 3 *****\nFAILED: number of whitespaces is {count_spaces}")

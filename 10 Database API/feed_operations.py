import csv
import os
from string_operations import capitalize_sentences


def count_characters(file_path: str):
    # function to count the number of characters in a text
    # parameters: file_path
    # returns number of characters w/o new line character ("\n")
    # or raises the os.error exception when an inaccessible or invalid file path is specified
    try:
        with open(file_path, 'r') as file:
            # read provided file
            content = file.read()
            # remove all new line characters for calculating letters only (will be used in checks later)
            content = content.replace("\n", "")
        return len(content)
    except OSError:
        print(f"The file '{file_path}' does not exist or could not be opened")


def cut_initial_feed(file_path, idx=None):
    # function cuts provided in file feeds if not all files have to be published
    # parameters: file path
    #             idx - index indicates the desired number of feeds that have to be published
    try:
        with open(file_path, 'r') as file:
            feeds_data = file.read()
            # capitalize feeds from file
            capitalized_feeds = capitalize_sentences(feeds_data)
            # split file feeds to select desired numbers of feeds to be published
            split_feeds = capitalized_feeds.split('\n\n')

            if idx is None:
                copied_feeds = split_feeds
            elif idx > 0:
                # for cases when only first feeds need to be published
                copied_feeds = split_feeds[:idx]
            elif idx < 0:
                # for cases when only last feeds need to be published
                copied_feeds = split_feeds[idx:]
            elif idx == 0:
                print("No feeds selected because of the input number of feeds = 0")
                return None
            else:
                print(f"Invalid number of feeds entered")
                return None

            # join all desired feeds in one text for further processing
            cut_feeds = '\n\n'.join(copied_feeds)

            return cut_feeds
    # errors handling
    except TypeError:
        print('Invalid value for number of feeds, please enter an integer')
    except OSError:
        print(f"The file '{file_path}' does not exist or could not be opened")


def day_days(days_qty):
    # function to return the correct format of day / days
    # days_qty: quantity of days
    # returns a string that says 'x day(s) left' where x is the days_qty
    result = f'{days_qty} day left' if days_qty == 1 else f'{days_qty} days left'
    return result


def word_count(file_path):
    # function to count the occurrence of each word in the file
    # parameters: file path
    with open(file_path, 'r') as file:
        feeds = file.read()
        # removing special characters from the text
        chars = '!@#$%^&*()_=+{}[];|<>?/~,.-:'
        for char in chars:
            feeds = feeds.replace(char, "")

    # split the text into words
    words = feeds.split()
    # initialize empty dictionary to collect word counts
    counts = dict()

    # iterate over each word
    for word in words:
        # check if the word is alphabetic
        if word.isalpha():
            # convert the word to lowercase and incrementing its count in the dictionary
            if word.lower() in counts:
                counts[word.lower()] += 1
            # if the word does not exist in the dictionary, it is added with a count of 1
            else:
                counts[word.lower()] = 1

    # write the dictionary of word counts to a CSV file
    with open('word_counts.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['word', 'count'], delimiter='-')
        writer.writeheader()
        for key, value in counts.items():
            writer.writerow({'word': key, 'count': value})

    return counts


def letter_count(file_path):
    # function to count the occurrence of each letter in the text
    with open(file_path, 'r') as file:
        feeds = file.read()
        # removing special characters from the text
        chars = '!@#$%^&*()_=+{}[];|<>?/~,.-: \n'
        for char in chars:
            feeds = feeds.replace(char, "")

    # initialize empty dictionary to collect word counts
    counts = dict()

    # iterate over each letter in the text
    for char in feeds:
        # check if the word is alphabetic
        if char.isalpha():
            # convert the letter to lowercase
            letter = char.lower()
            # if the letter does not exist in the dictionary, it is added with a count of 1
            # value of the element is a list where list[0] - count of letter, list[1] - count of letter in uppercase
            if letter not in counts:
                counts[letter] = [1, int(char.isupper())]
            # if the letter exists in the dictionary, incrementing its count
            else:
                counts[letter][0] += 1
                counts[letter][1] += int(char.isupper())

    # calculate the percentage of uppercase letters
    for key in counts.keys():
        counts[key].append(round((counts[key][1] / counts[key][0]) * 100, 1))

    # writing the dictionary of letter counts to CSV file
    with open('letter_counts.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['letter', 'count_all', 'count_uppercase', 'percentage'],
                                delimiter='|')
        writer.writeheader()
        for key, value in counts.items():
            # generate row of CSV file
            writer.writerow({'letter': key, 'count_all': value[0], 'count_uppercase': value[1], 'percentage': value[2]})

    return counts


def output_check(file_path: str) -> int:
    # function to count number of characters in a file
    # parameters: file path
    # returns a number of characters
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            data = file.read()
            # removing new line characters
            data_cleaned = data.replace("\n", "")
            count_chars = len(data_cleaned)
        return count_chars
    else:
        count_chars = 0
        return count_chars


def feed_check(record: str) -> int:
    # function to count number of characters in a feed
    # parameters: feed
    # returns a number of characters
    record_cleaned = record.replace("\n", "")
    count_chars = len(record_cleaned)
    return count_chars


def compare_counts(qty_before, qty_after, qty_feed, uploaded_file_path, removed_file):
    # function to compare data by counting the number of characters
    # parameters: qty_before is a number of characters of the file before uploading data
    #             qty_after is a number of characters of the file after uploading data
    #             qty_feed is a number of characters of the uploaded feed
    #             removed_file is a path of the removed feed source file
    if qty_after - qty_before == qty_feed != 0:
        print(f"Feed was successfully uploaded to the '{uploaded_file_path}' file")
        # remove file if it was successfully uploaded
        os.remove(removed_file)
    else:
        print(f"Incorrect uploading, check '{uploaded_file_path}' file")
        print(f"{qty_after} - {qty_before} = {qty_after - qty_before} is not equal to count_feed = {qty_feed}")
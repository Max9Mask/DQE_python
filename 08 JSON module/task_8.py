import csv
from datetime import datetime
import os
from string_operations import capitalize_sentences
import json


# Writer class is used to write text to a file
class Writer:
    # constructor initializes the filename where the text will be written
    def __init__(self, filename='output_feed.txt'):
        self.filename = filename

    def write_to_file(self, record):
        # write_to_file method writes the given record to the file
        # record: the text to write to the file
        with open(self.filename, 'a') as f:
            f.write(f'{record}')


# News class inherits from Writer class and is used to publish news
class News(Writer):
    def __init__(self, source_type=None, news_data=None):
        super().__init__()
        # chose the source of the feed data (file or manual input)
        if source_type == 'json':
            self.text = news_data.get('text')
            self.city = news_data.get('city')
        else:
            self.text = input('Enter text of news: ')
            self.city = input('Enter city: ')

        self.date_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def publish_feed(self):
        feed = ("***** news *****\n"
                f"{self.text}\n"
                f"{self.city}, {self.date_stamp}\n\n"
                )
        self.write_to_file(capitalize_sentences(feed))


def day_days(days_qty):
    # function to return the correct format of day / days
    # days_qty: quantity of days
    # returns a string that says 'x day(s) left' where x is the days_qty
    result = f'{days_qty} day left' if days_qty == 1 else f'{days_qty} days left'

    return result


# Ads class inherits from Writer class and is used to publish ads
class Ads(Writer):
    def __init__(self, source_type=None, ads_data=None):
        super().__init__()
        # chose the source of the feed data (file or manual input)
        if source_type == 'json':
            self.text = ads_data.get('text')
            self.exp_date = ads_data.get('exp_date')
        else:
            self.text = input('Enter text of ad: ')
            # raise a ValueError if the date is not in the correct format or does not exist
            while True:
                self.exp_date = input('Enter expiration date (yyyy-mm-dd): ')
                try:
                    # check if date is in the past
                    if datetime.strptime(self.exp_date, '%Y-%m-%d') < datetime.now():
                        print("The expiration date can't be in the past, please enter future date")
                        continue
                    break
                except ValueError:
                    print("Incorrect date, please enter date in the format 'yyyy-mm-dd'")

    def calc_period(self):
        # calc_period method calculates the remaining days until the expiration date
        # returns the number of days left
        given_date = datetime.strptime(self.exp_date, '%Y-%m-%d')
        current_date = datetime.now()
        diff = given_date - current_date

        return diff.days

    def publish_feed(self):
        # publish_feed method constructs the ad feed and writes it using the superclass write_to_file method
        feed = ("***** ads *****\n"
                f"{self.text}\n"
                f"Actual until: {self.exp_date}, {day_days(self.calc_period())}\n\n"
                )
        # writes feed to the file
        self.write_to_file(capitalize_sentences(feed))


# Forecast class inherits from Writer class and is used to publish weather forecasts
class Forecast(Writer):
    # constructor asks for user input for forecast text and the date of the forecast
    def __init__(self, source_type=None, forecast_data=None):
        super().__init__()
        # chose the source of the feed data (file or manual input)
        if source_type == 'json':
            self.text = forecast_data.get('text')
            self.forecast_date = forecast_data.get('fr_date')
        else:
            self.text = input('Enter text of forecast: ')
            # handle provided date of the forecast
            while True:
                self.forecast_date = input('Enter date (yyyy-mm-dd): ')
                try:
                    # check if date is in the past
                    if datetime.strptime(self.forecast_date, '%Y-%m-%d') < datetime.now():
                        print("The forecast date can't be in the past, please enter future date")
                        continue
                    break
                except ValueError:
                    print("Incorrect date, please enter date in the format 'yyyy-mm-dd'")

    def publish_feed(self):
        # publish_feed method constructs the forecast feed and writes it using the superclass write_to_file method
        feed = ("***** forecast *****\n"
                f"{self.text}\n"
                f"{self.forecast_date}\n\n"
                )
        # writes feed to the file
        self.write_to_file(capitalize_sentences(feed))


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


# CopyFile class copies feeds from provided txt file to the target file
class CopyFile:
    def __init__(self):
        self.content = None
        self.current_dir = os.getcwd()
        self.adding_file_path = input(f"Uploaded file: enter full path or filename for default directory '{self.current_dir}': ")
        self.number_of_feeds = int(input(f"Enter number of feeds for coping to the output file. If you need last feeds, enter negative index, e.g. -1, -2: "))
        self.target_file_path = "output_feed.txt"  # default output file
        # uncomment next line of code if you would like to provide target file manually
        # self.target_file_path = input(f"Enter full target file path or file name for default directory '{self.current_dir}': ")

    def copy_file(self):
        # function to copy a file to a new file
        try:
            # prepare specified number of feed from file
            self.content = cut_initial_feed(self.adding_file_path, self.number_of_feeds)
            # count the number of characters (new line characters are not considered)
            count_new_data = len(self.content.replace("\n", ""))

            # check if uploaded file have any data
            if count_new_data == 0:
                print(f"Copying file {self.adding_file_path} is empty")
                return

            # append data to target file
            with open(self.target_file_path, 'a') as file:
                # count number of characters in the target file before uploading
                count_before_adding = count_characters(self.target_file_path)
                # write data to the target file
                file.writelines(f"{self.content}\n\n")

            # count number of characters in the target file after uploading
            count_after_adding = count_characters(self.target_file_path)

        # raises the os.error exception when an inaccessible or invalid file path is specified
        except OSError:
            print(f"An error occurred while copying the file {self.adding_file_path}")
            return

        # check if all data was uploaded to the target file
        if count_after_adding - count_before_adding == count_new_data:
            print("All data was successfully uploaded")
            # remove source file with uploaded data
            os.remove(self.adding_file_path)
        else:
            print("There are discrepancies after uploading new data.txt")


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
        writer = csv.DictWriter(file, fieldnames=['letter', 'count_all', 'count_uppercase', 'percentage'], delimiter='|')
        writer.writeheader()
        for key, value in counts.items():
            # generate row of CSV file
            writer.writerow({'letter': key, 'count_all': value[0], 'count_uppercase': value[1], 'percentage': value[2]})

    return counts

# function load feed data from the JSON file
def load_from_json(json_file):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File '{json_file}' not found")
        return []
    return data


# Input class is used to process user input
class Input:
    # constructor accepts feed_type which indicates the type of feed to be processed.
    def __init__(self, feed_type):
        self.type = feed_type

    def process_input(self):
        # process_input method constructs the appropriate class object based on feed_type and calls
        # that object's publish_feed method.
        # if the feed_type is not between 1-4, it alerts the user
        if self.type == 1:
            # create News class object
            feed = News()
            # publish News to the file
            feed.publish_feed()
        elif self.type == 2:
            # create Ads class object
            feed = Ads()
            # publish Ads to the file
            feed.publish_feed()
        elif self.type == 3:
            # create Forecast class object
            feed = Forecast()
            # publish Forecast to the file
            feed.publish_feed()
        elif self.type == 4:
            feed = CopyFile()
            feed.copy_file()
        elif self.type == 5:
            json_file = input("Enter the path to json file: ")
            limit = input("Enter number of feeds for coping (for all feeds - press <Enter>"
                          "If you need last feeds, enter negative index, e.g. -1, -2: ")
            data_list = load_from_json(json_file)

            # check if the source file is empty
            if len(data_list) == 0:
                print('The source JSON file is empty')
            else:
                # for cases when pulling all data from the feed)
                if len(limit.strip()) == 0:
                    data_list = data_list[:]
                else:
                    limit = int(limit)
                    # pulling data from the start
                    if limit > 0:
                        data_list = data_list[:limit]
                    # pulling data from the end
                    elif limit < 0:
                        data_list = data_list[limit:]
                    else:
                        data_list = []

                # parse provided JSON data
                for feed_data in data_list:
                    if feed_data.get('feed_type') == 'News':
                        news = News(source_type='json', news_data=feed_data)
                        news.publish_feed()
                    elif feed_data.get('feed_type') == 'Ads':
                        ads = Ads(source_type='json', ads_data=feed_data)
                        ads.publish_feed()
                    elif feed_data.get('feed_type') == 'Forecast':
                        forecast = Forecast(source_type='json', forecast_data=feed_data)
                        forecast.publish_feed()
                    else:
                        print('Incorrect feed type, please check the source JSON file')

        elif self.type == 6:
            pass  # place holder for XML

        elif self.type == 7:
            # Exit message
            print('Application closed')
        else:
            # raise alert if input integer not between 1-6
            print('Please enter a valid integer between 1 and 6')


if __name__ == '__main__':
    # The main function takes the user input for the feed type, and creates an Input object with this type
    # This object's process_input method is then called as long as the feed type is not 5 (to exit)
    # If the user's input is invalid, an error message is printed and the user is prompted again
    while True:
        try:
            start_app = int(input(
                'Enter type of input: \n1) news \n2) ads \n3) forecast \n4) copy from TXT file \n5) copy from JSON file \n6) copy from XML file \n7) Exit\n'))
            if start_app == 7:
                print('Application closed')
                break
            else:
                Input(start_app).process_input()

            word_count('output_feed.txt')
            letter_count('output_feed.txt')
        except ValueError:
            print('Please enter an integer')
            continue

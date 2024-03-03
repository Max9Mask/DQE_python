from datetime import datetime
import os
from string_operations import capitalize_sentences


# Writer class is used to write text to a file
class Writer:
    # constructor initializes the filename where the text will be written
    def __init__(self, filename='output_feed.txt'):
        self.filename = filename

    def write_to_file(self, record):
        # write_to_file method writes the given record to the file
        # record: the text to write to the file
        with open(self.filename, 'a') as f:
            f.write(f'{record}\n')


# News class inherits from Writer class and is used to publish news
class News(Writer):
    # constructor asks for user input for news text and city. It also sets the current time as the date stamp
    def __init__(self):
        super().__init__()
        self.text = input('Enter text of news: ')
        self.city = input('Enter city: ')
        # handle timestamp
        self.date_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def publish_feed(self):
        # publish_feed method constructs the news feed and writes it using the superclass write_to_file method
        feed = ("***** news *****\n"
                f"{self.text}\n"
                f"{self.city}, {self.date_stamp}\n"
                )
        # writes feed to the file
        self.write_to_file(capitalize_sentences(feed))


def day_days(days_qty):
    # function to return the correct format of day / days
    # days_qty: quantity of days
    # returns a string that says 'x day(s) left' where x is the days_qty
    result = f'{days_qty} day left' if days_qty == 1 else f'{days_qty} days left'

    return result


# Ads class inherits from Writer class and is used to publish ads
class Ads(Writer):
    def __init__(self):
        super().__init__()
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
                f"Actual until: {self.exp_date}, {day_days(self.calc_period())}\n"
                )
        # writes feed to the file
        self.write_to_file(capitalize_sentences(feed))


# Forecast class inherits from Writer class and is used to publish weather forecasts
class Forecast(Writer):
    # constructor asks for user input for forecast text and the date of the forecast
    def __init__(self):
        super().__init__()
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
                f"{self.forecast_date}\n"
                )
        # writes feed to the file
        self.write_to_file(capitalize_sentences(feed))


def count_characters(file_path):
    # function to count the number of characters in text
    # parameters: file_path - the file path
    # returns number of characters or raises the os.error exception when an inaccessible or invalid file path is specified
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return len(content)
    except OSError:
        print(f"The file '{file_path}' does not exist or could not be opened")


# CopyFile class copies feeds from provided txt file to the target file
class CopyFile:
    def __init__(self):
        self.content = None
        self.current_dir = os.getcwd()
        self.adding_file_path = input(f"uploaded file: enter full path or filename for default directory '{self.current_dir}': ")
        self.target_file_path = "output_feed.txt"  # default output file
        # uncomment next line of code if you would like to provide target file manually
        # self.target_file_path = input(f"Enter full target file path or file name for default directory '{self.current_dir}': ")

    def copy_file(self):
        # Function to copy a file to a new file
        try:
            # count number of characters in the uploaded file
            count_new_data = count_characters(self.adding_file_path)

            # check if uploaded file have any data.txt
            if count_new_data == 0:
                print(f"Copying file {self.adding_file_path} is empty")
                return

            # read uploaded file
            with open(self.adding_file_path, 'r') as file:
                # Read each line and capitalize sentences using 'string_operations' module
                self.content = [capitalize_sentences(line) for line in file.readlines()]

            # append data.txt to target file
            with open(self.target_file_path, 'a') as file:
                # count number of characters in the target file before uploading
                count_before_adding = count_characters(self.target_file_path)
                # write data.txt to the target file
                file.writelines(self.content)

            # count number of characters in the target file after uploading
            count_after_adding = count_characters(self.target_file_path)
        # raises the os.error exception when an inaccessible or invalid file path is specified
        except OSError:
            print(f"An error occurred while copying the file {self.adding_file_path}")
            return

        # check if all data.txt was uploaded to the target file
        if count_after_adding - count_before_adding == count_new_data:
            print("All data.txt was successfully uploaded")
            # remove source file with uploaded data.txt
            os.remove(self.adding_file_path)
        else:
            print("There are discrepancies after uploading new data.txt")


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
            # Exit message
            print('Application closed')
        else:
            # raise alert if input integer not between 1-5
            print('Please enter a valid integer between 1 and 5')


if __name__ == '__main__':
    # The main function takes the user input for the feed type, and creates an Input object with this type
    # This object's process_input method is then called as long as the feed type is not 5 (to exit)
    # If the user's input is invalid, an error message is printed and the user is prompted again
    while True:
        try:
            start_app = int(input('Enter type of input: 1) news, 2) ads, 3) forecast, 4) copy from file, 5) exit: '))
            if start_app == 5:
                print('Application closed')
                break
            else:
                Input(start_app).process_input()
        except ValueError:
            print('Please enter an integer')

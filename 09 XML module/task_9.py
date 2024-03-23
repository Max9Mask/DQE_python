from datetime import datetime
import json
import xml.etree.ElementTree as ET
from feed_operations import *


output_file = "output_feed.txt"


# Writer class is used to write text to a file
class Writer:
    # constructor initializes the filename where the text will be written
    def __init__(self, filename=output_file):
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
        self.source_type = source_type
        # chose the source of the feed data (file or manual input)
        if self.source_type == 'json':
            self.text = news_data.get('text')
            self.city = news_data.get('city')
        elif self.source_type == 'xml':
            self.text = news_data.find('feed_text').text
            self.city = news_data.find('city').text
        else:
            self.text = input('Enter text of news: ')
            self.city = input('Enter city: ')

        self.date_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def publish_feed(self):
        feed = ("***** news *****\n"
                f"{self.text}\n"
                f"{self.city}, {self.date_stamp}\n\n"
                )
        # write feed to the output file
        self.write_to_file(capitalize_sentences(feed))
        # count characters in the feed
        count_feed = feed_check(feed)
        return count_feed


# Ads class inherits from Writer class and is used to publish ads
class Ads(Writer):
    def __init__(self, source_type=None, ads_data=None):
        super().__init__()
        # chose the source of the feed data (file or manual input)
        if source_type == 'json':
            self.text = ads_data.get('text')
            self.exp_date = ads_data.get('exp_date')
        elif source_type == 'xml':
            self.text = ads_data.find('feed_text').text
            self.exp_date = ads_data.find('exp_date').text
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
        # write feed to the output file
        self.write_to_file(capitalize_sentences(feed))
        # count characters in the feed
        count_feed = feed_check(feed)
        return count_feed


# Forecast class inherits from Writer class and is used to publish weather forecasts
class Forecast(Writer):
    # constructor asks for user input for forecast text and the date of the forecast
    def __init__(self, source_type=None, forecast_data=None):
        super().__init__()
        # chose the source of the feed data (file or manual input)
        if source_type == 'json':
            self.text = forecast_data.get('text')
            self.forecast_date = forecast_data.get('fr_date')
        elif source_type == 'xml':
            self.text = forecast_data.find('feed_text').text
            self.forecast_date = forecast_data.find('fr_date').text
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
        # write feed to the output file
        self.write_to_file(capitalize_sentences(feed))
        # count characters in the feed
        count_feed = feed_check(feed)
        return count_feed


# CopyFile class copies feeds from provided txt file to the target file
class CopyFile:
    def __init__(self):
        self.content = None
        self.current_dir = os.getcwd()
        self.adding_file_path = input(
            f"Uploaded file: enter full path or filename for default directory '{self.current_dir}': ")
        self.number_of_feeds = int(input(
            f"Enter number of feeds for coping to the output file. If you need last feeds, enter negative index, e.g. -1, -2: "))
        self.target_file_path = output_file  # default output file
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


# function load feed data from the JSON file
def load_from_json(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            all_feeds = json.load(file)
    except FileNotFoundError:
        print(f"File '{json_file_path}' not found")
        return []
    return all_feeds


def load_from_xml(xml_file_path):
    try:
        xml_file = ET.parse(xml_file_path)
        root = xml_file.getroot()
        all_feeds = root.findall('feed')
    except FileNotFoundError:
        print(f"File '{xml_file_path}' not found")
        return []
    return all_feeds


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
            json_file = input("Enter the path to JSON file: ")
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

                # count characters before uploading feeds to the output file
                count_before = output_check(output_file)
                # start value to count of feeds
                count_feed = 0

                # parse provided JSON data
                for feed_data in data_list:
                    if feed_data.get('feed_type') == 'News':
                        news = News(source_type='json', news_data=feed_data)
                        count_feed += news.publish_feed()
                    elif feed_data.get('feed_type') == 'Ads':
                        ads = Ads(source_type='json', ads_data=feed_data)
                        count_feed += ads.publish_feed()
                    elif feed_data.get('feed_type') == 'Forecast':
                        forecast = Forecast(source_type='json', forecast_data=feed_data)
                        count_feed += forecast.publish_feed()
                    else:
                        print('Incorrect feed type, please check the source JSON file')

                # count characters before uploading feeds to the output file
                count_after = output_check(output_file)
                # check if all data was written to the output file
                compare_counts(count_before, count_after, count_feed, output_file, json_file)

        elif self.type == 6:
            xml_file = input("Enter the path to XML file: ")
            limit = input("Enter number of feeds for coping (for all feeds - press <Enter>"
                          "If you need last feeds, enter negative index, e.g. -1, -2: ")
            data_xml = load_from_xml(xml_file)

            # check if the source file is empty
            if len(data_xml) == 0:
                print('The source XML file is empty')
            else:
                # for cases when pulling all data from the feed
                if len(limit.strip()) == 0:
                    pass
                else:
                    limit = int(limit)
                    # pulling part data from the start
                    if limit > 0:
                        data_xml = data_xml[:limit]
                    # pulling part data from the end
                    elif limit < 0:
                        data_xml = data_xml[limit:]
                    else:
                        data_xml = []

                # count characters before uploading feeds to the output file
                count_before = output_check(output_file)
                # start value to count of feeds
                count_feed = 0

                # parse provided XML data
                for feed_data in data_xml:
                    feed_type = feed_data.find('feed_type').text
                    if feed_type == 'News':
                        news = News(source_type='xml', news_data=feed_data)
                        count_feed += news.publish_feed()
                    elif feed_type == 'Ads':
                        ads = Ads(source_type='xml', ads_data=feed_data)
                        count_feed += ads.publish_feed()
                    elif feed_type == 'Forecast':
                        forecast = Forecast(source_type='xml', forecast_data=feed_data)
                        count_feed += forecast.publish_feed()
                    else:
                        print('Incorrect feed type, please check the source XML file')

                # count characters before uploading feeds to the output file
                count_after = output_check(output_file)
                # check if all data was written to the output file
                compare_counts(count_before, count_after, count_feed, output_file, xml_file)

        elif self.type == 7:
            # Exit message
            print('Application closed')
        else:
            # raise alert if input integer not between 1-7
            print('Please enter a valid integer between 1 and 7')


if __name__ == '__main__':
    # The main function takes the user input for the feed type, and creates an Input object with this type
    # This object's process_input method is then called as long as the feed type is not 7 (to exit)
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

            word_count(output_file)
            letter_count(output_file)
        except ValueError:
            print('Please enter an integer')
            continue

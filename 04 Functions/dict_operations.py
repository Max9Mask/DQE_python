import random
from typing import List, Dict, Set

'''
This script is designed for creating a list of dictionaries with random keys and values. 
It then collates all dictionary keys and values into a single dictionary 
while eliminating duplicate keys and keeping only the maximum value for each key.
'''


def create_dict() -> Dict:
    # function creates a random dictionary where kes is a random letter (a-z) and value is a random number (0-100)
    # parameters: keys_qty - number of dictionaries that should be created
    # function returns a dictionary with random number of elements

    random_key_quantity = random.randint(0, 10)

    # empty dict where all elements will be collected
    element_dict = {}

    for i in range(random_key_quantity):
        # random letter in lower case a-z
        random_letter = chr(random.randint(ord('a'), ord('z')))
        # random value (0-100)
        random_value = random.randint(0, 100)
        element_dict[random_letter] = random_value

    return element_dict


def create_list_of_dicts(min_qty: int, max_qty: int) -> List[Dict]:
    # function creates a list with random number of dictionaries
    # parameters: min_qty - minimal number of dicts in the list
    #             max_qty - maximal number of dicts in the list
    # for creating dictionaries function create_dict() is used
    # function returns list of dictionaries

    random_number = random.randint(min_qty, max_qty)
    # create a list  using list comprehensions
    list_of_dicts = [create_dict() for i in range(random_number)]

    return list_of_dicts


def collect_keys(dicts_in: List[Dict]) -> Set:
    # function collect all key from all dictionaries from the provided list of dicts
    # function remove all duplicated keys if any
    # parameters: list of dictionaries
    # function returns set of all keys

    collected_keys = set()

    for element in dicts_in:
        for key in element.keys():
            collected_keys.add(key)

    return collected_keys


def combine_dict(dicts_in: List[Dict], keys_set: Set) -> Dict:
    # function creates combined dictionary from all key-values pairs of provided list[dict]
    # parameters: dicts_in is a list of dictionaries
    #             keys_set is a set of keys from dicts_in
    # function returns a dictionary in the following format - key: value1, value2, ...

    # create empty dict where all key will be collected

    common_dict = {key: [] for key in keys_set}

    # loop through all dicts in the dicts_in
    for element in dicts_in:
        # loop through all common keys
        for key in keys_set:
            # if key presents in the dictionary take this value to the common dict
            if key in element:
                common_dict[key].append(element[key])

    return common_dict


def clean_dict(dict_in: Dict, initial_list_of_dicts: List[Dict]) -> Dict:
    # function leaves only max value for each key in the provided dictionary
    # parameters: combined_dict is a dictionary in format key: value1, value2, ...
    #            initial_list_of_dicts is an initial list of dictionaries created by the function create_list_of_dicts()
    # function returns dictionary in format key_{index of dictionary where max value}: max(value)

    result_dict = {}

    # loop through all elements in common dict and take only MAX value to the result
    for key, value in dict_in.items():
        # for cases when a key has more than 1 value
        if len(value) > 1:
            # find MAX value
            max_value = max(value)
            # loop through each dictionary in the list
            for i, d in enumerate(initial_list_of_dicts):
                # if there is key with MAX value in the dict, collect index of this dict
                if d.get(key) == max_value:
                    # add +1 to star counting from 1
                    idx_max_value = i + 1
                    # add MAX values in the result dict with suffix "_index"
                    result_dict[f"{key}_{str(idx_max_value)}"] = max_value
                    break
            # for cases when a key has only 1 value
            else:
                result_dict[key] = value[0]

    return result_dict

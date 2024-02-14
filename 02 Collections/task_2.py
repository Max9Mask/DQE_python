import random


# PART 1
# a function that create a random dict
def create_dict():
    # random quantity of keys in the dict (0-11)
    random_key_quantity = random.randint(0, 11)

    # empty dict where all elements will be collected
    element_dict = {}

    for i in range(random_key_quantity):
        # random letter in lower case a-z
        random_letter = chr(random.randint(ord('a'), ord('z')))
        # random value (0-100)
        random_value = random.randint(0, 101)
        element_dict[random_letter] = random_value

    return element_dict


# random number of dicts in the list (from 2 to 10)
random_number = random.randint(2, 10)

# # create list  using list comprehensions
list_of_dicts = [create_dict() for i in range(random_number)]

# print(list_of_dicts)

# PART 2
# use set to remove duplicates of keys if any
keys = set()
for element in list_of_dicts:
    for key in element.keys():
        keys.add(key)

# create empty dict where all key will be collected
common_dict = {key: [] for key in keys}

# loop through all dicts in the list_of_dicts
for element in list_of_dicts:
    # loop through all common key
    for key in keys:
        # if key presents in the dictionary take this value to the common dict
        if key in element:
            common_dict[key].append(element[key])

# prepare final result dict
result_dict = {}

# loop through all elements in common dict and take only MAX value to the result
for key, value in common_dict.items():
    # for cases when a key has more than 1 value
    if len(value) > 1:
        # find MAX value
        max_value = max(value)
        # loop through each dictionary in the list
        for i, d in enumerate(list_of_dicts):
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

print(result_dict)

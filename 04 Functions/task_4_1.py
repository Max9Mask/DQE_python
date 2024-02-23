from dict_operations import *

if __name__ == '__main__':
    # create list of dicts with number of keys from 2 to 10
    created_list_of_dicts = create_list_of_dicts(2, 10)

    # collect keys from dicts
    keys = collect_keys(created_list_of_dicts)

    # combine all values by common keys
    combined_dictionary = combine_dict(created_list_of_dicts, keys)

    # prepare final result
    cleaned_dict = clean_dict(combined_dictionary, created_list_of_dicts)
    print(cleaned_dict)
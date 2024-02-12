import random


# generate list of 100 random numbers using module "random"
random_list = random.sample(range(0, 1001), 10)

print(f"Generated list: {random_list}")

# sort list using bubble sort algorithm
for i in range(len(random_list)):
    # looping through the list, eliminating the last i elements that are already sorted from the previous iterations
    for j in range(len(random_list) - i - 1):
        # check if the current number is greater than the next number
        if random_list[j] > random_list[j+1]:
            # if it's true then we swap the current number (j) and the next one(j+1)
            random_list[j], random_list[j+1] = random_list[j+1], random_list[j]

print(f"Sorted list: {random_list}")

# calculate average for even and odd numbers
# create new lists for even and odd numbers
even_numbers = []
odd_numbers = []

# looping through elements from random_list and append them in respective list (even or odd)
for elem in random_list:
    # check if a number is divided by 2 then it goes to even list
    if elem % 2 == 0:
        even_numbers.append(elem)
    # if no - moves to odd list
    else:
        odd_numbers.append(elem)

print(f"Even numbers in the list: {even_numbers}")
print(f"Odd numbers in the list: {odd_numbers}")

# calculate average values of even numbers
# check if the list contains any even numbers
if len(even_numbers) > 0:
    # calculate AVG value and round it
    even_agv = round(sum(even_numbers)/len(even_numbers), 3)
    print(f"Average of the even numbers is {even_agv}")
else:
    # print message if there is no any even numbers
    print("List doesn't contain even numbers")

# calculate average values of odd numbers
# check if the list contains any odd numbers
if len(odd_numbers) > 0:
    # calculate AVG value and round it
    odd_agv = round(sum(odd_numbers)/len(odd_numbers), 3)
    print(f"Average of the odd numbers is {odd_agv}")
else:
    # print message if there is no any even numbers
    print("List doesn't contain odd numbers")

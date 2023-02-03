"""
CS 4395.001 Human Language Technologies
Portfolio Assignment 1: Text Processing with Python
Cady Baltz (cmb180010)
2/4/2022
"""

import sys
import re
import pickle


class Person:

    def __init__(self, last, first, mi, id, phone):
        """
            Class representing a Person
            Args:
                last: string with the last name of the person
                first: string with the first name of the person
                mi: string with the middle initial of the person
                id: string with ID of the person (two letters followed by four numbers)
                phone: string with 10-digit phone number of the person
        """
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        """
          Prints the ID, first name, middle initial, last name, and phone number of a person
          Args: None
          Returns: None
          Example:
            >>> person.display()

            >>> Employee id: AA1234
            >>>         First X Last
            >>>         555-555-5555
        """
        id_string = 'Employee id: ' + self.id
        name_string = self.first + ' ' + self.mi + ' ' + self.last
        phone_string = self.phone
        print(id_string)
        print('\t\t' + name_string)
        print('\t\t' + phone_string)
        print()


def process_input_file(filename):
    """
      Parses a data file to create a dictionary of Person objects
      Args:
        filename: Relative path to the user's data file
      Returns:
        A dictionary with the ID as the key, and Person object as the value
      Example:
        >>> process_input_file('data/data.csv')
        >>> {'AA1234': <__main__.Person object at 0x00000179E222FCD0>}
    """

    # try opening the file with the given filename
    try:
        file = open(filename, "r")
    except IOError:
        print('Error: The specified relative file path is not valid')
        return None

    person_dict = {}

    # skip the first line and process each subsequent line of the data file
    for line in file.readlines()[1:]:

        # split on comma to get fields
        fields = line.split(',')

        # modify first and last name to be capital
        last_name = fields[0].capitalize()
        first_name = fields[1].capitalize()

        # modify middle initial to be a single uppercase letter
        middle_init = fields[2].capitalize()

        # use 'X' as a middle initial if one is missing or invalid
        if not (middle_init.isalpha() and len(middle_init) == 1):
            middle_init = 'X'

        # modify ID to be 2 letters followed by 4 digits
        id_pattern = re.compile('^[A-Za-z]{2}[0-9]{4}$')

        id = fields[3].upper()

        # check that the ID is valid and not a duplicate
        while not id_pattern.match(id) or id in person_dict:
            if id in person_dict:
                # print an error message if a duplicate ID is present in the input file
                print('Error: Duplicate ID', id, 'already present in the input data file')
            else:
                # if an ID is not in the correct format, allow the user to re-enter a valid ID
                print('ID invalid:', id)
                print('ID is two letters followed by 4 digits')

            id = input('Please enter a valid id: ').upper()

        # Use regex to modify the phone number so it is in the form 999-999-9999
        phone_number_exp = '^([0-9]{3}).*([0-9]{3}).*([0-9]{4})$'
        phone_number_pattern = re.compile(phone_number_exp)
        phone_number = fields[4].strip()

        # if the phone number does not match the required format, prompt the user for a new one
        while not phone_number_pattern.match(phone_number):
            print('Phone', phone_number, 'is invalid')
            print('Enter phone number in form 123-456-7890')
            phone_number = input('Enter phone number: ')

        # modify phone number to be in the format 999-999-9999
        phone_number = re.sub(phone_number_exp, r'\1-\2-\3', phone_number)

        # create a Person object with the valid data
        current_person = Person(last_name, first_name, middle_init, id, phone_number)

        # save the object to a dict of people, where the ID is the key
        person_dict[id] = current_person

    # return the dict of persons to the main function
    return person_dict


if __name__ == '__main__':
    '''
      Parses an input data file, saves the results to a Pickle file, and then prints out the values from this Pickle file
      Args:
        One system argument with a relative path to the input data
      Returns: None
      Example:
        >>> Employee list:
        >>>
        >>> Employee id: AA1234
        >>>     First X Last
        >>>     555-555-5555
    '''

    # if the user does not specify a sysarg, print an error message and end the program
    if len(sys.argv) < 2:
        print('Error: Please specify a relative path to your input data file as a system arg')
    else:
        output = process_input_file(sys.argv[1])

        if output is not None:
            # save the returned dictionary as a pickle file
            pickle.dump(output, open('person_dict.p', 'wb'))

            # open the pickle file for read
            pickle_dict = pickle.load(open('person_dict.p', 'rb'))

            # print each person using the display() method
            print('\nEmployee list:\n')
            for person in pickle_dict.values():
                person.display()

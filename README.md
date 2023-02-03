# CS_4395_NLP_Portfolio
This is my portfolio for the course CS 4395: Human Language Technologies (Spring 2023)

### Assignment 0: Getting Started
Click [here](https://github.com/cadybaltz/CS_4395_NLP_Portfolio/blob/main/Assignment_0/Overview_of_NLP.pdf) to read my overview of NLP

### Assignment 1: Text Processing with Python
[This program](https://github.com/cadybaltz/CS_4395_NLP_Portfolio/blob/main/Assignment_1/cmb180010-NLP-Assignment-1.py) parses an employee data file to produce more standardized values. It processes an employee's first name, last name, middle initial, phone number, and ID and makes sure each value follows a specified format (e.g., all phone numbers must be in the format 555-555-5555). To handle this text processing, I used standard Python text processing functions as well as regex. Then, this processed data is saved to a dictionary in a Pickle file. This Pickle file is then read to print out the data for each person.

#### To run:
To run this program, you must include one system argument with a relative path to the input data. In this repository, I have uploaded a sample data file within the 'data' subdirectory. 

`python .\cmb180010-NLP-Assignment-1.py .\data\data.csv`

#### Strengths/Weaknesses of Python for Text Processing
##### Strengths
- Python has a large number of built-in function for processing text, such as `split()`, which allowed me to easily split the input data based on commas.
- Python also has many libraries that provide additional functionality for processing text, such as `re`, which allowed me to use regex to process the employee's ID and phone number.

##### Weaknesses
- Python does not do type checking. I had to manually do any checks that were necessary for my data, such as ensuring the middle initial was a letter and not a number.
- Python does not distinguish between characters and strings. This would have been useful for fields like this middle initial.

#### What I learned in this assignment
- In this assignment, I reviewed the basics of Python text processing, including how to open and modify files, use built-in functions like `.capitalize()` and `input()`, and store data in a dictionary.
- Additionally, I learned how to work with additional Python libraries that I had less experience with, including `re` to match and modify text with regex, and `pickle` to store a dictionary in another file.
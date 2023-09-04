# Kansas Tax Calculator

## Project Description

This project was developed while I was searching for my first job in tech. I built it so that I could quickly determine what my actual income would be after taxes in the state of Kansas. There are remarkably few websites out there that make for a simple calculation. I myself don't itemize deductions or anything like that, so I wanted to enter a few simple numbers and get the information I needed fast. I even added the ability to write the info a text file.

### Features

Below are a few things I was proud of within this project.

<img src="./readme images/Program_Screenshot.png" alt="program"/>

#### Data Validation

The program checks to make sure that the information that a user is entering is valid, and re-prompts the user for input if it is invalid.

<img src="./readme images/Data_Validation.png" alt="data_validation"/>

#### Modules

A constants.py file was created and imported to keep track of all the numbers required for tax calculations. This will make it easy to update from year to year. All I have to do is change the numbers in the constants file.

<img src="./readme images/Constants.png" alt="constnts"/>

#### File Read/Write

After the output has been delivered to the console, the option to name a file and write the calculated data to it is presented to the user.

### How to Use

Simply clone the repository to a directory of your choosing.

```bash
git clone https://github.com/DavidMiles1925/kansas_taxes
```

Ensure you have [Python](https://www.python.org/downloads/) installed (tested on v3.11.5).

Run the program:

```bash
python main.py
```

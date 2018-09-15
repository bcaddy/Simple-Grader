"""
================================================================================
 Written by Robert Caddy.  Started on 9/11/2018, last revised 9/11/2018

 used to accelerate the grading process.  Reads in a single csv file from
 courseweb.

 -The user inputs an assignment to be graded and the grading range
 -then the user can search through the students and assign them a grade
 -the program automatically detects duplicates, will warn the user if the grade
   is outside the grade range or if the grade already exists
 -and finally all the unassigned (NaN) grades are set to zero
 -then the user can either grade another assignment or quit and save the csv

 Dependencies:
     pandas

 Changelog:
     Version 1.0 - First Version
================================================================================
"""

import pandas as pd
import numpy as np


# get the path to the file
inputpath = input('What is the path to the file? ')

# read in the grades
grades = pd.read_csv(inputpath)

#outer loop for choosing which assignment to grade
while True:
    # get the assignment name
    assignment = input('Input the name of the assignment to be graded, type {exit} when done\n ')

    # exit if the user is done grading
    if assignment.lower() == '{exit}':
        break

    graderange_min = float(input('input the lower limit for the grade: '))
    graderange_max = float(input('input the upper limit for the grade: '))


    # main loop, searches through names, requests grade, writes grade to the grades
    #  data frame
    while True:
        # get the name of the student
        name = input('Please input the name of the student, type {exit} when done\n')

        # exit if the user is done with this assignment
        if name.lower() == '{exit}':
            break

        # find the entries relating to the student in question
        student = grades[grades['Last Name'].str.contains(name)]



        # if there's multiple students with the same last name then choose just one
        if len(student) > 1:
            # inform the user of the issue
            print('Multiple students found.  Choose which.')
            print(student['First Name'])

            # make sure the user puts the name in correctly
            while True:
                first_name = input('first name: ')

                # find the student
                temp = student[student['First Name'].str.contains(first_name)]

                # check if the student was found correctly
                if len(temp) == 1:
                    student = temp
                    break
                else:
                    print('Incorrect name, try again')

        # check to see if student exists
        if len(student) == 1:

            # Prompt the user for the grade and check if it's within the range
            while True:
                new_grade = float(input(f'Please input the new grade (current grade = {student[assignment].item()}): '))

                # check if the grade is in the right range
                if graderange_min <= new_grade <= graderange_max:
                    # assign the grade to the student
                    grades.at[student.index[0], assignment] = new_grade

                    break
                else:
                    print('Entry out of range, try again')

        else:
            print('Incorrect name, please try again')

        for i in range(len(grades)):
            if np.isnan(grades.at[i, assignment]):
                grades.at[i, assignment] = 0

#####  The loops are finished now #####

# write the value to a new csv file
savepath = input('Please input the save path: ')
grades.to_csv(savepath, index=False)

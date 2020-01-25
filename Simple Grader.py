#!/usr/bin/env python3
"""
    Author: Robert Caddy <r.caddy@pitt.edu>
    Created: 9/11/2018
    Modified: 10/08/201
    Short Description: Accelerate the grading process of assignments fomr Courseweb
    Long Description:8
        This utility is used to accelerate an instructor's grading process. Reads in a single
        csv file from courseweb.

        -The user inputs an assignment to be graded and the grading range
        -then the user can search through the students and assign them a grade
        -the program automatically detects duplicates, will warn the user if the grade
            is outside the grade range or if the grade already exists
        -and finally all the unassigned (NaN) grades are set to zero
        -then the user can either grade another assignment or quit and save the csv
    Dependencies:
        - pandas
        - numpy
"""

import pandas as pd
from numpy import isnan


def main():
    # import the original grades and find the save path
    global grades
    savepath, grades = File_Reader()

    #outer loop for choosing which assignment to grade
    while True:
        # get the assignment details
        assignment, graderange_min, graderange_max = Assignment_Info()

        if assignment == '{exit}':
            break

        # main loop, searches through names, requests grade, writes grade to the grades data frame
        while True:
            # find the student
            student_index = Student_Finder()

            # exit the assignment if the user is done with this assignment
            if student_index == '{exit}':
                break

            # grade the student
            Grader(student_index, assignment, graderange_min, graderange_max)
            
            # save the grades to a .csv file
            grades.to_csv(savepath, index=False)

        ##### end of student loop #####

        # Let the user choose whether or not to give zeroes to all ungraded
        # students for this assignment
        zeroes_choice = str(input('\nDo you want to give all ungraded students zeroes?'
                                  ' (y/n): '))
        if zeroes_choice.lower() == 'y':
            for i in range(len(grades)):
                if isnan(grades.at[i, assignment]):
                    grades.at[i, assignment] = 0



# =============================================================================
#
# =============================================================================

def File_Reader():
    """This function find the path to the original csv file, loads in the grades,
    and gets the path to save the file at"""

    while True:
        # get the path to the file
        inputpath = str(input('\nWhat is the path to the file? ')).rstrip()

        # read in the grades and declare the grades variable to be global so all functions can access it
        try:
            raw_grades = pd.read_csv(inputpath)
            break
        except FileNotFoundError:
            print('\nThe file does not exist.  Please try again')

    while True:
        # get the path to save the file to
        savepath = str(input('\nPlease input the save path (defaults next to '
                            'input file with _new added to filename): ')).rstrip()
        if (len(savepath) == 0):
            savepath =  inputpath[:-4] + '_new' + inputpath[-4:]

        # check to see if the path exists
        try:
            raw_grades.to_csv(savepath,index=False)
            break
        except FileNotFoundError:
            print('\nThe save path does not exist.  Please try again')

    return savepath, raw_grades


# =============================================================================
#
# =============================================================================

def Assignment_Info():
    """Finds and returns the min and max values for the grade of a given assignemnt.
       Also tests for data type conformation"""

    ###### print the list of assignments and prompt the user to choose one to grade #####
    headers = grades.columns.values #find all the column headers

    # this loop prints out the names of each of the assignments
    print('\nList of assignments:')
    for head in headers:
        if '[Total' in head:
            print(head)


    # prompot the user to choose an assignment
    while True:
        try:
            # get the assignment index from user
            assignment_index = str(input('Please input the name of the assigment you wish to grade, type {exit} when done:\n'))

            # exit when the user is done grading
            if assignment_index == '{exit}':
                return assignment_index.lower(), 0, 0

            # get the name of the assignment
            for head in headers:
                if assignment_index.lower() in head.lower():
                    assignment = head
                    break

            # ask the user if they chose the correct assignment
            check = str(input(f'You have chose to grade {assignment}.  Is that correct? (y/n): '))

            # check if it is the correct assignment
            if check.lower() in ('y', 'yes'):
                break
            else:
                del assignment
                continue

        except (ValueError, UnboundLocalError):
            print('\nInvalid input.  Please input an integer corrosponding to an assignment')



    ##### Get the grade ranges #####

    # get the minimum grade and check for non float values of input
    while True:
        try:
            graderange_min = float(input('\ninput the lower limit for the grade: '))
            break
        except ValueError:
            print('Invalid input.  Please input a number')

    # get the maximum grade and check for non float values of input
    while True:
        try:
            graderange_max = float(input('input the upper limit for the grade: '))
            break
        except ValueError:
            print('Invalid input.  Please input a number')

    return assignment, graderange_min, graderange_max

# =============================================================================
#
# =============================================================================

def Student_Finder():
    """Takes a students last name as input and then finds that student.
       This returns the index of the student that was found"""

    # get students name from the user and determine if that student exists
    while True:
        # get the name of the student
        last_name = str(input('\nPlease input the last name of the student, type {exit} when done\n'))

        # return exit condition and exit if the user is done grading students
        if last_name.lower() == '{exit}':
            return last_name

        # find the entries relating to the student in question
        student = Student_Searcher(last_name, grades, 'Last Name')

        if type(student) == str:
            print('\nStudent does not exist')
        else:
            break



    # if there's multiple students with the same last name then choose just one
    if len(student) > 1:
        # inform the user of the issue
        print('\nMultiple students found.  Choose which.\n')
        # print students first names
        for i in student.index:
            print(student['First Name'][i])

        # make sure the user puts the name in correctly
        while True:
            first_name = str(input('first name: '))

            # find the student
            temp = Student_Searcher(first_name, student, 'First Name')

            # check if the student was found correctly
            if type(temp) == str:
                print('Incorrect input, please try again')
            else:
                break

        # reassign the variable student so that it has only one entry
        student = temp

    return student.index[0]

# =============================================================================
#
# =============================================================================

def Student_Searcher(name, dataset, search_type):
    """Search for the student.  Currently this is case sensitive but does allow
    for partial searching"""

    # search for the student, currently this is case sensitive
    student = dataset[dataset[search_type].str.contains(name, case=False)]

    # return error code if the student does not exist
    if len(student) <= 0:
        student = "student does not exist"


    return student

# =============================================================================
#
# =============================================================================

def Grader(student_index, assignment, graderange_min, graderange_max):
    """This function does that actual grading.  It determines a value for the
    grades then sets the grade to that in the grades data frame.  It also checks
    to make sure that the grades are within the bounds specified in the \
    Assignment_Info function"""

    # These variables just exist so that the string the the new_grade input
    # isn't 202 columns long.  I couldn't get multiline f strings to work any
    # other way
    a = f'\nPlease input the new grade for {grades.at[student_index,"First Name"]} '
    b = f'{grades.at[student_index,"Last Name"]} '
    c = f'(current grade = {grades.at[student_index,assignment]}): '

    # Prompt the user for the grade and check if it's within the range
    while True:
        new_grade = str(input(f'{a}{b}{c}'))

        if len(new_grade) > 0:

            try:
                new_grade = float(new_grade)
            except ValueError:
                print('\nNon numerical value input.  Please try again')
                continue


            # check if the grade is in the right range
            if graderange_min <= new_grade <= graderange_max:
                # assign the grade to the student
                grades.at[student_index, assignment] = new_grade

                break
            else:
                print('\nEntry out of range, try again')
                continue
        else:
            print('Student not graded')
            break

# =============================================================================
#
# =============================================================================


# don't execute main if this file is called as a module
if __name__ == '__main__':
    main()
    exit(0)

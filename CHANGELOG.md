# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Version 2.1
### Changes
- Prompts the user to choose which assignment to grade instead of requiring that they input the exact name of the assignment (Resolves issue #10)

- Resolves: #10

## Version 2.0.1
### Changes
Updated the student name prompt to say "last name" instead of just "name"

## Version 2.0
### Changes
Significant increases in robustness, readability, and utility

- Complete refactoring of version 1.0 to enhance readability and maintainability (Resolves issue #1)
- A host of checks added to make sure that user input data is correct and to avoid runtime errors (Resolves issues #5 and #9)
- Added case insensitivity to searches (Resolves issue #2)
- Added intermediate saves between grading each assignment to avoid losing work if the program crashes (Resolves issue #3)
- Shows the name of the student when inputting the grades, general UI clean up (Resolves issues #4 and #7)
- Now sets ungraded students grades to zero after finishing a particular assignment instead of after grading the first student (Resolves issue #6)

- Resolves: #1, #2, #3, #4, #5, #6, #7, #9


## Initial Release (Version 1.0)
### Added
- Open Courseweb / Blackboard Learn CSV file
- Changelog
- Input a grade for each student in an assignment

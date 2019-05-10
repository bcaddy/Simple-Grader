# Simple-Grader
This is a python program to help instructors with large classes input grades for assignments
quickly and easily.  It's designed to work with the University of Pittsburgh's Courseweb/Blackboard
Learn system but should work with Canvas or other similar tools with relatively minor modifications.

## Dependencies:
* Python >= 3.5
* numpy >= 1.15.0
* pandas >= 0.23.3


## How to Use

1. Go to Courseweb/Blackboard Learn, select the class you wish to grade, and under the grades tab click "Work offline"
2. Download the grades as a .csv file
3. Run `Simple Grader.py`
4. Input the path to the .csv file
5. Choose which assignment to grade
6. Input minimum and maximum grades for that assignment
7. Search for students by last name and input their grades, the program will warn you if the input grade is outside of the specified grading range
8. When done type `{exit}` 
9. The program will ask if you want to set all ungraded students grade to 0
10. Either choose antoher assignment to grade or type `{exit}` again 
11. When finished grading input the path the save the new .csv file with all the grades in it and then upload that file to Courseweb/Blackboard Learn


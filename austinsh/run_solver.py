from settings import settings
from scripts.solve import solve

def file_grabber(file_name):
    """ Input the filename of the dataset you wish to be handling. In these
    cases it will a .json file. """
    try:
        # Testing if the file exists with the directory location
        temp = open('testcases/' + file_name + ".json")
        # If file exists, print indicative feedback
        print("\nFile successfully located.")
        # Close the file, it is not needed to be open here
        temp.close
        # Assign the value to casename
        casename = 'testcases/' + file_name + ".json"
        # End the while loop and provide the casename path
        return False, casename
    except:
        # Inform the user the file could not be located
        print("\nFile was not successfully found. Try making sure that the filename",
        "was spelled correctly.")
        # Allows the user to process the information from the above print statement
        input("\nPress ENTER")
        # Continue executing while loop while having no value for casename. Thus, "False"
        return True, False

# Initial condition for the while loop
attempt = True
while attempt:
    # Continue to prompt for the file until it is located
    file = input("\nEnter the name of the file you wish to use.\n")
    # Assign the values to continue or end the while loop while providing a path to case name
    attempt, casename = file_grabber(file)

# Initiate the solver
solve(casename, settings)
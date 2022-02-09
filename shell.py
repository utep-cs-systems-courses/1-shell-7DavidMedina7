import os, sys, re 


# ** Function that changes the current directory **
def change_directory(user_array):
    try:
        # Change the directory
        os.chdir(user_array[1])
    except:
        print(f"{user_array[0]}: no such file or directory: {user_array[1]}")

        
# ** Function to execute programs **
def execute_programs(user_array):
    # Search each directory in PATH
    for dir in re.split(":", os.environ['PATH']):
        # Obtain the program
        program = "%s/%s" % (dir, args[0])
        try:
            # Attemp to execute program
            os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
            pass                              # ...fail quietly lol
    os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
    sys.exit(1)                 # terminate with error

                                            
# ** Function that will list all files in the current directory **
def list_directory(user_array):
    try:
        # | WHAT??? COME BACK TO THIS BC IDK WHY NO WORKY |
        directories = os.listdir(user_array[1])
        print(directories)
    except:
        print("{user_array[0]}: no such file or directory: {user_array[1]}")
    print(directories)
        
# ** Function for redirection **
def redirection(user_array):
    return


# *** INITIAL START OF PROGRAM ***
while True:
    # Checking if PS1 is set in our environment
    if "PS1" not in os.environ:
        # Obtaining the current path
        path = os.getcwd() + " $ "
        os.write(1, path.encode())
    else:
        # Setting PS1 in our environment
        os.environ["PS1"]
    
    # Taking in string and cleaning it
    user_string = input().strip()
    print("\nThis is the current user string: " + user_string)
    
    # Converting the user's stirng into an array
    user_array = user_string.split()
    print("This is the current user array:" + str(user_array))

    # Executing <Exit> command
    if "exit" in user_array:
        print("Program terminated with exit code 0.")
        sys.exit(0)

    # Executing <Change directory> command
    if "cd" == user_array[0]:
        print("This is the cd command.")
        change_directory(user_array)

    # Executing <List files in directory> command
    if "ls" == user_array[0]:
        list_directory(user_array)

import os, sys, re 


# ** Function that changes the current directory **
def change_directory(user_array):
    try:
        # Change the directory
        os.chdir(user_array[1])
    except:
        print(f"{user_array[0]}: no such file or directory: {user_array[1]}")

        
# ** Function to execute program **
def execute_program(user_array):
    # Search each directory in PATH
    for dir in re.split(":", os.environ['PATH']):
        # Obtain the program
        program = "%s/%s" % (dir, user_array[0])
        try:
            # Attemp to execute program
            os.execve(program, user_array, os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
            pass                              # ...fail quietly lol
    os.write(2, ("Child:    Error: Could not exec %s\n" % user_array[0]).encode())
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
        

# Obtaining the P-ID
pid = os.getpid()
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
    elif "cd" == user_array[0]:
        print("This is the cd command.")
        change_directory(user_array)

    # Executing <List files in directory> command
    elif "ls" == user_array[0]:
        list_directory(user_array)

    else:
        # Forking begins~
        os.write(1, ("About to fork (pid:%d)\n" % pid).encode())

        # Obtaining the race condition
        rc = os.fork()

        # Fork failed~
        if rc < 0:
            os.write(2, ("Fork failed, returning %d\n" % rc).encode())
            sys.exit(1)

        # This is the child~
        elif rc == 0:
            os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())

            if "/" in user_array[0]:
                try:
                    os.execve(user_array[0], user_array, os.environ)
                except FileNotFoundError:
                    pass

            elif "<" in user_array or ">" in user_array:
                execute_program(user_array)

        # This is the parent (fork was succesful~
        else:
            os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % (pid, rc)).encode())
            childPidCode = os.wait()
            os.write(1, ("Parent: Child %d terminated with exit code %d\n"
                         % childPidCode).encode())
        
        

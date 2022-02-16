import os, sys, re 


# ** Function that changes the current directory **
def change_directory(path):
    # Signifies that changing directory is possible
    if len(path) > 1:
        try:
            # Change the directory
            os.chdir(path[1])
        except:
            print(f"{path[0]}: no such file or directory: {path[1]}")
    else:
        # Change to main directory
        os.chdir(os.path.expanduser("~"))

        
# ** Function to execute program **
def execute_program(path):
    # Search each directory in PATH
    for dir in re.split(":", os.environ['PATH']):
        # Obtain the program
        program = "%s/%s" % (dir, path[0])
        try:
            # Attemp to execute program
            os.execve(program, path, os.environ)
        except FileNotFoundError:
            # Fail quitely lol
            pass                          
    os.write(2, ("Child:    Error: Could not exec %s\n" % user_input[0]).encode())
    # Terminate with error
    sys.exit(1)        


# ** Function for redirection **
def redirect(path, file_descriptor):
    os.close(file_descriptor)
    os.open(path[2], os.O_CREAT | os.O_WRONLY)
    os.set_inheritable(file_descriptor, True)
    path = path[:1]
    return path
    
    
# ** Function that will list all files in the current directory **
def list_directory(path):
    try:
        # | WHAT??? COME BACK TO THIS BC IDK WHY NO WORKY |
        directories = os.listdir(path[1])
        print(directories)
    except:
        print("{path[0]}: no such file or directory: {path[1]}")
    print(directories)
        

# ** Function that will handle all the pipe work **
def pipe(path):
    print("We in here boys ;)")

    
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
    
    # Obtaining the user's input
    user_input = os.read(0, 1000).decode().split()
    print("This is the current user input: " + str(user_input))

    # Executing <Exit> command
    if "exit" in user_input:
        print("Program terminated with exit code 0.")
        sys.exit(0)

    # Executing <Change directory> command
    elif "cd" == user_input[0]:
        change_directory(user_input)

    # Executing <List files in directory> command
    elif "ls" == user_input[0]:
        list_directory(user_input)

    # Executing <Pipe> command
    elif "|" in user_input:
        print("This is a pipe.")
        pipe(user_input)
    
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

            if ">" in user_input:
                # Redirect with file descriptor 1: stdout
                user_input = redirect(user_input, 1)
                
            elif "<" in user_input:
                # Redirect with file descriptor 0: stdin
                user_input = redirect(user_input, 0)

            # Execute the progam at hand
            execute_program(path)
            
        # This is the parent (fork was succesful)~
        else:
            os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % (pid, rc)).encode())
            childPidCode = os.wait()
            os.write(1, ("Parent: Child %d terminated with exit code %d\n"
                         % childPidCode).encode())
            # Wait for the rest to finish their processes
            child_pid = os.wait()
        
        

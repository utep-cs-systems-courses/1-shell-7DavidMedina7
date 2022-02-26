
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
    os.write(2, ("Child:    Error: Could not exec %s\n" % path[0]).encode())
    # Terminate with error
    sys.exit(1)        


# / Helper function for the pipe() function /
def pipe_helper(pipe_read, pipe_write, program, fd_type):

    # Checks for what to duplicate
    dup_this = pipe_write if fd_type == 1 else pipe_read
    
    os.close(fd_type)
    os.dup(dup_this)
    os.set_inheritable(fd_type, True)

    for file_descriptor in (pipe_read, pipe_write):
        execute_program(program)
    sys.exit(1)


# ** Function that will handle all the pipe work **
def pipe(path):
    print("We in here boys ;)")
    pipe_split_index = path.index("|")
    w = path[0:pipe_split_index]
    r = path[pipe_split_index + 1:]
    print("This is w: " + str(w))
    print("This is r: " + str(r) + "\n")

    pipe_read, pipe_write = os.pipe()

    # Forking begins~
    rc = os.fork()

    # This is the child (write side of pipe)~
    if rc == 0:
        # Let's goooo pipe magic
        pipe_helper(pipe_read, pipe_write, w, 1)

    # This is the child (read side of pipe)~
    elif rc > 0:
        # Let's goooo pipe magic pt.2
        pipe_helper(pipe_read, pipe_write, r, 0)

    # Fork failed~
    else:
        os.write(2, ("Fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

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
                print("We are about to > redirect.")
                os.close(1)
                # Creates file specified on input, otherwise, write on it
                os.open(user_input[2], os.O_CREAT | os.O_WRONLY)
                # Inherit with flag code #1
                os.set_inheritable(1, True)
                user_input = user_input[:1]
            if "<" in user_input:
                # Redirect with file descriptor 0: stdin
                print("We are about to < redirect.")
                os.close(0)
                # Opening the file specified on input only for reading
                os.open(user_input[2], os.O_RDONLY)
                # Inherit with flag code #0
                os.set_inheritable(0, True)
                user_input = user_input[:1]

            # Execute the progam at hand
            execute_program(user_input)
            
        # This is the parent (fork was succesful)~
        else:
            os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % (pid, rc)).encode())
            # Wait for the rest to finish their processes
            childPidCode = os.wait()
            os.write(1, ("Parent: Child %d terminated with exit code %d\n"
                         % childPidCode).encode())

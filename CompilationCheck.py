import sys
import os
from glob import glob
import subprocess
'''
You should have a single directory that contains every student repo folder for the assignment
To run python3 CompilationCheck.py <path>
Where path is a path to that single directory
If no path is supplied, code exits
'''
def main():
    pathToCheckFromCommandLine = sys.argv[1] #get CLI path
    os.chdir(pathToCheckFromCommandLine)
    numNoCompile = 0
    numNoMake = 0
    issue = ""
    if(os.path.exists(pathToCheckFromCommandLine)):
        allFilesInRoot = glob(pathToCheckFromCommandLine + "/*")
        allFilesRoot = [x for x in allFilesInRoot if "failedToCompile" not in x]
        for path in allFilesRoot:
            splitPathList = path.split("/")
            os.chdir(path)
            if(cleanupRepos(path) == 0):
                numNoMake += 1
                issue = " | no makefile"
                repo = splitPathList[-1]
                writeCompilationFailureToFile(issue, repo, pathToCheckFromCommandLine)
            else:
                try:
                    make_process = subprocess.Popen("make", shell=True, stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE, text = True)
                    out, err = make_process.communicate()
                    if "error" in err.lower() and err!= "":

                        issue = " | error at make"
                        repo = splitPathList[-1]
                        writeCompilationFailureToFile(issue, repo, pathToCheckFromCommandLine)
                        numNoCompile += 1
                except:
                    pass
    else:
        print("Path not found. Terminating.")
        exit(1)
    print("makefile not present; no submission likely: " + str(numNoMake))
    print("Did not compile: " + str(numNoCompile))
    print((str(numNoCompile + numNoMake) + " repos did not compile. Repo names and reason for failure in failedToCompile.txt"))

#remove all files ending in .o or named meatMob; return 0 for failure if makefile not present
def cleanupRepos(path):
    files = os.listdir(path)
    if "makefile" not in files and "Makefile" not in files: #makefile not present, no compilation expected
        return 0
    removeFiles = [f for f in files if os.path.isfile(path + '/' + f) and (f[-1] == "o" or f == "meatMob")]

    try:
        for file in removeFiles:
            removalPath = path + "/" + file
            os.remove(removalPath) #clean out the repos .o and meatMob files
    except:
        pass
    return 1

#write repo and issue to file in 0_failedToCompile.txt dir
def writeCompilationFailureToFile(issue, repo, originalPath):
    print(repo + issue)
    f = open(originalPath+ "/0_failedToCompile.txt", "a")
    f.write(repo + issue + "\n")
    f.close()

#confirm num arguments, output error if not correct. Otherwise call main
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print("\nNo path given. Format is python3 CompilationCheck.py path/to/directory/containing/student/repos")
        print("Try again.\n")
        exit(1)
    main()
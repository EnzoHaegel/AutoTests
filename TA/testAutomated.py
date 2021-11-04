import sys
import os
import subprocess
from os import listdir
from os.path import isfile, join


def usage(nb, reason=""):
    if reason != "":
        print("\033[91mError: " + reason + "\033[0m")
    print("USAGE")
    print("\ttestAutomated [name of test] [Executable] [Args]", end="\n\n")
    print("Permet la création de tests automatiques\n")
    print("\ttestAutomated binary")
    print("Permet de run les tests sur le binaire binary")
    exit(nb)


def printFirstChange(text, compare):
    compare = compare.split("\n")
    for i in range(len(text)):
        if text[i].replace("\n", "") != compare[i]:
            print("Line: " + str(i + 1) + '\n' + "Expected:\n" +
                  text[i] + '\n' + "But got:\n" + compare[i])
            return


def runTests(exe):
    passed = 0
    filesList = checkFilesTests()
    for file in filesList:
        content = getFileContent("specs/" + file)
        createTest(["tmp", exe] + content[0].replace('\n', '').split(" "))
        got = getFileContent("specs/tmp.txt")
        os.remove("specs/tmp.txt")
        if got == content:
            passed += 1
            print(file + ": \033[92mPASSED\033[0m")
        else:
            print(file + ": \033[91mFAILED\033[0m")
            printFirstChange(content, got)
    printResults(passed, filesList)


def printResults(passed, filesList):
    if passed*100/len(filesList) == 100:
        print("\nYou got: " + "\033[92m100%\033[0m")
        exit(0)
    print("\nYou got: " + "\033[91m" +
          str(passed*100/len(filesList))+"%" + "\033[0m")
    exit(1)


def getFileContent(file):
    with open(file) as f:
        content = f.readlines()
    if not content:
        usage(1, "Test file is empty")
    return content


def checkFilesTests():
    if not os.path.isdir("specs"):
        usage(1, "There if no tests here :(")
    filesList = [f for f in listdir("specs") if isfile(join("specs", f))]
    if len(filesList) == 0:
        usage(1, "Tests directory is empty :(")
    return filesList


def main():
    if len(sys.argv) == 2:
        runTests(sys.argv[1])
    if len(sys.argv) < 3:
        usage(1, "Bad number of arguments")
    createTest(sys.argv[1:])
    return 0


def createTest(args):
    createFile(args[0])
    text = launchCommand(args[1:])
    f = open("specs/" + args[0] + ".txt", "a")
    f.write(text)
    f.close()


def launchCommand(args):
    arguments = args[1:]
    ret = os.system(' '.join(args)+">> tmp.txt")
    os.system("rm tmp.txt")
    res = ""
    try:
        res = subprocess.check_output(args).decode('utf-8')
    except subprocess.CalledProcessError:
        print(res)
        pass
    return (' '.join(arguments) + '\n' + str(ret) + '\n' + res)


def createFile(filename):
    if not os.path.isdir("specs"):
        os.system("mkdir specs")
    if os.path.isfile("specs/"+filename):
        usage(1, "Name of test already exist")
    os.system("touch specs/" + filename + ".txt")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exited")
        exit(0)
    except IndexError:
        print("IndexError: list index out of range")
        exit(1)

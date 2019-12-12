import sys
import os
import shutil

def fetchTitle(content):
    title = ""
    titleFinished = 0
    index = 0
    while titleFinished == 0:
        currentLine = ""
        while content[index] != "\n":
            currentLine += content[index]
            index += 1
        title += currentLine
        index += 1
        if currentLine == "":
            titleFinished = 1
    return title
        
def fetchAbstract(content):
    index = content.find("Abstract")
    abstractFinished = 0
    abstract = ""
    while abstractFinished == 0:
        currentLine = ""
        while content[index] != "\n":
            currentLine += content[index]
            index += 1
        abstract += currentLine
        index += 1
        if currentLine == "":
            abstractFinished = 1
    return abstract

def convertFolderContentToPlainText(folder):
    shutil.rmtree("./tmp/")
    os.mkdir("./tmp/")
    for filename in os.listdir(folder):
        if filename.endswith('.pdf'):
            input = "'./" + folder + filename + "'"
            output = "'./tmp/" + filename[:-4] + ".txt'"
            command = "pdftotext " + input + " " + output
            os.system(command)

def createOutputs(folder):
    shutil.rmtree("./" + folder + "Paper2Text/")
    os.mkdir("./" + folder + "Paper2Text/")
    for filename in os.listdir("./tmp/"):
        if filename.endswith('.txt'):
            file = open("./tmp/" + filename)
            fileContent = file.read()
            file.close()
            outputContent = ""
            outputContent += filename[:-4] + "\n"
            outputContent += fetchTitle(fileContent) + "\n"
            outputContent += fetchAbstract(fileContent) + "\n"
            outputFile = open("./" + folder + "Paper2Text/" + filename[:-3] + "txt", "w")
            outputFile.write(outputContent)
            outputFile.close()

def main():
    targetFolder = sys.argv[1]
    convertFolderContentToPlainText(targetFolder)
    createOutputs(targetFolder)

main()
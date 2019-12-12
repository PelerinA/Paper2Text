import sys
import os
import re
import shutil
import tempfile

class PaperEnt:
    def __init__(self,filename="",title="",abstract="",auteurs="",biblio=""):
        self.filename=filename
        self.title=title
        self.abstract=abstract
        self.auteurs=auteurs
        self.biblio=biblio

    def toText(self):
        return self.filename+'\n'+self.title+'\n'+self.abstract

    def toXML(self):
        return """<article>\n
            <preamble>"""+self.filename+"""</preamble>\n
            <title>"""+self.title+"""</titre>\n
            <auteur>"""+self.auteurs+"""</auteur>\n
            <abstract>"""+self.abstract+"""</abstract>\n
            <biblio>"""+self.biblio+"""</biblio>\n
            </article>"""

class PersiFichierTexte:
    @staticmethod
    def persiToString(persi):
        with open(persi,'r') as textFile:
            return textFile.read().rstrip()

    @staticmethod
    def stringToPersi(string,filePath):
        with open(filePath,"w") as textFile:
            print(string,file=textFile)

class Parser:
    def __init__(self,content):
        self.content=content
    
    # premiere ligne
    def getTitle(self):
        return self.content.partition('\n')[0]

    # contenu entre abstract et introduction
    def getAbstract(self):
        ss = re.search('(?is)abstract(.*?)introduction',self.content)
        if ss:
            return ss.group(1).replace('\n',' ')
        return ""
    
    # entre le titre et l'abstract
    def getAuteurs(self):
        # ss = re.search('(?is)'+self.getTitle()+'(.*?)abstract',self.content)
        # if ss:
        #     return ss.group(1)
        # return ""
        pass
    
    # derniere page ou après Aknowledgments et References
    def getBiblio(self):
        pass

def main():
    # on suppose que le targetDir est dans le meme repertoire que le script
    targetDir=os.path.dirname(os.path.realpath(__file__))+os.path.sep+sys.argv[1]
    outputDir=targetDir+os.path.sep+"output"

    # creer un sous dossier à ce dossier (le supprimer s'il existe deja)
    if os.path.exists(outputDir) and os.path.isdir(outputDir):
        shutil.rmtree(outputDir)
    os.mkdir(outputDir)

    # convertir les PDF en format txt avec pdftotext dans un dossier tmp
    with tempfile.TemporaryDirectory() as tmpDir:
        for filename in os.listdir(targetDir):
            if filename.endswith('.pdf'):
                f = filename.replace(" ","\ ")
                os.system("pdftotext "+targetDir+os.path.sep+f+" "+tmpDir+os.path.sep+f[:-3]+"txt")

        # # deposer les sorties au format .txt, avec meme nom que pdf respectif
        for filename in os.listdir(tmpDir):
            # parsing vers entite Paper
            paper = PaperEnt()
            parser = Parser(PersiFichierTexte.persiToString(tmpDir+os.path.sep+filename))
            paper.filename=filename[:-4]+".pdf"
            paper.title=parser.getTitle()
            paper.abstract=parser.getAbstract()
            # ecriture de l'entite Paper au format texte dans le dossier output
            # PersiFichierTexte.stringToPersi(paper.toText(),outputDir+os.path.sep+filename)
            PersiFichierTexte.stringToPersi(paper.toXML(),outputDir+os.path.sep+filename[:-3]+"xml")

main()
# paper = PaperEnt()
# filename = "levner.txt"
# filepath = os.path.dirname(os.path.realpath(__file__))+os.path.sep+filename
# parser = Parser(PersiFichierTexte.persiToString(filepath))
# paper.filename = filename
# paper.title = parser.getTitle()
# paper.abstract = parser.getAbstract()
# print(paper.toText())
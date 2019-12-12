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
            <title>"""+self.title+"""</title>\n
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
        # if ss:./tmp/Mikolov_2013_Distributed
        #     return ss.group(1)
        # return ""
        pass

    # derniere page ou après Aknowledgments et References
    def getBiblio(self):
        pass

class Converter:
    def __init__(self):
        # on suppose que le targetDir est dans le meme repertoire que le script
        self.targetDir=os.path.dirname(os.path.realpath(__file__))+os.path.sep+sys.argv[1]
        self.outputDir=self.targetDir+os.path.sep+"output"
        self.tmpDir="./tmp"
        if os.path.exists(self.tmpDir):
            print("Le répertoire /tmp existe déjà")
        else:
            os.mkdir(self.tmpDir, 0o755)

    def createTemporaryFiles(self):
        # convertir les PDF en format txt avec pdftotext dans un dossier tmp
            for filename in os.listdir(self.targetDir):
                if filename.endswith('.pdf'):
                    f = filename.replace(" ","\ ")
                    os.system("pdftotext "+self.targetDir+os.path.sep+f+" "+self.tmpDir+os.path.sep+f[:-3]+"txt")

    def convert(self):
        # # deposer les sorties au format .txt, avec meme nom que pdf respectif
        for filename in os.listdir(self.tmpDir):
            # parsing vers entite Paper
            paper = PaperEnt()
            parser = Parser(PersiFichierTexte.persiToString(self.tmpDir+os.path.sep+filename))
            paper.filename=filename[:-4]+".pdf"
            paper.title=parser.getTitle()
            paper.abstract=parser.getAbstract()
            # ecriture de l'entite Paper au format texte dans le dossier output
            # PersiFichierTexte.stringToPersi(paper.toText(),outputDir+os.path.sep+filename)
            PersiFichierTexte.stringToPersi(paper.toXML(),self.outputDir+os.path.sep+filename[:-3]+"xml")

    def removeTemporaryFolder(self):
        if os.path.exists(self.tmpDir):
                shutil.rmtree(self.tmpDir)
        else:
            print("Le repertoire tmp ne peut être supprimé")



def main():
    converter = Converter()
    converter.createTemporaryFiles()
    converter.convert()
    converter.removeTemporaryFolder()

main()
# paper = PaperEnt()
# filename = "levner.txt"
# filepath = os.path.dirname(os.path.realpath(__file__))+os.path.sep+filename
# parser = Parser(PersiFichierTexte.persiToString(filepath))
# paper.filename = filename
# paper.title = parser.getTitle()
# paper.abstract = parser.getAbstract()
# print(paper.toText())

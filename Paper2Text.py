###################################################################################################
##                                                                                               ##
##                                        Copyright (C) 2020                                     ##
##          Pelerin Aurelien, Frisson Ben, Anfosso Tommy, Monteil Alison, Jacob Alex             ##
##                                                                                               ##
##                                    Licensed under GPLv3                                       ##
##                          https://www.gnu.org/licenses/gpl-3.0.html                            ##
##                                                                                               ##
##          This program is free software: you can redistribute it and/or modify                 ##
##          it under the terms of the GNU General Public License as published by                 ##
##          the Free Software Foundation, either version 3 of the License, or                    ##
##          (at your option) any later version.                                                  ##
##                                                                                               ##
##          This program is distributed in the hope that it will be useful,                      ##
##          but WITHOUT ANY WARRANTY; without even the implied warranty of                       ##
##          MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                        ##
##          GNU General Public License for more details.                                         ##
##                                                                                               ##
##          You should have received a copy of the GNU General Public License                    ##
##          along with this program.  If not, see <https://www.gnu.org/licenses/>.               ##
##                                                                                               ##
##                                                                                               ##
###################################################################################################


import sys
import os
import re
import shutil
import tempfile

class PaperEnt:
    def __init__(self,filename="",title="",abstract="",auteurs="",discussion="",biblio="", intro="", corps="", acknow="", conclusion=""):
        self.filename=filename
        self.title=title
        self.abstract=abstract
        self.intro=intro
        self.auteurs=auteurs
        self.discussion=discussion
        self.conclusion=conclusion
        self.acknow=acknow
        self.biblio=biblio
        self.corps=corps

    def toText(self):
        return self.filename+'\n'+self.title+'\n'+self.auteurs+self.abstract+'\n'+self.intro+'\n'+self.corps+'\n'+self.discussion+'\n'+self.conclusion+'\n'+self.acknow+'\n'+self.biblio


    def toXML(self):
        return """<article>\n
            <preamble>"""+self.filename+"""</preamble>\n
            <titre>"""+self.title+"""</titre>\n
            <auteur>"""+self.auteurs.rsplit(' ', 1)[0]+"""</auteur>\n
            <abstract>"""+self.abstract.rsplit(' ', 3)[0]+"""</abstract>\n
            <introduction>"""+self.intro.rsplit(' ', 1)[0]+"""</introduction>\n
            <corps>"""+self.corps.rsplit(' ', 1)[0]+"""</corps>\n
            <discussion>"""+self.discussion.rsplit(' ', 3)[0]+"""</discussion>\n
            <conclusion>"""+self.conclusion.rsplit(' ', 1)[0]+"""</conclusion>\n
            <acknowledgments>"""+self.acknow.rsplit(' ', 2)[0]+"""</acknowledgments>\n
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
        dictionnaryPath = os.path.dirname(os.path.realpath(__file__))+os.path.sep+"firstnames.txt"
        # firstnames est une liste de str
        with open(dictionnaryPath, "r") as dictionnaryFile:
            self.firstnames = dictionnaryFile.readlines()

    # retourne le numero de la premiere ligne contenant un prenom
    # on suppose que le fichier firstnames.txt se trouve dans le meme repertoire
    def nbFirstLineWithName(self):
        # parcourir le contenu a parser
        fileLines = self.content.split("\n")
        for line in fileLines:
            for firstname in self.firstnames:
                for word in re.findall(r"[\w']+", line):
                    if word == (firstname.upper()[0] + firstname.lower()[1:-1]):
                        return self.content.find(line)


    # premiere ligne ou contenu avant la premiere ligne contenant un prenom
    def getTitle(self):
        return self.content[0:self.nbFirstLineWithName()].replace('\n', ' ')

    # entre le titre et l'abstract
    def getAuteurs(self):
        ss = re.search('(?is)(.*?)\Z',self.content)
        if ss:
            auteurs = ss.group(1).replace('\n', ' ')
            tmp = self.getBiblio()
            tmp2 = self.getAcknow()
            tmp3 = self.getConclusion()
            tmp4 = self.getDiscussion()
            tmp5 = self.getCorps()
            tmp6 = self.getIntroduction()
            tmp7 = self.getAbstract()
            tmp8 = self.getTitle()
            return auteurs.replace(tmp, '').replace(tmp2, '').replace(tmp3, '').replace(tmp4, '').replace(tmp5, '').replace(tmp6, '').replace(tmp7, '').replace(tmp8, '')
        print("FOUND NO AUTHORS")
        return ""

    # contenu entre abstract et introduction
    def getAbstract(self):
        ss = re.search('(?is)Abstract(.*?)\Z',self.content)
        if ss:
            abstract = ss.group(1).replace('\n',' ')
            tmp = self.getBiblio()
            tmp2 = self.getAcknow()
            tmp3 = self.getConclusion()
            tmp4 = self.getDiscussion()
            tmp5 = self.getCorps()
            tmp6 = self.getIntroduction()
            return abstract.replace(tmp, '').replace(tmp2, '').replace(tmp3, '').replace(tmp4, '').replace(tmp5, '').replace(tmp6, '')
        return ""

    def getIntroduction(self):
        ss = re.search('(?is)Introduction\n(.*?)\Z',self.content)
        if ss:
            introduction = ss.group(1).replace('\n',' ')
            tmp = self.getBiblio()
            tmp2 = self.getAcknow()
            tmp3 = self.getConclusion()
            tmp4 = self.getDiscussion()
            tmp5 = self.getCorps()
            return introduction.replace(tmp, '').replace(tmp2, '').replace(tmp3, '').replace(tmp4, '').replace(tmp5, '')
        return ""

    # contenu entre l'intro et la conclusion
    def getCorps(self):
        ss = re.search('(?is)Introduction.*?\nII(.*?)\Z',self.content)
        if ss:
            corps = ss.group(1).replace('\n',' ')
            tmp = self.getBiblio()
            tmp2 = self.getAcknow()
            tmp3 = self.getConclusion()
            tmp4 = self.getDiscussion()
            return corps.replace(tmp, '').replace(tmp2, '').replace(tmp3, '').replace(tmp4, '')
        else:
            ss = re.search('(?is)Introduction.*?\n2(.*?)\Z',self.content)
            if ss:
                corps = ss.group(1).replace('\n',' ')
                tmp = self.getBiblio()
                tmp2 = self.getAcknow()
                tmp3 = self.getConclusion()
                tmp4 = self.getDiscussion()
                return corps.replace(tmp, '').replace(tmp2, '').replace(tmp3, '').replace(tmp4, '')
        return ""

    def getDiscussion(self):
        ss = re.search('(?is)Discussion(.*?)\Z',self.content.split("\n", 200)[-1])
        if ss:
            discussion = ss.group(1).replace('\n',' ')
            tmp = self.getBiblio()
            tmp2 = self.getAcknow()
            tmp3 = self.getConclusion()
            return discussion.replace(tmp, '').replace(tmp2, '').replace(tmp3, '')
        else:
            ss = re.search('(?is)Discussion(.*?)\Z',self.content)
            if ss:
                discussion = ss.group(1).replace('\n',' ')
                tmp = self.getBiblio()
                tmp2 = self.getAcknow()
                tmp3 = self.getConclusion()
                return discussion.replace(tmp, '').replace(tmp2, '').replace(tmp3, '')
        return ""

    # avant la biblio
    def getConclusion(self):
        ss = re.search('(?is)Conclusion(.*?)\Z',self.content.split("\n", 500)[-1])
        if ss:
            conclusion = ss.group(1)
            conclusion =  '\n'.join(conclusion.split('\n')[1:]).replace('\n',' ')
            tmp = self.getBiblio()
            tmp2 = self.getAcknow()
            return conclusion.replace(tmp,'').replace(tmp2,'')
        else:
            ss = re.search('(?is)Conclusion(.*?)\Z',self.content)
            if ss:
                conclusion = ss.group(1)
                conclusion =  '\n'.join(conclusion.split('\n')[1:]).replace('\n',' ')
                tmp = self.getBiblio()
                tmp2 = self.getAcknow()
                return conclusion.replace(tmp,'').replace(tmp2,'')
        return ""

    def getAcknow(self):
        ss = re.search('(?is)Acknowledgment(.*?)\Z',self.content)
        if ss:
            acknow = ss.group(1).replace('\n',' ')
            tmp = self.getBiblio()
            return acknow.replace(tmp,'')[1:]
        else:
            ss = re.search('(?is)Acknowledgement(.*?)\Z',self.content)
            if ss:
                acknow = ss.group(1).replace('\n',' ')
                tmp = self.getBiblio()
                return acknow.replace(tmp,'')[1:]
        return ""

    # derniere page ou après Aknowledgments et References
    def getBiblio(self):
        ss = re.search('(?is)\nReferences\n(.*?)\Z',self.content.split("\n", 500)[-1])
        if ss:
            return ss.group(1).replace('\n',' ')
        else:
            ss = re.search('(?is)References(.*?)\Z',self.content.split("\n", 500)[-1])
            if ss:
                return ss.group(1).replace('\n',' ')
            else:
                ss = re.search('(?is)\nReferences\n(.*?)\Z',self.content)
                if ss:
                    return ss.group(1).replace('\n',' ')
                else:
                    ss = re.search('(?is)References(.*?)\Z',self.content)
                    if ss:
                        return ss.group(1).replace('\n',' ')
        return ""

class Manager:

    def __init__(self):
        # on suppose que le targetDir est dans le meme repertoire que le script
        self.targetDir=os.path.dirname(os.path.realpath(__file__))+os.path.sep+sys.argv[1]
        self.outputDir=self.targetDir+os.path.sep+"output"
        self.tmpDir="./tmp"

        #On verifie que les dossiers ne sont pas présents au démarrage du script
        self.removeOutputFolder()
        self.removeTemporaryFolder()

        #On les crée
        os.mkdir(self.outputDir, 0o755)
        print("Répertoire output crée")
        os.mkdir(self.tmpDir, 0o755)
        self.analyseTargetFolder()
        index = 0
        self.choices = []
        for file in self.files:
            self.choices.insert(index, 0)

    def createTemporaryFiles(self):
        # convertir les PDF en format txt avec pdftotext dans un dossier tmp
            index = 0
            for filename in self.files:
                if self.choices[index] == 1 and filename.endswith('.pdf'):
                    f = filename.replace(" ","\ ")
                    os.system("pdftotext -raw "+self.targetDir+os.path.sep+f+" "+self.tmpDir+os.path.sep+f[:-3]+"txt")
                index += 1

    def convert(self):
        # # deposer les sorties au format .txt, avec meme nom que pdf respectif
        for filename in os.listdir(self.tmpDir):
            # parsing vers entite Paper
            paper = PaperEnt()
            parser = Parser(PersiFichierTexte.persiToString(self.tmpDir+os.path.sep+filename))
            paper.filename=filename[:-4]+".pdf"
            paper.title=parser.getTitle()
            paper.auteurs=parser.getAuteurs()
            paper.abstract=parser.getAbstract()
            paper.intro=parser.getIntroduction()
            paper.discussion=parser.getDiscussion()
            paper.biblio=parser.getBiblio()
            paper.corps=parser.getCorps()
            paper.acknow=parser.getAcknow()
            paper.conclusion=parser.getConclusion()
            # ecriture de l'entite Paper au format texte dans le dossier output
            if len(sys.argv) <= 2 or sys.argv[2] == "-t" :
                PersiFichierTexte.stringToPersi(paper.toText(),self.outputDir+os.path.sep+filename)
            elif sys.argv[2] == "-x" :
                PersiFichierTexte.stringToPersi(paper.toXML(),self.outputDir+os.path.sep+filename[:-3]+"xml")
            else :
                print("Unvalid option " + sys.argv[2])
                break

    def removeTemporaryFolder(self):
        if os.path.exists(self.tmpDir):
                shutil.rmtree(self.tmpDir)

    def displayListOfFiles(self):
        print("Liste des fichiers pris en charges :")
        index = 0
        for file in self.files:
            chosen = " "
            if(self.choices[index] == 1):
                chosen = "X"
            print(str(index) + ". " + chosen + " " + file)
            index += 1

    def askChoiceInput(self):
        self.displayListOfFiles()
        print("---------------------")
        choice = input("Veuillez choisir un fichier à convertir par son numéro (entrez 'a' pour tout sélectionner ,'c' pour lancer la conversion, 'T' pour une jolie bannière): ")
        if choice.isdigit():
            if int(choice)+1 > len(self.files):
                print("ERREUR: Aucun fichier n'est identifié par l'entrée donnée")
            else:
                if (self.choices[int(choice)] == 1):
                    self.choices[int(choice)] = 0
                else:
                    self.choices[int(choice)] = 1
        else:
            if(choice == "c"):
                return 1
            elif(choice == "T"):
                self.displayBanner()
            elif(choice == "a"):
                for i in range(len(self.choices)):
                    self.choices[i] = 1
            else:
                print("ERREUR: Commande inconnue")
        return 0

    def choiceLoop(self):
        loopOver = 0
        while loopOver != 1:
            loopOver = self.askChoiceInput()

    def analyseTargetFolder(self):
        index = 0
        self.files = []
        for filename in os.listdir(self.targetDir):
            if filename.endswith(".pdf"):
                self.files.insert(index, filename)
                index += 1

    def displayBanner(self):
        print("")
        print(PersiFichierTexte.persiToString("art"))
        print("")

    def removeOutputFolder(self):
        if os.path.exists(self.outputDir):
                shutil.rmtree(self.outputDir)
                print("Répertoire output supprimé")
        else:
            print("Le repertoire output ne peut être supprimé, il n'existe pas")


def main():
    manager = Manager()
    manager.displayBanner()
    manager.choiceLoop()
    manager.createTemporaryFiles()
    manager.convert()
    manager.removeTemporaryFolder()

main()

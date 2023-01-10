# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 11:02:35 2022

@author: bourh
"""
import re
import pandas as pd

class Corpus:
    
    '''
    nom
    authors
    documents
    ndoc
    naut
    '''
    
    def __init__(self, nom, authors={}, documents={}, ndoc=0, naut=0):
        self.nom = nom
        self.authors = authors
        self.documents = documents
        self.ndoc = ndoc
        self.naut = naut
    
    def __repr__(self):
        docs = list(self.documents.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))
        
    def getDocuments(self):
        return self.documents
    
    def sortTitre(self, nbDocs):
        return self.documents
        docSorted = sorted(self.documents.items(), key=lambda doc:doc[1].titre)
        for i in range(nbDocs):
             print(docSorted[i][1])
    
    def sortDate(self, nbDocs):
        docSorted = sorted(self.documents.items(), key=lambda doc:str(doc[1].date))
        for i in range(nbDocs):
             print(docSorted[i][1])
             
    def save(self):
        f = open("corpus.txt", "w")
        f.write(self.__repr__())
        f.close()
        
    def load(self):
        f = open("corpus.txt", "r")
        return f.read()
    
    def search (self, keyword, text):
        #on enlève les sauts de ligne
        text=re.sub("\n", " ", text)
        passages=[]
        for sentence in text.split("."):
            match = re.search(keyword, sentence)
            if match:
                passages.append(sentence)
        return passages
    
    def concorde(self, keyword, text, size):
        #on enlève les sauts de ligne
        text=re.sub("\n", " ", text)
        passages = self.search(keyword, text)
        contextes=[]
        for p in passages:
            #on sépare en 2 le passage à partir du keyword
            passage = re.split(keyword, p, 1)
            #ce qui est à gauche du keyword sous forme de liste pour extraire les omts
            passageGauche = passage[0].split()
            passageDroit = passage[1].split()
            contextes.append([" ".join(passageGauche[-size:]), keyword, " ".join(passageDroit[:size])])
        df = pd.DataFrame(contextes, columns=['gauche', 'motif', 'droit'])
        return df
    
    def nettoyer_texte(self,text):
        text = text.lower()
        #enlève les sauts de ligne
        text = re.sub(r'\n', ' ', text)
        text = re.sub(r'[^\w\s]', '', text)
        #enlève les chiffres
        text = re.sub(r'\d', '', text)
        return text
    
    def stats(self, text):
        documents = self.getDocuments()
        #dictionnaire des mots et de leur nombre d'occurences
        termFreq = {}
        for i in range(self.ndoc):
            doc = documents[i].getTexte()
            cleanDoc = self.nettoyer_texte(doc)
            for word in cleanDoc.split():
                if word not in termFreq:
                    termFreq[word] = 1
                else:
                    termFreq[word] += 1
        freq = pd.DataFrame(termFreq.items(), columns=['words', 'term frequency'])
        return freq
        
    def sortVocab(self, text):
        documents = self.getDocuments()
        #dictionnaire des mots et de leur nombre d'occurences
        termFreq = {}
        for i in range(self.ndoc):
            doc = documents[i].getTexte()
            cleanDoc = self.nettoyer_texte(doc)
            for word in cleanDoc.split():
                if word not in termFreq:
                    termFreq[word] = 1
                else:
                    termFreq[word] += 1
        #vocabulary 
        sortedVocab = {}
        uniqueId = 0
        for key in sorted(termFreq.keys()):
            sortedVocab[key] = {'id': uniqueId, 'nombre total occurence' : termFreq[key], 'nombre de document' : 0}
            uniqueId += 1
        return sortedVocab
    

        
        
        
        
        
        
        
        
        
        
        
        
    
    
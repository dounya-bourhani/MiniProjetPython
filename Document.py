# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 14:12:56 2022

@author: bourh
"""

class Document:
    
    '''
    - titre
    - auteur
    - date
    - url
    - texte
    - type
    '''
    
    def __init__(self, titre, auteur, date, url, texte):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        
    def __str__(self):
        return("Titre du document : " + self.titre )
    
    def getTitre(self):
        return self.titre
    
    def getAuteur(self):
        return self.auteur
    
    def getDate(self):
        return self.date
    
    def getTexte(self):
        return self.texte
    
    def getType(self):
        pass
    
    
    
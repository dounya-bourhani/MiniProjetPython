# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 15:04:13 2022

@author: bourh
"""
from Document import Document

class ArxivDocument(Document):
    
    '''
    - titre
    - auteur
    - date
    - url
    - texte
    - type
    '''
    
    def __init__(self, titre, auteur, date, url, texte):
        super().__init__(titre, auteur, date, url, texte)
        
    def __str__(self):
        return("Titre du document Arxiv : " + self.titre + "\nAuteur : " + str(self.auteur) + "\nTexte : " + self.texte + "\nDate : " + str(self.date))
    
    def getType(self):
        return "Arxiv"
        
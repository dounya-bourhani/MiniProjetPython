# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 14:42:56 2022

@author: bourh
"""
from Document import Document

class RedditDocument(Document):
    
    '''
    - titre
    - auteur
    - date
    - url
    - texte
    - nbCommentaires
    - type
    '''
    
    def __init__(self, titre, auteur, date, url, texte, nbCom):
        super().__init__(titre, auteur, date, url, texte)
        self.nbCom = nbCom
        
    def __str__(self):
        return("Titre du document Reddit: " + self.titre + "\nAuteur : " + str(self.auteur) + "\nResumé : " + self.texte + "\nDate : " + str(self.date) + "\nNombres de commentaires : " + str(self.nbCom))
    
    def getCommentaires(self):
        return self.commentaires
    
    def setCommentaires(self, commentaires):
        self.commentaires = commentaires
        
    def getType(self):
        return "Reddit"
        
    
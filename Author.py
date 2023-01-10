# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 15:17:07 2022

@author: bourh
"""

class Author:
    
    '''
    - nom
    - ndoc
    - production
    '''
    
    def __init__(self, nom, ndoc=0, production={}):
        self.nom = nom
        self.ndoc = ndoc
        self.production = production
        
    def add(self, document):
        longueurDico = len(self.production)
        self.production[longueurDico] = document
        self.ndoc += 1
    
    def __str__(self):
        return("Auteur : " + self.nom + 
               "\nNombre de document publiés : " + str(self.ndoc))
    
    def getNdoc(self):
        return self.ndoc
    
    def getProduction(self):
        return self.production
    
    
    
    
    
    
    
    
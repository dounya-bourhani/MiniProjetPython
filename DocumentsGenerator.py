# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 18:56:09 2022

@author: bourh
"""
import RedditDocument as redditDoc 
import ArxivDocument as arxivDoc

class DocumentsGenerator:
    
    @staticmethod
    def factory(type, titre, auteur, date, url, texte, nbCom):
        if type == "Reddit" : return redditDoc.RedditDocument(titre, auteur, date, url, texte, nbCom)
        if type == "Arxiv" : return arxivDoc.ArxivDocument(titre, auteur, date, url, texte)
        
        assert 0, "Erreur : " + type    
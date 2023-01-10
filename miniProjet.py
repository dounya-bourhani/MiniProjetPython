# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 12:16:58 2022

@author: bourh
"""

# RedditDocument
import DocumentsGenerator as docGen

import praw

reddit = praw.Reddit(client_id='ec5FgSk-d3hUFJVoJNogrw', client_secret='bhCrt4HvyS1yhyF5nbKRsCuAJGnIeQ', user_agent='TD3')

subr = reddit.subreddit('Coronavirus')

id2doc = {}

import RedditDocument as redditDoc
import datetime

#   ajout des documents Reddit dans id2doc
i = 0   # clé du dictionnaire 
for post in subr.hot(limit=100):
    documentReddit = docGen.DocumentsGenerator.factory("Reddit", post.title, post.author, datetime.datetime.fromtimestamp(post.created), post.url, post.selftext, 1)
    id2doc[i] = documentReddit
    i += 1
print(documentReddit.getTexte())
# ArxivDocument 

import urllib.request
import xmltodict 
#import ArxivDocument as arxivDoc

query = "covid"
url = 'http://export.arxiv.org/api/query?search_query=all:' + query + '&start=0&max_results=100'
url_read = urllib.request.urlopen(url).read()

# url_read est un "byte stream" qui a besoin d'être décodé
data =  url_read.decode()
dico = xmltodict.parse(data) #xmltodict permet d'obtenir un objet ~JSON
docs = dico['feed']['entry']

# ajout des document Arxiv dans id2doc
for d in docs:
    listAuthors=[]
    if isinstance(d['author'], list):
        for auteur in d['author']:
            listAuthors.append(auteur['name'])
    else:
        listAuthors.append(d['author']['name'])
    #documentArxiv = arxivDoc.ArxivDocument(d['title'], listAuthors, d['published'], d['link'], d['summary'])
    documentArxiv = docGen.DocumentsGenerator.factory("Arxiv", d['title'], listAuthors, d['published'], d['link'], d['summary'], 0)
    id2doc[i] = documentArxiv
    i += 1
    
# Corpus 
    
import Author as aut

id2aut = {} 

for doc in id2doc :
    document = id2doc[doc]
    type(document)
    #si le doc vient de reddit il n'y a qu'un seul auteur
    if isinstance(document, redditDoc.RedditDocument):
        #si l'auteur n'est pas déja dans id2aut ou crée un nouvel auteur
        if document.getAuteur() not in id2aut:
            nouvAuteur = aut.Author(document.getAuteur(), 0, {})
            nouvAuteur.add(document)
            id2aut[document.getAuteur()] = nouvAuteur
        else:
            id2aut[document.getAuteur()].add(document)
    #si le doc vient de arxiv il y a plusieurs auteurs
    else:
        for nomAuteur in document.getAuteur():
            if nomAuteur not in id2aut:
                nouvAuteur = aut.Author(nomAuteur, 0, {})
                nouvAuteur.add(document)
                id2aut[nomAuteur] = nouvAuteur
            else:
                id2aut[nomAuteur].add(document)
 
import Corpus as corp
corpus = corp.Corpus("Corpus Coronavirus", id2aut, id2doc, len(id2doc), len(id2aut))
corpus.save()
#corpus.load()

print(corpus.search("crisis", corpus.load()))
concordancier = corpus.concorde("crisis", corpus.load(), 5)
#------------------- Partie 1 : matrice Documents x Mots ----------------------

# Matrice TF
freq = corpus.stats(corpus.load())
print(freq)

vocab = corpus.sortVocab(corpus.load)
print(vocab)

import re
def nettoyer_texte(text):
    text = text.lower()
    #enlève les sauts de ligne
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    #enlève les chiffres
    text = re.sub(r'\d', '', text)
    return text

#récupérer la liste des documents nettoyer
listDoc = []
for t in corpus.getDocuments().values():
    listDoc.append(nettoyer_texte(t.getTexte()))

import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(vocabulary=vocab.keys())
mat_TF = vectorizer.fit_transform(listDoc)
result = pd.DataFrame(data=mat_TF.toarray(), columns=vectorizer.get_feature_names_out())
print(result)

    
# ajouter a vocab le nombre total de documents contenant chaque mot
nbLine = mat_TF.shape[0]
nbCol = mat_TF.shape[1]
mat_TF_array = mat_TF.toarray()
for c in range(nbCol):
    for l in range(nbLine):
        if mat_TF_array[l][c] != 0:
            list(vocab.values())[c]['nombre de document'] += 1


# Matrice TFxIDF
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
mat_TFxIDF = vectorizer.fit_transform(listDoc)
print(mat_TFxIDF)


# --------------- Partie 2 : moteur de recherche --------------------------

#cos_similarity_matrix = (mat_TFxIDF * mat_TFxIDF.T).toarray()
#print(cos_similarity_matrix)

""" similarité entre notre vecteur requête et tous les documents """

#demander à l’utilisateur d’entrer quelques mots-clefs
keywords = input("Entrez quelques mot-clefs : ").split()

import numpy as np

scores=[]

for doc in listDoc:
    doc = doc.split()
    
    A=[]; B=[]
    
    rvector = keywords + doc
    for w in rvector:
        if w in keywords: A.append(1) # create a vector
        else: A.append(0)
        if w in doc: B.append(1)
        else: B.append(0)
    c=0
    
    if sum(B) != 0:
        # cosine formula 
        for i in range(len(rvector)):
                c+= A[i]*B[i]
        cosine = c / float((sum(A)*sum(B))**0.5)
    else:
        cosine = 0
    scores.append(cosine)
    
#trier les scores
scores.sort(reverse=True)
top_scores = scores[:10]
print("Les 10 meilleurs scores :", top_scores)

















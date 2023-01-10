# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 17:57:11 2023

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

# création corpus Reddit
import Author as aut
import Corpus as corp

id2aut = {} 

for doc in id2doc :
    document = id2doc[doc]
    if document.getAuteur() not in id2aut:
        nouvAuteur = aut.Author(document.getAuteur(), 0, {})
        nouvAuteur.add(document)
        id2aut[document.getAuteur()] = nouvAuteur
    else:
        id2aut[document.getAuteur()].add(document)

corpusReddit = corp.Corpus("Corpus Coronavirus Reddit", id2aut, id2doc, len(id2doc), len(id2aut))        
corpusReddit.save("corpusReddit")


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
id2doc = {}
i = 0   # clé du dictionnaire 
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
    
# Création corpus Arxiv
id2aut = {} 
for doc in id2doc : 
    document = id2doc[doc]
    for nomAuteur in document.getAuteur():
        if nomAuteur not in id2aut:
            nouvAuteur = aut.Author(nomAuteur, 0, {})
            nouvAuteur.add(document)
            id2aut[nomAuteur] = nouvAuteur
        else:
            id2aut[nomAuteur].add(document)
 
corpusArxiv = corp.Corpus("Corpus Coronavirus", id2aut, id2doc, len(id2doc), len(id2aut))
corpusArxiv.save("corpusArxiv")

import re
def nettoyer_texte(text):
    text = text.lower()
    #enlève les sauts de ligne
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    #enlève les chiffres
    text = re.sub(r'\d', '', text)
    return text

from sklearn.feature_extraction.text import TfidfVectorizer


fileReddit = nettoyer_texte(corpusReddit.load("corpusReddit"))
fileArxiv = nettoyer_texte(corpusArxiv.load("corpusArxiv"))

from sklearn.feature_extraction.text import TfidfVectorizer

keywords = input("Entrez quelques mot-clefs : ")

def cosine_sim(text1, text2):
    tfidf = TfidfVectorizer().fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

sim_Reddit = cosine_sim(keywords, fileReddit)
sim_Arxiv = cosine_sim(keywords, fileArxiv)
print("Score similarité Reddit :", sim_Reddit)
print("Score similarité Arxiv :", sim_Arxiv)

corpus_Plus_Sim = ""
if sim_Reddit > sim_Arxiv:
    corpus_Plus_Sim = "Reddit"
else:
    corpus_Plus_Sim = "Arxiv"
print("Les mots clés que vous avez entrés ont plus d'importance dans le corpus", corpus_Plus_Sim)

















import numpy as np
from glob import glob
import string
import os
from textblob import TextBlob
import unicodedata
import codecs
import re

def make_window_weights(window):
    weights = np.concatenate((np.linspace(0,window,num=window),[0],np.linspace(window,0,num=window)))
    return weights

def only_capitals(s):
    return re.sub(r'[^A-Z]', '', s)

def readtolist(f):
    text = []
    with codecs.open(f, mode='r', encoding='utf-8') as F:
        for line in F.readlines():
            line = unicodedata.normalize('NFKD',line).encode('ascii','ignore')
            text.extend([only_capitals(X.translate(None,string.punctuation+string.digits+string.whitespace).upper()) for X in line.split(" ")])
        text = filter(lambda x: len(x.strip())>2, text)
    return text

def find_all(tblob,word):
    occurence = []
    start = 0
    while 1:
        try:
            occ = tblob.index(word, start=start)
            occurence.append(occ)
            start=occ+1
        except ValueError:
            break
    return occurence

def unique_words(files):
    all_u = np.empty((0),dtype='string')
    for f in files:
        text = readtolist(f)
        u = np.unique(text)
        all_u = np.concatenate((all_u,u))
    uniques = np.unique(all_u)
    return uniques
    
def textblobber(pdf,uniques,wordmatrix,window,w):
    text = readtolist(pdf)
    tblob = TextBlob(" ".join(text))
    for j,word in enumerate(uniques):
        print str(j)+"of"+str(len(uniques))+"words:"+word
        indices = find_all(tblob,word)
        for i in indices:
            sl_start = max(0, i-window)
            sl_end =  min(i+window, len(text)-1)
            sl = slice(sl_start, sl_end)
            offset_start = max(0,0-(i-window))
            offset_end = min(len(w)-1, len(w)+len(text)-(i+window)-2)
            for k,wrd in enumerate(tblob.words[sl]):
                u_index = np.where(uniques==wrd)[0][0]
                wordmatrix[j][u_index] += w[offset_start:offset_end][k]
    return wordmatrix
            
file1 = '/home/rschadmin/Soft/pdftocog/9558644.txt'
file2 ='/home/rschadmin/Soft/pdftocog/21368084.txt'
file3 ='/home/rschadmin/Data/scraped/20533557.txt'
file4 = '/home/rschadmin/Data/scraped/21273403.txt'
file5 = '/home/rschadmin/Data/scraped/21277171.txt'
file6 = '/home/rschadmin/Data/scraped/19580873.txt'
files = [file1,file2,file3,file4,file5,file6]
files = glob('/home/rschadmin/Data/scraped/*.txt')[:100]
uniques_file = "/home/rschadmin/Soft/pdftocog/uniques_100files.npy"
if not os.path.exists(uniques_file):
    print "running uniques"
    uniques= unique_words(files)
    np.save(uniques_file,uniques)
else:
    uniques = np.load(uniques_file)
window = 50
weights = make_window_weights(window)
wordmatrix= np.zeros((len(uniques)+1,len(uniques)+1))

for f in files[:3]:
    print "textblobbing file "+str(f)+"\n"
    wordmatrix= textblobber(f,uniques,wordmatrix,window,weights)
    corrmatrix= np.corrcoef(wordmatrix)

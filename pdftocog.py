import numpy as np
from glob import glob
import string
from sklearn.metrics import mean_squared_error as mse
from textblob import TextBlob
import unicodedata
import codecs

def make_window_weights(window):
    weights = np.concatenate((np.linspace(0,window,num=window),[0],np.linspace(window,0,num=window)))
    return weights

def readtolist(f):
    text = []
    with codecs.open(f, mode='r', encoding='utf-8') as F:
        for line in F.readlines():
            line = unicodedata.normalize('NFKD',line).encode('ascii','ignore')
            text.extend([X.translate(None,string.punctuation+string.digits+string.whitespace).upper() for X in line.split(" ")])
        text = filter(lambda x: len(x.strip())>1, text)
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
files = glob('/home/rschadmin/Data/scraped/*.txt')
uniques= unique_words([file6])
#window = 4
#w = np.array([1,2,3,4,0,4,3,2,1]) #window weight
window = 50
weights = make_window_weights(window)
wordmatrix= np.zeros((len(uniques)+1,len(uniques)+1))
wordmatrix= textblobber(file6,uniques,wordmatrix,window,weights)

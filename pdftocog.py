from textblob import TextBlob
import numpy as np
import string
from sklearn.metrics import mean_squared_error as mse

def make_window_weights(window):
    weights = np.concatenate((np.linspace(0,100,num=window),[0],np.linspace(100,0,num=window)))
    return weights
file1 = '/home/rschadmin/Soft/pdftocog/9558644.txt'
file2 ='/home/rschadmin/Soft/pdftocog/21368084.txt'
#window = 4
#w = np.array([1,2,3,4,0,4,3,2,1]) #window weight

def readtolist(f):
    text = []
    with open(f, 'r') as F:
        for line in F.readlines():
            try:
                line.decode("ascii")
                text.extend(line.strip("\n").translate(None,string.punctuation).split(" "))
            except UnicodeDecodeError:
                pass
    return text
    
text = readtolist(file1)
text = filter(lambda x: len(x.strip())>0, text)
#tb = TextBlob(" ".join(text1))

window = 20
w = make_window_weights(window)

u, index = np.unique(text, return_inverse=True)
num_unique = len(u)+1
matrix = np.zeros((num_unique,num_unique))

for word in xrange(num_unique):
    for i in np.where(index==word)[0]:
        sl_start = max(0, i-window)
        sl_end =  min(i+window, len(index)-1)
        sl = slice(sl_start, sl_end)
        j = index[sl]
        offset_start = max(0,0-(i-window))
        offset_end = min(len(w)-1, len(w)+len(index)-(i+window)-2)
        for x,j in enumerate(index[sl]):
            matrix[word][j] = matrix[word][j]+w[offset_start:offset_end][x]

#for word in xrange(num_unique):    
#    matrix[word]=index==word

#simmatrix = np.zeros((num_unique,num_unique))
#for i in xrange(num_unique):
#    for j in xrange(num_unique):
#        simmatrix[i,j] = np.sqrt(mse(matrix[i],matrix[j]))
    

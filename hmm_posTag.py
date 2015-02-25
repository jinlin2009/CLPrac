import os
import numpy as np
import viterbi

print("Starts!")
print("Training!!")

def train( testSection ) : # section from 0 to 9
  words = {} # list of {[words,index]...} 
  wordIndex = [] # index map of the word; reverse of words{}
  CATs = {} # list of {[CATs,index]...} 
  catIndex = [] # index map of cat; reverse of cats{}

  CATs["START"]=0 #"START" takes the first slot in cat
  catIndex.append("START")
  Amatrix = np.zeros((80,80)) #initially sign Amatrix to be a 80 by 80 matrix with 0.00001 value
  Amatrix.fill(0.00001) # [pCAT | CAT] count
  pWC = np.zeros((100000,80)) #p matrix for storing the p[word/cat] 
  pWC.fill(0.00001)

  testCats = []
  testWords = []
  testnum = 0
  testOn = 0  # testOn = 1 means getting data for test
  num = 0 #total number of '==' is 10700

  for filename in os.listdir('WSJ-2-12/'):
    for files in os.listdir('WSJ-2-12/'+filename+'/'):
      f = open('WSJ-2-12/'+filename+'/'+files)
      fileText = f.read()
      wordCats = fileText.split()
      #pCat = "START" # = starts a new sentence.
      
      # loop through all the word in file f.
      for wordCat in wordCats:
        if "=" in wordCat: 
          pCat = "START" # = starts a new sentence. 
          if num/1070 >= testSection and num/1070 < (testSection+1):
            testOn = 1
            testCats.append([])
            testWords.append([])
            testnum = testnum + 1
          else :
            testOn = 0
          num = num+1
          continue
        if not "/" in wordCat: continue
        
        tokens = wordCat.split("/")
        if not len(tokens) == 2 :
          wordCat = wordCat.replace('\\/','|') # special case
          tokens = wordCat.split("/")
          if not len(tokens) == 2 :
            continue #discard
  
        if not words.has_key(tokens[0]) :
          words[tokens[0]] = len(words)
          wordIndex.append(tokens[0])
          # count the cat, and add it in the map.
        if not CATs.has_key(tokens[1]) :
          CATs[tokens[1]] = len(CATs)
          catIndex.append(tokens[1])
          
        if testOn :
          testWords[testnum-1].append(words[tokens[0]])
          testCats[testnum-1].append(CATs[tokens[1]]-1)# save one slot for the "start"
        # count the word, and add it in the map.
        else :
          Amatrix[CATs[pCat]][CATs[tokens[1]]] = Amatrix[CATs[pCat]][CATs[tokens[1]]]+1
          pWC[words[tokens[0]]][CATs[tokens[1]]] = pWC[words[tokens[0]]][CATs[tokens[1]]] + 1
          pCat = tokens[1] #update the previous cat
         
  print testnum
  print num 
  return Amatrix, pWC, CATs, words, wordIndex, catIndex, testWords, testCats  ## the end of train function.
'''
wrong = 0
totaln = 0
for j in range(10) :
  Amatrix, pWC, CATs, words, wordIndex, catIndex, testWords, testCats = train(j) # train the first section
  sumSen = sum(Amatrix[0])
  trans = Amatrix[1:len(CATs),1:len(CATs)] # remove the "start" state
  pi = np.atleast_2d(Amatrix[0, 1:len(CATs)]/sumSen).T # initial probability
  row_sum = np.sum(trans, axis=1)
  trans_prob = trans/np.atleast_2d(row_sum).T # calculate the tran prob
  pWC = pWC[:len(wordIndex), 1:len(CATs)]  # remove the "start" state
  col_sum = np.sum(pWC, axis=0)
  catw_prob = pWC/np.atleast_2d(col_sum) # calculate the word|cat prob

  # build viterbi algorithm
  d = viterbi.Decoder(pi, trans_prob, catw_prob.T)

  ## n fold validation 
  for i in range(0, len(testWords)-1):
    w = testWords[i]
    t = testCats[i]
    if len(w) > 1:
      pt = d.Decode(w)
      wrong = wrong + len([i for i, j in zip(pt, t) if not i == j])
      totaln = totaln + len(pt)
      
print round(float(wrong)/totaln, 8)
'''
## demo part
print "start demo: trying the whole data set"
Amatrix, pWC, CATs, words, wordIndex, catIndex, testWords, testCats = train(100) # train the whole data
sumSen = sum(Amatrix[0])
trans = Amatrix[1:len(CATs),1:len(CATs)] # remove the "start" state
pi = np.atleast_2d(Amatrix[0, 1:len(CATs)]/sumSen).T # initial probability
row_sum = np.sum(trans, axis=1)
trans_prob = trans/np.atleast_2d(row_sum).T # calculate the tran prob
pWC = pWC[:len(wordIndex), 1:len(CATs)]  # remove the "start" state
col_sum = np.sum(pWC, axis=0)
catw_prob = pWC/np.atleast_2d(col_sum) # calculate the word|cat prob

# build viterbi algorithm
d = viterbi.Decoder(pi, trans_prob, catw_prob.T)
#d.Decode(w)

while 1:
  var = raw_input("Please enter something: ")
  iSen = var.split()
  iWor = []
  print len(iSen)
  for i in range(len(iSen)):
    iWor.append(words[iSen[i]])
  oWord = d.Decode(iWor)

  oSen = []
  for i in range(len(oWord)):
    oSen.append(catIndex[oWord[i]+1])
    
  print oSen



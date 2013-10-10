# s0946868
# Machine Translation Spring 2013
# Assignment 1
# EM algorithm for IBM Model 1

# Please provide toy.en, toy.de, in the same folder as the source code. 
#always run english text first and foreign one second, as in:
# python em.py toy.en toy.de
import sys
import time
import string
import re

class EMalgorithm(object):
  def __init__(self, inputFiles):
    self.texts = inputFiles # we input 2 text files, first in english, second in a foreign language
    self.sentences_e=[] # list of english sentences
    self.sentences_f=[] # list of sentences in a foreign language
    self.words_e=[] # list of words in english that appear in the sentences, but without the duplicates
    self.words_f=[] # same as above, but in the foreign language
    self.pairs=[] # pairs of english-foreign language sentences
    self.all_alignments={} # foreign key, value=list of english words that are possible alignments of the foreign word which is a key
    self.prob_e_f={} # uniform probabilities of a given translation 
    self.total_s={} # total s
    self.total_f={} # total f
    self.count_e_f={} # count e|f
    self.converged={}
    self.oldest_probs={}
  
  def preprocess(self, text): # deals with the removal of unwanted symbols and loads the lists of words/sentences
    sentences  = []
    uniqueWords = []
    t = open(text, 'r') #open a text file
    for line in t.readlines():
	  #line = line.translate(string.maketrans("",""), string.punctuation) # remove all punctuation
	  line=line.lower() #turn all uppercase letters to lowercase
	  replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
	  line = line.translate(replace_punctuation)
	  line=re.sub("\d+", "", line)
	  sentences.append( line.rstrip() )
	  uniqueWords = uniqueWords + line.split()
    t.close()
    uniqueWords = list( set(uniqueWords) ) # remove duplicated words from a list of words
   # print uniqueWords, sentences
    return uniqueWords,sentences
    
  def allAlignments(self):
  # for each foreign word in the list of all words in the files
  # we need to find all english words that appear in the sentence translations as the foreign words
  # and list them as possible alignments
  	for w in self.words_f:
  		alignments=[]
  		for s in self.sentences_f: # if the word is in the foreign sentence
  			if w in s:				# then get the whole english translation of that sentence and list its words as values of the key in question
  				english_equivs=self.sentences_e[self.sentences_f.index(s)]
  				alignments+=english_equivs.split()
  		alignments =list( set (alignments))# remove duplicate possible translations
  		self.all_alignments[w]=alignments		
	#print 'all alignments possibilities', self.all_alignments
  
  def assignProbabilities(self):
	# assign uniform probabilities to each possible translation in english to start off with
	# this is t(e|f) in the slides
  	for w in self.words_f:
  		denominator=len(self.all_alignments[w])
  		if denominator>0:
  			prob=1.0/denominator
  			self.prob_e_f[w]=dict([(e,prob) for e in self.all_alignments[w]])
  			self.oldest_probs[w]=dict([(e,0)for e in self.all_alignments[w]])
  			
  			
  			
  			
  		#just added 15/02/2013
  		#elif denominator==0:
  		#	self.prob_e_f[w]="NULL"
  			
  			
  			
  			
  			
  			
  	#print self.prob_e_f
 
  def zeroing(self):
  # creates a dictionary with foreign words and zeroes 
  # creates another dictionary with foreign words , their possible translations and 0s as values of the transltations in the dict
  	for w in self.words_f:
  		self.total_f[w]=0
  		alignments=self.all_alignments[w]
  		self.count_e_f[w]=dict([(e,0) for e in alignments])
  		
  	#print "count f",self.total_f
  	#print "count e f",self.count_e_f
  
  def alg(self):
 	final=False
 	conv_list=[]
 	c=0
 	while not(final):
 		#print len(self.pairs)
 		self.zeroing() #initialize to 0 all probs and counts
 		for (es,fs) in self.pairs: #for every sentence pair
 			for e in es: #initialize the prob of each english word to 0
 				self.total_s[e]=0
 				for f in fs: #update total probs of english words based on the probs given the translation (t(e|f)
 					probs=self.prob_e_f[f]
 					if (e not in probs):
 						continue
 					#print 'probability of', e, 'is', probs[e]
	 				self.total_s[e]+=probs[e]
	 				#print 'hmmmmmmmmmmmmmm' ,self.total_s
	 		for e in es: #for each english word in a sentence pair 
	 			for f in fs:#for each foreign word in a sentence pair
	 				if (e not in self.prob_e_f[f]):
	 					continue #update counts by probs/total english 
	 				self.count_e_f[f][e]+=self.prob_e_f[f][e]/self.total_s[e]
	 				self.total_f[f]+=self.prob_e_f[f][e]/self.total_s[e]
 		 				
 		for f in self.words_f:
 			#print f
 			self.converged[f]=[]

 			#print "number of all english words", len(self.all_alignments[f])
 			
 			for e in self.all_alignments[f]:
 				#print self.prob_e_f[f][e],self.prob_e_f[f][e]+(self.count_e_f[f][e]/self.total_f[f])
 				current=self.prob_e_f[f][e]
 				new=self.count_e_f[f][e]/self.total_f[f]
 				oldest=self.oldest_probs[f][e]
 				#print "old prob", old
 				#print "new prob", new
 				
 				
 				if (current!=new):
 					self.oldest_probs[f][e]=self.prob_e_f[f][e]
 					self.prob_e_f[f][e]=self.count_e_f[f][e]/self.total_f[f]
 					
 				else:
 					if (current==oldest):
 						self.converged[f]+=['True']

 			
 					else:
	 					self.oldest_probs[f][e]=self.prob_e_f[f][e]
 						self.prob_e_f[f][e]=self.count_e_f[f][e]/self.total_f[f]				
 				
 				#if (self.prob_e_f[f][e]==self.prob_e_f[f][e]+(self.count_e_f[f][e]/self.total_f[f])): 
 				#	self.converged[f]+=['True']
					#print self.converged[f]
	 				#self.prob_e_f[f][e]=self.count_e_f[f][e]/self.total_f[f]
	 		#print self.converged[f]
	 		 #	print "number of converged", len(self.converged[f])
	 		if (len(self.converged[f])==len(self.all_alignments[f])):
	 		
	 			#print "CONVERGED", f
	 			conv_list+=['True'] 
	 			
	 	
 		if len(conv_list)==2*len(self.pairs):
 			print conv_list
 			final=True
 			#		if (self.prob_e_f[f][e]==1.0)or(self.prob_e_f[f][e]==0):
 					#	final=True
 			#			counter=counter+1
 			#			print counter
 					
 		#if counter==p:
		#if c>=30:#stop at iteration 100(waiting until convergence is too long)
		#	final=True
		#c+=1
		#print c
		
		
  def output(self):
    f = open('Word_translation_table2.txt','w')
    g = open ('Viterbi_alignments2.txt', 'w')
    for word in self.words_f:
      word_probs = self.prob_e_f[word]
      ordered_probs = sorted(word_probs.iteritems(), key=lambda (k,v): (v,k))
      ordered_probs.reverse()
      (high, rest) =  ordered_probs[0]
      m='%s %s %24s %s' % (word.ljust(20), '==>', high.ljust(24), '\n')
      g.write(m)
      line=[]
      line.append(word)
      for (a, b) in ordered_probs[:3]:
      	b=format(b,"g") #only print first few digits after the decimal point
      	l=a + ":" + str(b)
      	line.append(l)
      if len(line)==4:
	      k='%s %s %s %s %s' %  (line[0].ljust(20), '==>', line[1].ljust(25), line[2].ljust(25),line[3].ljust(25))
	      f.write(k)
	      f.write("\n")
      elif len(line)==3:
 	      k='%s %s %s %s' %  (line[0].ljust(20), '==>', line[1].ljust(25), line[2].ljust(25))
 	      f.write(k)
 	      f.write("\n")     
    f.close()
    g.close()

  def run(self): #run the algorithm
  	self.words_e,self.sentences_e= self.preprocess( self.texts[1] )
  	self.words_f,self.sentences_f= self.preprocess( self.texts[2] )
  	# pair each each english sentence with the corresponding foreign language one
  	self.pairs=[(self.sentences_e[x].split(),self.sentences_f[x].split()) for x in range(len(self.sentences_e))]
	self.allAlignments()
	self.assignProbabilities()
	self.alg()
	self.output()
	
def main():  
  args = sys.argv
  algorithm = EMalgorithm(args) #initialize class with input files
  algorithm.run() # run the EM algorithm
if __name__=="__main__":
  main()

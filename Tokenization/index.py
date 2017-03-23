#Python 2.7.3
import re
import os
import collections
import time

class index:
	def __init__(self,path):
		self.path = path

	def buildIndex(self):
		# function to read documents from collection, tokenize and build the index with tokens
		# index should also contain positional information of the terms in the document --- term: [(ID1,[pos1,pos2,..]), (ID2, [pos1,pos2,…]),….]
		# use unique document IDs
		start_time = time.time()
		document_dict = dict()
		master_dict = collections.defaultdict(dict)
		# To read the files from the folder
		for file in os.listdir(self.path):
			if file.endswith(".txt"):
				doc_id = re.sub('[^\d+]', "", file)
				doc = "doc" + str(doc_id)

				#Assigning unique id to each document
				document_dict.__setitem__(doc, file)

				#to read specific file
				currentFile = open(os.path.join(self.path,file), 'r')
				content = currentFile.read().lower()
				currentFile.close()

				content = re.sub('[^a-z\ \']+', " ", content)
				words = list(content.split())
			word_position_dict = dict((w, []) for w in words)
			i = 0
			#To store the positions of each word
			for word in words:
				if word not in word_position_dict.keys():
					word_position_dict.__setitem__(word, i)
				else:
					if word_position_dict.get(word) is None:
						word_position_dict.__setitem__(word, i)
					else:
						temp_list =  word_position_dict.get(word)
						temp_list.append(i)
						word_position_dict.__setitem__(word, temp_list)
				i += 1

			## For loop to store documents Ids and positions corresponding to each term
			for word in word_position_dict.keys():
				temp_dict = dict()
				if(master_dict[word]):
					temp_dict = master_dict.get(word)
				temp_dict[doc] = word_position_dict.get(word)
				master_dict[word][doc] = temp_dict[doc]
		self.master_dict = master_dict
		self.document_dict = document_dict
		print("Built index in:", (time.time() - start_time))



	def and_query(self, query_terms):
	#function for identifying relevant docs using the index
		start_time = time.time();

		master_dict= self.master_dict
		query_val_dict = collections.defaultdict()
		master_list = list()

		#To iterate over the query items
		for word in query_terms:
			word = word.lower()
			val_list = master_dict[word]
			master_list.append(val_list)

		#to find the merge of all the output document lists
		master_list = list(set.intersection(*map(set, master_list)))
		# To print the output of query
		print(sorted(master_list))
		print("Fetched query result in:", (time.time() - start_time))

	def print_dict(self):
	#function to print the terms and posting list in the index
		start_time = time.time();
		#master_dict = collections.OrderedDict(sorted(self.master_dict.values()))
		master_dict = self.master_dict
		master_dict = collections.OrderedDict(sorted(self.master_dict.items()))
		for words in master_dict.keys():
			print(words, master_dict.get(words))
		print("Fetched term dictionary in:", (time.time() - start_time))

	def print_doc_list(self):
	# function to print the documents and their document id
		start_time = time.time();
		document_dict = self.document_dict
		for doc in document_dict.keys():
			print(doc, document_dict.get(doc))

		print("Fetched document index in:", (time.time() - start_time))

#Local path
path = 'D:/Information Retreival/Assignment-1/collection'
obj = index(path)

#to execute

obj.buildIndex()
obj.print_dict()
obj.print_doc_list()

query = ['ask' , 'where' , 'location' , 'capital' , 'but']

obj.and_query(query)





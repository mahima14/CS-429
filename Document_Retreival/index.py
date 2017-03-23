# Python 3.0
from __future__ import division
import math
import re
import os
import collections
import time
import operator
import random


# import other modules as needed
class index:

    # function to read documents from collection, tokenize and build the index with tokens
    # implement additional functionality to support methods 1 - 4
    # use unique document integer IDs
    def __init__(self, path, stop_word_path):
        self.path = path
        self.stop_word_path = stop_word_path



        # function to read documents from collection, tokenize and build the index with tokens
        # implement additional functionality to support methods 1 - 4
        # use unique document integer IDs
    def buildIndex(self):
        all_documents = dict()
        master_dict = collections.defaultdict(dict)
        self.document_dict = collections.defaultdict()
        doc_Ids = []
        stopListFile = open(os.path.join(self.stop_word_path, "stop-list.txt"), 'r')
        stopContent = stopListFile.read().lower()
        stopListFile.close()

        stopContent = re.sub('[^a-z\ \']+', " ", stopContent)
        stop_words_raw = list(stopContent.split())

        word_position_dict = dict()


        for file in os.listdir(path):
            if file.endswith(".txt"):
                doc_id = re.sub('[^\d+]', "", file)
                doc = "doc" + doc_id
                doc_Ids.append(doc)
                self.document_dict.__setitem__(doc, file)
                doc_tokenize = list()
                # to read specific file
                currentFile = open(os.path.join(path, file), 'r')
                content = currentFile.read().lower()
                currentFile.close()

                content = re.sub('[^a-z\ \']+', " ", content)
                words = list(content.split())
                i = 0
                # To store the positions of each word
                word_position_dict = collections.defaultdict(dict)
                for word in words:
                    temp_list = []
                    if not stop_words_raw.__contains__(word):

                        if word not in word_position_dict.keys():
                            word_position_dict.__setitem__(word, i)
                        else:
                            if word_position_dict.get(word) is None:
                                word_position_dict.__setitem__(word, i)
                            else:
                                temp_list.append(word_position_dict.get(word))
                                temp_list.append(i)
                                word_position_dict.__setitem__(word, temp_list)
                        doc_tokenize.append(word)
                        i += 1
                for word in word_position_dict.keys():
                    temp_dict = dict()
                    temp_dict[doc] = word_position_dict.get(word)

                    master_dict[word][doc] = temp_dict[doc]
                all_documents.__setitem__(doc, doc_tokenize)
        self.master_dict = master_dict
        self.all_documents = all_documents
        self.doc_Ids = doc_Ids

    #function to calculate term frequency respective to each document
    def term_frequency(term, tokenized_document):
        return tokenized_document.count(term)

    #function to calculate weighted term frequency respective to each document
    def weighted_term_frequency(self, term, tokenized_document):
        count = tokenized_document.count(term)
        if count == 0:
            return 0
        return 1 + math.log(count)

    #function to calculate the inverse document frequency values for each document term
    def inverse_document_frequencies(self, input):
        tokenized_documents = input.values()
        idf_values = {}
        all_tokens_set = set([item for sublist in tokenized_documents for item in sublist])
        for tkn in all_tokens_set:
            idf_values[tkn] = 1 + math.log(len(tokenized_documents) / len(self.master_dict.__getitem__(tkn)))
        return idf_values

    #function to calculate the inverse document frequency values for each query term
    def inverse_query_frequencies(self, input):
        tokenized_documents = input
        idf_values = {}
        all_tokens_set = set([item for item in tokenized_documents])
        for tkn in all_tokens_set:
            idf_values[tkn] = 1 + math.log(1 / 1)
        return idf_values

    #function to calculate the tf-idf for each document term
    def tfidf(self):
        wt_dict = collections.defaultdict(dict)
        tfidf_master_dict = collections.defaultdict(dict)
        tfidf_documents = collections.defaultdict(dict)
        tfidf_dict = collections.defaultdict(dict)


        tokenized_documents = self.all_documents
        idf = self.inverse_document_frequencies(self.all_documents)
        self.idf = idf
        for docId, document in tokenized_documents.items():
            for term in idf.keys():
                tf = self.weighted_term_frequency(term, document)
                doc_tfidf = tf * idf[term]
                sub_list = []
                t_list = []
                wt_dict[term][docId] = tf
                tfidf_dict[term][docId] = doc_tfidf
                t_list.append(wt_dict[term][docId])
                if (self.master_dict[term].__contains__(docId)):
                    sub_list.append(self.master_dict[term][docId])
                    t_list.append(sub_list)
                tfidf_documents[term][docId] = t_list
        self.tfidf_documents= tfidf_documents
        self.wt_dict = wt_dict
        self.tfidf_dict = tfidf_dict
        for term in idf.keys():
            t_list = list()
            t_list.append(idf[term])
            t_list.append(tfidf_documents[term])
            tfidf_master_dict[term] = t_list
        self.tfidf_master_dict = tfidf_master_dict
        print("Master dictionary of terms with their idf and tf idf values")
        print(tfidf_master_dict)

    #function to calculate the tf-idf value for each query term
    def tfidf_query(self,query):
        wt_query_dict = collections.defaultdict(dict)
        idf_query = self.inverse_query_frequencies(query)
        for term in idf_query.keys():
            tf = self.weighted_term_frequency(term, query)
            query_tfidf = tf * idf_query[term]
            wt_query_dict[term] = query_tfidf
        self.wt_query_dict = wt_query_dict
        self.idf_query = idf_query

    # function for exact top K retrieval (method 1)
    # Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score
    def exact_query(self, query_terms, k, tfidf_dict, docIds):
        cosine_similarty_dict = dict()
        cosine =0
        for docid in docIds:
            sum = 0
            sum_vector1 = 0
            sum_vector2 = 0
            for queryTerms in query_terms:
                vector1 = self.wt_query_dict.get(queryTerms)
                if(tfidf_dict[queryTerms].__contains__(docid)):
                    vector2 = tfidf_dict[queryTerms][docid]
                else:
                    vector2 = 0
                dot_product = float(vector1) * float(vector2)
                sum += dot_product
                sum_vector1 += sum_vector1 + vector1 ** 2
                sum_vector2 += vector2 ** 2

            magnitude = math.sqrt(sum_vector1) * math.sqrt(sum_vector2)
            if not magnitude:
                cosine =0
            else:
                cosine = sum / magnitude
            if not cosine == 0 :
                cosine_similarty_dict.__setitem__(docid, cosine)
        return dict(sorted(cosine_similarty_dict.items(), key=operator.itemgetter(1), reverse=True)[:k])

    # Method for cluster pruning
    # It itertively updating the cluster for every remaining documents
    def clusterPruning(self, docK, docN):
        cosine_similarty_dict = dict()
        cosine = 0
        sum = 0
        sum_vector1 = 0
        sum_vector2 = 0
        for terms in self.all_documents.get(docK):
            vector1 = self.tfidf_dict[terms][docK]
            if (self.tfidf_dict[terms].__contains__(docN)):
                vector2 = self.tfidf_dict[terms][docN]
            else:
                vector2 = 0
            dot_product = float(vector1) * float(vector2)
            sum += dot_product
            sum_vector1 += sum_vector1 + vector1 ** 2
            sum_vector2 += vector2 ** 2

        magnitude = math.sqrt(sum_vector1) * math.sqrt(sum_vector2)
        if not magnitude:
            cosine = 0
        else:
            cosine = sum / magnitude
        if not cosine == 0:
            if(self.cosine_map[docN].keys()):
                for key in self.cosine_map[docN].keys():
                    if cosine > self.cosine_map[docN][key]:
                        self.cosine_map[docN].pop(key)
                        self.cosine_map[docN][docK] = cosine
            else:
                self.cosine_map[docN][docK] = cosine



    # function for exact top K retrieval using champion list (method 2)
    # Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score
    def inexact_query_champion(self, query_terms, k):
        r = 25
        champion_dict = collections.defaultdict(dict)
        required_queries = dict(
            (query, self.tfidf_dict.get(query)) for query in query_terms if query in self.tfidf_dict)
        for term_dict in required_queries.keys():
            champion_dict[term_dict] = dict(
                sorted(required_queries[term_dict].items(), key=operator.itemgetter(1), reverse=True)[:r])

        print("Champion List Method:", self.exact_query(query_terms, k, champion_dict, self.doc_Ids))

        # function for exact top K retrieval using index elimination (method 3)
        # Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score

    def inexact_query_index_elimination(self, query_terms, k):
        query_size = len(query_terms)
        required_queries_size = round(math.floor(query_size/2))
        required_queries = dict((query, self.idf.get(query)) for query in query_terms)
        for query in required_queries.keys():
            if(required_queries.get(query) == None):
                required_queries.__setitem__(query, 0)
        high_idf_terms = dict(sorted(required_queries.items(), key=operator.itemgetter(1), reverse=True)[:required_queries_size])
        if k < required_queries_size:
            k = required_queries_size
        print(k)
        print("Index Elimination" , self.exact_query(high_idf_terms,k, self.tfidf_dict, self.doc_Ids))



    # function for exact top K retrieval using cluster pruning (method 4)
    # Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score
    def inexact_query_cluster_pruning(self, query_terms, k):
        sizeOfkMeans = round(math.sqrt(len(self.all_documents)))
        doc_Ids = self.doc_Ids
        self.cosine_map = collections.defaultdict(dict)
        self.cluster_map = collections.defaultdict(dict)
        rand_item = list(random.sample(self.doc_Ids, sizeOfkMeans))
        for values in rand_item:
            doc_Ids.remove(values)
        for doc in rand_item:
            for docs in doc_Ids:
                self.clusterPruning(doc, docs)
        #Cluster Formation
        for doc_N in doc_Ids:
            for doc_K in rand_item:
                if self.cosine_map[doc_N].__contains__(doc_K):
                    self.cluster_map[doc_K][doc_N] = self.cosine_map[doc_N][doc_K]
        output_cluster = self.exact_query(query_terms,1, self.tfidf_dict, rand_item)
        value = str(output_cluster.keys())
        value_list = []
        value_list.append(value)
        if self.cluster_map.__contains__(value):
            value = self.cluster_map[value].keys()
            value_list.append(value)
        print("Cluster Pruning Method:", self.exact_query(query_terms,k, self.tfidf_dict, value_list))

    # function to print the terms and posting list in the index
    def print_dict(self):

        start_time = time.time();
        master_dict = collections.OrderedDict(sorted(self.master_dict.items()))
        for words in master_dict.keys():
            print(words, master_dict.get(words))

        print("Fetched term dictionary in:", (time.time() - start_time))

    # function to print the documents and their document id
    def print_doc_list(self):
        start_time = time.time();
        document_dict = self.document_dict
        for doc in document_dict.keys():
            print(doc, document_dict.get(doc))

        print("Fetched document index in:", (time.time() - start_time))


# Local path
path = 'D:/Information Retreival/Assignment-1/collection'
stop_word_path = 'D:/Information Retreival/Assignment-2/attachments'
obj = index(path,stop_word_path)



# to execute

obj.buildIndex()
print("#####################################")
print()
print("Master dictionary for terms with their posting list:")
obj.print_dict()
print("#####################################")
print()

print("Document List:")
obj.print_doc_list()
print("#####################################")
print()

start_time = time.time()
obj.tfidf()
print("Built tf-idf index for all terms in:", (time.time() - start_time))

k = int(input("Enter the value of k: "))

num_Query = int(input("Enter the number of queries to be executed: "))

n =1
while n <= num_Query:
    input_q = input("Enter query separated by comma in small letters: ")

    query = input_q.split(',')
    obj.tfidf_query(query)
    print("#####################################")
    print()
    start_time = time.time();
    print("Exact Query Method:", obj.exact_query(query,k, obj.tfidf_dict, obj.doc_Ids))
    print("Executed Exact Query Method in:", (time.time() - start_time))

    print("#####################################")
    print()
    start_time = time.time();
    obj.inexact_query_champion(query, k)
    print("Executed Champion List Method in:", (time.time() - start_time))


    print("#####################################")
    print()
    start_time = time.time();
    obj.inexact_query_index_elimination(query, k)
    print("Executed Index Elimination Method in:", (time.time() - start_time))

    print("#####################################")
    print()
    start_time = time.time();
    obj.inexact_query_cluster_pruning(query, k)
    print("Executed Cluster Pruning Method in:", (time.time() - start_time))

    print("#####################################")
    print()
    n += 1


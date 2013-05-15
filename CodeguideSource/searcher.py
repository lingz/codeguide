#!/usr/bin/python
#Codeguide.com searcher
#Written by Lingliang Zhang

#Type - Main / server-side Class to be called & executed from main script

import re
from whoosh.lang.porter import stem
from tree_builder import query_tree
from whoosh.filedb.filestore import FileStorage
from whoosh.lang.wordnet import Thesaurus
from r3tree import R3tree
#remove for release
import pickle

class Searcher(object):
    def __init__(self, language, version, lexicon, thesaurus, SQL, extended=1):
        self.__lexicon = lexicon
        self.__version = version
        self.__language = language
        self.__thesaurus = thesaurus
        self.__tree = R3tree("query")
        self.__SQL = SQL
        
    def get_SQL(self):
        return self.__SQL
        
    def get_lexicon(self):
        return self.__lexicon
    
    def get_thesaurus(self):
        return self.__thesaurus
    
    def add_child_to_tree(self, child):
        self.__tree.add_child(child)
        
    def get_version(self):
        return self.__version
    
    def get_tree(self):
        return self.__tree
    
    #returns a pure list of ranked id's
    @staticmethod
    def compute_tree(query_tree, max_results=20):
        query_results = query_tree.score()
        ids = []
        for key in query_results:
            ids.append(query_results[key])
        ids.sort(key=lambda tup: tup[1])
        ids.reverse()
        stripped_ranked_ids = []
        if len(ids) <= max_results:
            num_results = len(ids)
        else:
            num_results = max_results
        for i in range(num_results):
            stripped_ranked_ids.append(ids[i][0])
        return stripped_ranked_ids

   
    
    def search(self, query):
        #strips a query and returns a list of words without punctuation
        query = re.sub(r"[\W_]+", " ", query).split()
        #operates on each individual search term
        #print ("the query is:")
        #print(query)
        for word in query:
            if word:
                word = stem(word)
                #print("trying to form a tree from the word: %s"%word)
                #builds a new query tree from the word
                new_tree = query_tree(self, word)
                #if the query tree function didn't return none (has 1 or more children), adds it to the main tree
                if new_tree:
                    #print("tree %s successfully formed and added, children are:"%word)
                    #print(new_tree)
                    self.add_child_to_tree(new_tree)
                else:
                    pass
                    #print("tree %s returns no results"%word)
        #print(self.get_tree())
        if self.get_tree().get_all_children():
            return self.compute_tree(self.get_tree())
        else: 
            return None    
                    
                
    
if __name__ == '__main__':
    #load the thesaurus from memory
    thesaurus_path = r"E:\\codeguidedatadump\\whooshThesaurus"
    thesaurus = Thesaurus.from_storage(FileStorage(thesaurus_path))
    with open(r"E:\codeguidedatadump\SQLglobalLexicon.lexicon", "rb") as f:
        lexicon = pickle.load(f)
    searcher = Searcher("python", "3.2", lexicon["3.2"], thesaurus)
    print(searcher.search("list.append()"))
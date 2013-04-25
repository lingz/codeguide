#Indexer Class
#Written for codeguide.com
#Written by Lingliang Zhang

#Type - main

#given a directory and a whoosh DB directory, builds search trees
#for the given database

#written for Python 3

import os
import os.path
import tree_builder
import pickle
from whoosh.qparser import MultifieldParser
import whoosh.index

class Indexer(object):
    
    #the complete lexicon, containing the lexicon's for each indexed version
    global_lexicon = {}
    #the complete SQL library, containing all necessary information to build the SQL 
    global_SQL = {}
    
    def __init__(self, directory):
        self.__version = ("%r"%directory)[1:-1].split("\\")[-1]
        self.__SQLoutput = {}
        self.__trees = []
        self.__whooshIndex = whoosh.index.open_dir(directory)
        self.__whooshQueryParser = MultifieldParser(["header", "body"], self.__whooshIndex.schema)
        with self.__whooshIndex.searcher() as searcher: self.__lexicon = list(set(searcher.lexicon("body")).union(set(searcher.lexicon("header"))))
        
    def add_tree(self, search_term, tree):
        self.__trees.append((search_term, tree))
        
    def get_trees(self):
        return self.__trees
    
    def get_query_parser(self):
        return self.__whooshQueryParser
    
    def get_index(self):
        return self.__whooshIndex
    
    def get_version(self):
        return self.__version
    
    def get_SQLoutput(self):
        return self.__SQLoutput
    
    def get_lexicon(self):
        return self.__lexicon
    
    #crawls a directory, instantiating instances of itself in all subdirectories which should all be
    #Whoosh Db's
    @staticmethod
    def index_all(directory, max_depth = 20):
        #builds a list of immediate subdirectories
        to_build_list = [local_directory[0] for local_directory in os.walk(directory)][1:]
        for whoosh_directory in to_build_list:
            indexer = Indexer(whoosh_directory)
            indexer.build_index()
        with open(r"E:\codeguidedatadump\SQLsearchTreeIndex.trees", "wb") as file:
            pickle.dump(Indexer.global_SQL, file, protocol=2)
        with open(r"E:\codeguidedatadump\SQLglobalLexicon.lexicon", "wb") as file:
            pickle.dump(Indexer.global_lexicon, file, protocol=2)
        
    
    #crawls a directory, building trees from Whoosh DB's in the immediate subdirectories 
    def build_index(self, max_depth=20):
        print("indexing lexicon of length %d" % len(self.get_lexicon()))
        #add local lexicon to global lexicon
        Indexer.global_lexicon[self.get_version()] = []
        #initilize the searcher object
        with self.get_index().searcher() as searcher:
            for search_term in self.get_lexicon():
                query = self.get_query_parser().parse(str(search_term))
                #search the index with the query and return the results
                results = searcher.search(query, limit=max_depth)
                #build a tree using the results object
                if results.scored_length() > 0:
                    print("search term %s found %d results" %(search_term, results.scored_length()))
                    self.add_tree(search_term, tree_builder.search_tree(search_term, results))
                    Indexer.global_lexicon[self.get_version()].append(search_term)
                else:
                    print("search term %s found no scored results, (but found %d results total)" %(search_term, len(results)))
                
        Indexer.global_SQL[self.get_version()] = self.get_trees()
                

if __name__ == '__main__':
    import time
    start_time = time.clock()
    Indexer.index_all(r"E:\Skydrive\EclipseWorkspace\CodeguideDBScripts\data\python\whooshDB")
    print("Total time to run was %d seconds"%(time.clock()-start_time))
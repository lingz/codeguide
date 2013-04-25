#!/usr/bin/python
#Tree Builder Module
#Written for codeguide.com
#By Lingliang Zhang

#Type - Utility Module

#Nb. search -> pre-indexed term existing in the database lexicon
#query -> live, generated query 

from r3tree import R3tree
from whoosh.qparser import MultifieldParser
from whoosh.lang.porter import stem
import pickle

#validates the query to see if it or any of its synonyms exist
def query_check(query, thesaurus):
    synonym_list = thesaurus.synonyms(query)
    synonym_list.append(query)
    result = False
    for synonym in synonym_list:
        if tree_exists(synonym):
            result = True
            break
    return result
    
#creates a query tree, involving all synonyms of a query
#this function is run live for every possible search term
def query_tree(searcher, query):
    #print("creating query tree %s" % (query))
    new_tree = R3tree(query)
    
    try:
        synonym_list = searcher.get_thesaurus().synonyms(query)
    except:
        synonym_list = []
    stemmed_synonym_list = [stem(word) for word in synonym_list]
    for synonym in stemmed_synonym_list:
        if synonym in searcher.get_lexicon() and synonym != query: 
            #print("Adding child %s to tree %s" % (synonym, query))
            #print(fetch_tree(synonym, searcher.get_version()))
            new_tree.add_child(fetch_tree(synonym, searcher))
    if new_tree.get_all_children():
        main_boost = len(new_tree.get_all_children())+1
    else:
        main_boost = 1
    if query in searcher.get_lexicon(): 
        #print("Main query %s found. Adding as favorite to tree" % (query))
        new_tree.add_child(fetch_tree(query, searcher), main_boost)
    if new_tree.get_all_children() != None:
        return new_tree
    else:
        return None
    
#creates a search tree, involving all search results from that term
def search_tree(search_term, results):
    #the max number of children in the tree
    new_tree = R3tree(search_term)
    for i in range(results.scored_length()):
        new_tree.add_child(results[i]["id"], results.score(i))
    return new_tree
    
#fetches a search tree from the SQL database
def fetch_tree(search_term, searcher):
    version = searcher.get_version()
#    return searcher.get_SQL().tree_pull(version, search_term)
    #temp code for offline testing
    with open("/home/lz781/public_html/cgi-bin/SQLsearchTreeIndex_old.sql", "rb") as f:
        SQL_db = pickle.load(f)
        for entry in SQL_db["3.2"]:
            if entry[0] == search_term:
                return entry[1]
                
        

if __name__ == '__main__':
    pass
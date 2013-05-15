#!/usr/bin/python

#Codeguide main executable
#Written by Lingliang Zhang and Moiri

#Type - Main (executable)

print "Content-Type: text/html"
print
#print "hello world"
import sys
sys.path.append("/home/lz781/lib")
from searcher import Searcher
from results import Results
import cgi
from whoosh.lang.wordnet import Thesaurus
from whoosh.filedb.filestore import FileStorage
import SQL_builder
#remove on release
import pickle
#print "hello world8"

if __name__ == '__main__':
    #START ONLINE SEGMENT
    form = cgi.FieldStorage()
    query = form.getvalue("query")
    language = form.getvalue("language")
    version = form.getvalue("version")
    expandable = form.getvalue("expandable")
    thesaurus_path = r"/home/lz781/public_html/cgi-bin/whooshThesaurus"
    #FOR TESTING
    #query="list.append()"
    #language="python"
    #version="3.2"
    #expandable=1
    #END TEST
    thesaurus = Thesaurus.from_storage(FileStorage(thesaurus_path))
    SQL_builder = SQL_builder.SQLBuilder(language)
    lexicon = SQL_builder.lexicon_pull(version)
#    with open(r"/home/lz781/public_html/cgi-bin/SQLglobalLexicon_old.sql", "rb") as f:
#        lexicon = pickle.load(f)
#    print "hello world14"
#    END ONLINE SEGMENT
#    START OFFLINE TESTING SEGMENT
    
#    thesaurus_path = r"E:\\codeguidedatadump\\whooshThesaurus"
#    thesaurus = Thesaurus.from_storage(FileStorage(thesaurus_path))
#    with open(r"E:\codeguidedatadump\SQLglobalLexicon.lexicon", "rb") as f:
#        lexicon = pickle.load(f)
    #END OFFLINE TESTING SEGMENT
    searcher = Searcher(language, version, lexicon, thesaurus, SQL_builder)
#    print "hello world15"
    results = Results(language, version)
#    print "hello world16"
    #output results onto web page
#    print"hello world20"
    print(results.parse_list(searcher.search(query)))
#    print("helloworld17")
    
    
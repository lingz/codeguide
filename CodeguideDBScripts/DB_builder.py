#DB Builder
#Written for codeguide.com
#Written by Lingliang Zhang & Moiri Gambioni

#type - main module - to be executed

#Builds local pickled dictionaries to be transcribed onto SQL databases
#and also whoosh databases.

import os
import os.path
import pickle
import glob
from method_entry import Method_entry
from whoosh import index
from whoosh.fields import Schema, TEXT, STORED
from whoosh.analysis import StemmingAnalyzer

class DB_builder(object):
    
    def __init__(self):
        pass
        
    #takes a directory name and scans it, building relevant whoosh DB's
    def build_whoosh_db(self, dir_name, target=r"C:\Users\Administrator\Desktop\Group Project\whooshDB"):
        #for each version of the language being crawled
        for folder in [osdirectory[0] for osdirectory in os.walk(dir_name)][1:]:
            #build the schema
            schema = Schema(id=TEXT(stored=True), 
                            header=TEXT(field_boost=10.0, analyzer=StemmingAnalyzer()),
                            body=TEXT(analyzer=StemmingAnalyzer()))
            #save the index in the target directory, under the correct filename
            version_name = folder.split("\\")[-1]
            index_dir = os.path.join(target, version_name)
            #create the directory if it does not already exist
            if not os.path.exists(index_dir):
                os.mkdir(index_dir)
            whoosh_index = index.create_in(index_dir, schema)
            #initilize the index writer
            writer = whoosh_index.writer()
            #open each version of the method dump
            for file_name in glob.glob(r"%s\\*.method"%(folder)):
                with open(file_name, 'rb') as w:
                    method_list = pickle.load(w)
                    for method in method_list:
                        #add the method information to the WhooshDB
                        writer.add_document(id=str(method.get_id()), 
                                            header=str(method.get_header()),
                                            body=str(method.get_body_text()))
            writer.commit()
        
    def build_sql_db(self, dir_name, target=r'C:/Users/Administrator/Desktop/Group Project/sql.pickle'):
        '''Builds a pickled dictionary containing id, syntax and html description of methods (for enventual creation of SQL tables)'''
        self.__sql_dict = {}
        for folder in [osdirectory[0] for osdirectory in os.walk(dir_name)][1:]:
            for file_name in glob.glob(r"%s\\*.method"%(folder)):
                with open(file_name, 'rb') as w:
                    method_list = pickle.load(w)
                    for method in method_list:
                        if method.get_version() in self.__sql_dict:
                            self.__sql_dict[method.get_version()].append((method.get_id(),method.get_syntax(),method.get_body_html()))
                        else:
                            self.__sql_dict[method.get_version()] = [(method.get_id(),method.get_syntax(),method.get_body_html())]
        pickle.dump(self.__sql_dict, open(target, 'wb'))

        
    def read_methods(self, dir_name):
    '''Test function to print information about methods'''
        for folder in [osdirectory[0] for osdirectory in os.walk(dir_name)][1:]:
            for file_name in glob.glob(r"%s\\*.method"%(folder)):
                with open(file_name, 'rb') as w:
                    method_list = pickle.load(w)
                    for method in method_list:
                        try:
                            print(method.get_body_text(), method.get_header())
                        except:
                            print("Error")
    
    #Crawls a dumped version directory (note it doesn't crawl diretories) until the ID is found
    @staticmethod
    def find_id(id, dir_name):
        for file_name in glob.glob(r"%s\\*.method"%(dir_name)):
            with open(file_name, 'rb') as w:
                    method_list = pickle.load(w)
                    for method in method_list:
                        if method.get_id() == id:
                            print ("found id: %s, \n\
                                    method source: %s \n\
                                    method name: %s \n\
                                    method body: %s"%(method.get_id(), method.get_source(), method.get_header(), method.get_body_text()))
    #Crawls a dumped version directory (note it doesn't crawl diretories) until the function name is found
    @staticmethod
    def find_name(name, dir_name):
        for file_name in glob.glob(r"%s\\*.method"%(dir_name)):
            with open(file_name, 'rb') as w:
                    method_list = pickle.load(w)
                    for method in method_list:
                        if name in method.get_header():
                            print ("found id: %s, \n\
                                    method source: %s \n\
                                    method name: %s \n\
                                    method body: %s"%(method.get_id(), method.get_source(), method.get_header(), method.get_body_text()))
    #Crawls a dumped version directory (note it doesn't crawl diretories) until the url is found
    @staticmethod
    def find_source(url, dir_name):
        for file_name in glob.glob(r"%s\\*.method"%(dir_name)):
            with open(file_name, 'rb') as w:
                    method_list = pickle.load(w)
                    for method in method_list:
                        if url in method.get_source():
                            print ("found id: %s, \n\
                                    method source: %s \n\
                                    method name: %s \n\
                                    method body: %s"%(method.get_id(), method.get_source(), method.get_header(), method.get_body_text()))

    
if __name__ == "__main__":
    builder = DB_builder()
    #builder.build_sql_db(r"C:\Users\Administrator\Desktop\Group Project\method_dump")
    #builder.read_methods(r"C:\Users\Administrator\Desktop\Group Project\method_dump")
    #builder.build_whoosh_db(r"C:\Users\Administrator\Desktop\Group Project\method_dump")
    #builder.find_id(15670, r"C:\\Users\\Administrator\\Desktop\\Group Project\\method_dump\\3.2")
    #builder.find_name("append", r"C:\\Users\\Administrator\\Desktop\\Group Project\\method_dump\\3.2")
    builder.find_source("http://docs.python.org/2/tutorial/datastructures.html", r"C:\\Users\\Administrator\\Desktop\\Group Project\\method_dump\\3.2")
#!/usr/bin/python3.2
#Simple SQL builder from pickled objects
#written for codeguide.com
#By Moiri Gamboni and Lingliang Zhang


import MySQLdb as mdb
import sys
import cPickle as pickle

class SQLBuilder():        

    def unpack_lexicon(self, target):
        '''Converts lexicon dump file into an SQL table for each version containing a single entry a pickled list'''
        with open(target, "rb") as f:
            lexicon_dictionary = pickle.load(f)
            for version in lexicon_dictionary:
                data = pickle.dumps(lexicon_dictionary[version])
                version = version.replace('.','')
                table_name = "%s_lexicon_%s"%(self.get_language(), version)
                self.get_cursor().execute("DROP TABLE IF EXISTS %s"%(table_name))
                self.get_cursor().execute("CREATE TABLE IF NOT EXISTS %s(lexicon MEDIUMBLOB)"%(table_name))
                arg = "INSERT INTO " + table_name +  '(lexicon) VALUES(%s)'
                self.get_cursor().execute(arg, (data,))
                
    def lexicon_pull(self, version):
        '''Returns a list of possible search terms'''
        version = version.replace('.','')
        self.get_cursor().execute("SELECT * FROM \
                %s_lexicon_%s"%(self.get_language(),version))
        data = self.get_cursor().fetchone()[0]
        return pickle.loads(data)

    def method_pull(self, version, id):
        '''Returns a tuple countaining the method syntax and html description depending on the method id'''
        version = version.replace('.','')
        self.get_cursor().execute("SELECT syntax, html FROM \
                %s_method_%s WHERE id=%s"%(self.get_language(),version,id))
        data = self.get_cursor().fetchone()
        return data[0], data[1]

    def tree_pull(self, version, query):
        '''Returns a R3Tree object depending on a query'''
        version = version.replace('.','')
        self.get_cursor().execute("SELECT tree FROM \
                %s_tree_%s WHERE query='%s'"%(self.get_language(),version,query))
        data = self.get_cursor().fetchone()
        return pickle.loads(data[0])

    def unpack_method_dir(self, target):
        '''Converts a method dump file into an SQL table for each version with each row containing one method (id, syntax and html desrciption)'''
        with open(target, "rb") as f:
            method_dictionary = pickle.load(f)       
            for version,tuple_list in method_dictionary.items():
                version = version.replace('.','')
                table_name = "%s_method_%s"%(self.get_language(), version)
                arg = "INSERT INTO " + table_name +  ' VALUES(%s, %s, %s)'
                self.get_cursor().execute("DROP TABLE IF EXISTS %s"%(table_name))
                self.get_cursor().execute("CREATE TABLE IF NOT EXISTS %s(id INT, syntax BLOB, html MEDIUMBLOB)"%(table_name))
                for tuple in tuple_list:
                    data = (tuple[0],pickle.dumps(tuple[1]),pickle.dumps(tuple[2]))
                    self.get_cursor().execute(arg, (data[0],data[1],data[2],))
    
    def unpack_search_trees(self, target):
        '''Converts tree dump file into an SQL table for each version containing an R3Tree object for each possible query'''
        with open(target, "rb") as f:
            trees_dictionary = pickle.load(f)       
            for version,tuple_list in trees_dictionary.items():
                version = version.replace('.','')
                table_name = "%s_tree_%s"%(self.get_language(), version)
                arg = "INSERT INTO " + table_name +  ' VALUES(%s, %s)'
                self.get_cursor().execute("DROP TABLE IF EXISTS %s"%(table_name))
                self.get_cursor().execute("CREATE TABLE IF NOT EXISTS %s(query TINYBLOB, tree BLOB)"%(table_name))
                for tuple in tuple_list:
                    data = (tuple[0],pickle.dumps(tuple[1]))
                    self.get_cursor().execute(arg, (data[0],data[1],))

    def __init__(self, language):
        self.__con = mdb.connect('localhost', 'lz781', 'B8A2ip8lnq', 'lz781')
        self.__cur = self.__con.cursor()
        self.__language = language
        
    def get_cursor(self):
        return self.__cur
    
    def get_con(self):
        return self.__con
            
    def get_language(self):
        return self.__language
        
if __name__ == '__main__':
    new_builder = SQLBuilder("python")
    #new_builder.unpack_lexicon("/home/lz781/scripts/SQLglobalLexicon_old.sql")
    #new_builder.unpack_search_trees("/home/lz781/scripts/SQLsearchTreeIndex_old.sql")
    #new_builder.unpack_method_dir("/home/lz781/scripts/SQLmethodDirectory_old.sql")
    print(new_builder.lexicon_pull('3.2'))

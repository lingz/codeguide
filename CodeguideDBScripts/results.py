#!/usr/bin/python
#Results class
#Written for codeguide.com
#Written by Lingliang Zhang

#Type - Main

#receives a list of id's and parses them, returning the necessary output for the page.
import pickle
from SQL_builder import SQLBuilder

class Results(object):

    def __init__(self, language, version, extension=1):
        self.__output = []
        self.__language = language
        self.__version = version
        self.__extension = extension
        self.__result_no = 0
        with open(r"/home/lz781/public_html/cgi-bin/SQLmethodDirectory_old.sql", "rb") as f:
            directory = pickle.load(f)
            self.__SQL_method_directory = directory[self.__version]
    
    
    def increment_output(self):
        self.__result_no += 1
    
    def parse_result(self, method):
        self.increment_output()
        self.__output.append("<div id='cr%d'><div id='hr%d'>%s</div> <div id='rr%d'>%s</div></div>" \
        %(self.__result_no, self.__result_no, method[1], self.__result_no, method[2]))
        
    
    def parse_list(self, id_list):
        for id in id_list:
            self.parse_result(self.fetch_method(int(id)))
        return ''.join(self.__output)
    
    
    def fetch_method(self, id):
        method_directory = self.__SQL_method_directory
        for method in method_directory:
            if method[0] == id:
                return method
    
    def fetch_method2(self, id):
        SQL_builder2 = SQLBuilder("python")
        return SQL_builder2.method_pull(self.__version, id)
        

if __name__ == "__main__":
    results = Results("python", "3.2")
    print(results.parse_list([15104, 12372, 16368]))        
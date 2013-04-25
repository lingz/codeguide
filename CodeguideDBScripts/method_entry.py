#Method entry data structure
#Written for codeguide.com
#Written by Moiri

#Type - data structure

import re

class Method_entry():

'''Method object used to create dump files and other databases (from those files)'''
    
    id = 0
    
    def __init__(self, header, syntax, body_html, body_text, source, version):
        self.__header = header
        self.__syntax = syntax
        self.__body_html = body_html
        self.__body_text = body_text
        self.__source = source
        self.__version = version
        Method_entry.id += 1
        self.__id = Method_entry.id

    def __str__(self):
        return "%s\n"*7%(Method_entry.get_header(self),Method_entry.get_syntax(self),Method_entry.get_body_html(self),Method_entry.get_body_text(self),
                         Method_entry.get_source(self),Method_entry.get_version(self),Method_entry.get_id(self))

    def get_header(self):
        return self.__header

    def get_syntax(self):
        return self.__syntax

    def get_body_html(self):
        return self.__body_html

    def get_body_text(self):
        return self.__body_text

    def get_source(self):
        return self.__source

    def get_version(self):
        return self.__version

    def get_id(self):
        return self.__id

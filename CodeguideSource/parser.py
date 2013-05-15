#!/usr/bin/python3.2
#Parser class to process crawled pages and create pickled objects
#Written for codeguide.com
#Written by Moiri

import re
import pickle
import glob
import os
from page import Page
from method_entry import Method_entry
from bs4 import BeautifulSoup
import cProfile

class Counter(dict):
    def __missing__(self, key): return []

class Parser():

    def open_page_dumps(self, dir_name):
        '''Searches through a directory for any page dump files and processes them to create a method dump file'''

        self.__header_list = {}
        self.__method_dict = {}
        
        for file_name in glob.glob(dir_name):
            
            #Create dictionary entries and clear old dictionary
            self.__version = file_name.split('\\')[-2][:3]
            if self.__version not in self.__method_dict:                
                Parser.save_method_dict(self.__method_dict)
                self.__method_dict = {}
                self.__method_dict[self.__version] = {}
                print('added version', self.__version)
            
        #Process page dumps and save pickled dictionary
            with open(file_name, 'rb') as w:
                page_list = pickle.load(w)
                for page in page_list:
                    Parser.parse_bs4(self, page)
            print('finished dump', file_name)
        Parser.save_method_dict(self.__method_dict)
        
    def parse_bs4(self, page):
        '''Uses the data in the page object and parses it to add methods to a dictionary'''

        if 'doc' in page.get_source():soup = BeautifulSoup(page.get_html())
        else: return
        
        for tag in soup('dl', class_=re.compile("function|method")):
            for possible_name in tag.find_all('dt'):
                
                #Header extraction
                try:header = re.sub(r"[\W_]+", " ", possible_name['id'])
                except:return
                
                #Syntax extraction
                syntax = ''
                for string in possible_name.stripped_strings:
                    syntax += string
                if syntax.find('[') == 0: syntax = re.sub(r'[[].*?[]](.*?)', r'\1', syntax)
                syntax = syntax[:-1]
                
                #HTML Desrciption extraction
                body_html = tag.dd
                #Replacing link formatting
                for link in body_html.find_all('a'):
                    if link.get('title') != None:
                        link['href'] = 'javascript:void(0)'
                        link['onclick'] = 'internal_search(%s)'%link['title']
                        link.clear()
                        link.string = link['title'].split('.')[-1]+'()'
                    else:
                        link.name = 'span'
                        del link['class']
                        del link['href']
                #Removing unnecessary tags
                for tt in body_html.find_all('tt', class_='docutils literal'):
                    tt.name = 'span'
                    tt['class'] = 'pre'
                    tt.span.unwrap()
                
                #Plain text description extraction
                temp_body = body_html
                for highlight in body_html.find_all('div', class_=re.compile('highlight.')):
                    highlight['class'] = 'code'
                    del highlight['style']
                    try:
                        highlight.div.pre.unwrap()
                        highlight.div.unwrap()
                    except:highlight.pre.unwrap()
                
                while temp_body.find('div') != None:temp_body.div.decompose()
   
                body_text = ''
                for string in temp_body.strings:
                    body_text += string
    
                body_text = re.sub(r"[\W_]+", " ", body_text)
                
                #Adding method to dictionary
                if header in self.__method_dict[self.__version]:
                    if Parser.compare_version(self.__method_dict[self.__version][header].get_version(), page.get_version()):
                        self.__method_dict[self.__version][str(header)] = Method_entry(str(header), str(syntax), str(body_html), str(body_text), str(page.get_source()), str(page.get_version()))
                else:
                    self.__method_dict[self.__version][str(header)] = Method_entry(str(header), str(syntax), str(body_html), str(body_text), str(page.get_source()), str(page.get_version()))

    @staticmethod
    def save_method_dict(method_dict, target=r'C:\\Users\\Administrator\\Desktop\\Group Project\\method_dump'):
        '''Converts a method dictionary to a dump file'''

        for version in method_dict.keys():
            directory = os.path.join(target,version)
            savepath = os.path.join(directory,version +'.method')
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(savepath, "wb") as f:
                pickle.dump(method_dict[version],f)

    @staticmethod
    def compare_version(old, new):
        '''Compares version numbers of methods'''
        if len(old.split('.')) == 2: old += '.0'
        if len(new.split('.')) == 2: new += '.0'

        for idx, num in enumerate(old.split('.')):
            if new.split('.')[idx] > num: return 1
            elif new.split('.')[idx] < num: return 0
        return 0
        
if __name__ == '__main__':
    p = Parser()
    p.open_page_dumps(r"C:/Users/Administrator/Desktop/Group Project/python/*/*.dump")

#Page Class / datastructure for Codeguide
#Written by Lingliang Zhang

#Type - Class

import urllib.request
import re
from lang_parser import check_page_type

class Page(): #A class defining the datastructure of a webpage
    
    """
    The datastructure for a web-page in this crawler
    attributes:
    source - the url the page was made from
    html - the html content of the page
    language - the language the crawler was looking for
    version - what version language the documentation is describing
    is_dictionary - whether the page in question has a dictionary of functions/methods
    
    functions:
    """

    def __init__(self, url, language): #returns a string of the html of a url
        self.__source = url
        self.__html = urllib.request.urlopen(url).read().decode()
        self.__language = language
        print(check_page_type(self.get_html(), language, self.get_source()))
        self.__version, self.__is_dictionary = check_page_type(self.get_html(), language, self.get_source())
        
    def get_source(self):
        return self.__source

    def get_html(self):
        return self.__html
    
    def get_language(self):
        return self.__language
    
    def get_version(self):
        return self.__version
        
    def is_doc(self):
        return self.__is_dictionary
    
    def pull_links(self): #uses RegEx to pull all the links from a page
        output = re.findall(r'(href=\")([^\s\"]+)', self.__html)
        result = []
        while output:
            link = output.pop()[1]
            if "http://" not in link:
                if ".." in link:
                    link = link.lstrip("./")
                    link = "/".join(self.get_source().split("/")[:-2]) + "/" + link
                elif link[0] == "/":
                    link = link.lstrip("./")
                    link = "/".join(self.get_source().split("/")[0:3]) + "/" + link
                else:
                    link = "/".join(self.get_source().split("/")[:-1]) + "/" + link
            link = link.split("#")[0]
            result.append(link)
        return result

def main():
    page = Page("http://docs.python.org/2/contents.html", "python")
    print(page.is_dictionary())
    print(page.get_version())
    
if __name__ == "__main__":
    main()

#Web crawler for Codeguide.com
#Written by Lingliang Zhang
#For Python 3.2

#Type - Main - to be executed OFFLINE

import pickle
from page import Page
import os

#initiates the crawl
class Crawler(object):
    """
    Crawler class. Initiate it and then run the .crawl() function to generate page
    which can be parsed for the website.
    """
    def __init__(self, language, domain, crawl_depth, ):
        """
        Parameters:
        langage - the language being crawled
        domain - the domain it sticks to
        crawl_depth = crawl_depth #how deep into the tree diagram it will crawl
      
        """
        self.__crawl_history = set([]) #set of url's previously crawled
        self.__current_crawl = set([]) #set of pages in the current crawl
        self.__output = {}
        self.__save_state_count = {} #dictionary of outputs saved for each file version
        self.__crawl_depth = crawl_depth #how deep into the tree diagram it will crawl
        self.__domain = domain
        
    def crawl(self, seed):
        """
        main crawl function. Takes the seed URL and begings crawling
        """
        
        self.__crawl_history = set([]) #set of url's previously crawled
        self.__current_crawl = set([Page(seed, self.__language)]) #set of pages in the current crawl
        self.__output = {}
        self.__save_state_count = {} #dictionary of outputs saved for each file version
        for i in range(0,self.__crawl_depth+1):
            #set of pages for the next crawl
            self.__next_crawl = set([]) 
            
            #crawls each page in current_crawl
            for page in self.__current_crawl:
                #let the console know what is being crawled
                print("crawling %s" % (page.get_source()))
                
                print("adding %s to crawl history" % (page.get_source()))
                #add this page to the history of crawled pages
                self.__crawl_history.add(page.get_source())
                
                #parses all the links on the page
                if i != self.__crawl_depth:
                    try:
                        print("parsing links on page")
                        print(page.pull_links())
                    except:
                        print("passing link pulling error")
                    for link in page.pull_links():
                        if link not in self.__crawl_history and self.__domain in link: 
                            self.__next_crawl.add(link)
                            print("adding link %s to the next level crawl" %(link))
                    
                
                #saves the page in memory
                if page.is_doc() == True:
                    if page.get_version() in self.__output: #have crawled this version of doc before
                        print("saving page %s in memory" %(page.get_source()))
                        self.__output[page.get_version()].append(page)
                        if len(self.__output[page.get_version()]) == 10:
                            if page.get_version() in self.__save_state_count:
                                self.__save_state_count[page.get_version()] += 1
                            else:
                                self.__save_state_count[page.get_version()] = 1
                            print("dumping number %d of version: %s" %(self.__save_state_count[page.get_version()], page.get_version()))
                            self.dump(self.__output[page.get_version()], self.__language, page.get_version(), self.__save_state_count[page.get_version()])
                            print("clearing memory")
                            print("crawled %d links so far" %(len(self.__crawl_history)))
                            self.__output[page.get_version()] = []
                            
                    else:
                        print("creating entry %s  \n saving page" % (page.get_version())) 
                        self.__output[page.get_version()] = [page] #first time crawling this version of doc
                
            #updates the current crawl to the next one
            print("crawl level %d complete, starting next crawl" % i)
            self.__current_crawl = self.url_to_pages(self.__next_crawl, self.__language)
            print(self.__current_crawl)
            
        for version in self.__output:
            if version in self.__save_state_count:
                num = self.__save_state_count[version] + 1
            else:
                num = 1
            self.dump(self.__output[version], self.__language, version, num)
            
    
    
    #dumps the object into a file
    def dump(self, object_save, language, version, num):
        directory = "%s\\%s\\%s\\" % ("C:\\Users\\NYUAD\\Desktop\\Ling_Crawl2", language, version)
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = directory + str(num) +".dump"
        print(file_path)
        
        with open(file_path, "wb") as file:
            pickle.dump(object_save, file)
    
    #converts a set of url's to a set of pages
    def url_to_pages(self, input_set, language):
        output_list = set([])
        for url in input_set:
            print("pulling %s to memory" % url)
            try:
                output_list.add(Page(url, language))
            except:
                print("Error: cannot decode %s" % url)
        return output_list
    
if __name__ == '__main__':
    crawler = Crawler("python_package", "python.org", 7)
    crawler.crawl("http://pypi.python.org/pypi?%3Aaction=index", )

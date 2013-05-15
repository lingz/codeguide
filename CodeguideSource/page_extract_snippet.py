#data extraction 

import pickle

#Change this file_name to whatever file you want to open
file_name = "3.2/1.dump"

with open(file_name, 'rb') as w:
    list_object = pickle.load(w)
    for page in list_object:
        source_url = page.get_source()
        version = page.get_version()
        html = page.get_html()
        print(source_url,version,html)

        

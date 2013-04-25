#Language Parser for Codeguide
#Written by Lingliang Zhang

import re


def check_page_type(html, language, url): 
    """
    for the Page class - checks if a page is documentation 
and the version of the documentation. Returns a tuple containing
1. the version number if it is a documentation page, or returns None otherwise
2. the is_dictionary as a boolean, giving whether or not the page
has a functions/method dictionary and needs to be parsed    
    """
    if language == "python":
        info = re.search(r"(VERSION:\s+\')([^\']+)", html)
        is_dictionary = False
        right_url = False
        if info: 
            while True:
                has_methods = re.search(r'class="method"', html)
                if has_methods: is_dictionary = True; break
                has_functions = re.search('class="function"', html)
                if has_functions: is_dictionary = True; break
                has_exceptions = re.search('class="exception"', html)
                if has_exceptions: is_dictionary = True; break
                has_class = re.search('class="class"', html)
                if has_class: is_dictionary = True;
                break
            if is_dictionary:
                if "docs.python.org" in url:
                    right_url = True
                
            return info.group(2), is_dictionary and right_url
        else: return (None, False)

    if language == "python_package":
        info = re.search(r"(VERSION:\s+\')([^\']+)", html)
        is_dictionary = False
        right_url = False
        if info: 
            while True:
                has_methods = re.search(r'class="method"', html)
                if has_methods: is_dictionary = True; break
                has_functions = re.search('class="function"', html)
                if has_functions: is_dictionary = True; break
                has_exceptions = re.search('class="exception"', html)
                if has_exceptions: is_dictionary = True; break
                has_class = re.search('class="class"', html)
                if has_class: is_dictionary = True;
                break
            if is_dictionary:
                if "packages.python.org" in url:
                    right_url = True
                
            return info.group(2), is_dictionary and right_url
        else: return (None, False)
        
        

#!/usr/bin/python

class Database(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.__pythonIndex = {"list.append(x)": "Add an item to the end of the list; equivalent to a[len(a):] = [x].", \
                            "list.extend(L)": "Extend the list by appending all the items in the given list; equivalent to a[len(a):] = L.", \
                            "list.insert(i, x)": "Insert an item at a given position. The first argument is the index of the element before which to insert, so a.insert(0, x) inserts at the front of the list, and a.insert(len(a), x) is equivalent to a.append(x).",\
                            "list.remove(x)": "Remove the first item from the list whose value is x. It is an error if there is no such item.",\
                            "list.pop([i])": "Remove the item at the given position in the list, and return it. If no index is specified, a.pop() removes and returns the last item in the list. (The square brackets around the i in the method signature denote that the parameter is optional, not that you should type square brackets at that position. You will see this notation frequently in the Python Library Reference.)",\
                            "list.index(x)": "Return the index in the list of the first item whose value is x. It is an error if there is no such item.",\
                            "list.count(x)": "Return the number of times x appears in the list.",\
                            "list.sort()": "Sort the items of the list, in place.",\
                            "list.reverse()": "Reverse the elements of the list, in place."}
        self.__javaIndex ={"add(E e)": "Appends the specified element to the end of this list (optional operation).",\
                           "add(int index, E element)": "Inserts the specified element at the specified position in this list (optional operation).",\
                           "addAll(Collection<? extends E> c)": "Appends all of the elements in the specified collection to the end of this list, in the order that they are returned by the specified collection's iterator (optional operation).",\
                           "addAll(int index, Collection<? extends E> c)": "Inserts all of the elements in the specified collection into this list at the specified position (optional operation).",\
                           "clear()": "Removes all of the elements from this list (optional operation).",\
                           "contains(Object o)": " Returns true if this list contains the specified element.",\
                           "containsAll(Collection<?> c)": "Returns true if this list contains all of the elements of the specified collection.",\
                           "equals(Object o)": "Compares the specified object with this list for equality."
                           }
        self.__htmlIndex ={"HTML Unordered Lists":"An unordered list starts with the &lt;ul&gt; tag. Each list item starts with the &lt;li&gt; tag. The list items are marked with bullets (typically small black circles).",\
                           "HTML Definition Lists":"A definition list is a list of items, with a description of each item.The &lt;dl&gt; tag defines a definition list.The &lt;dl&gt; tag is used in conjunction with &lt;dt&gt; (defines the item in the list) and &lt;dd&gt; (describes the item in the list):"
                }
        self.__cssIndex = {"armenian" : "The marker is traditional Armenian numbering",\
                           "circle" : "The marker is a circle",\
                           "cjk-ideographic" : "The marker is plain ideographic numbers",\
                           "decimal": "The marker is a number. This is default for <ol>",\
                           "decimal-leading-zero": "The marker is a number with leading zeros (01, 02, 03, etc.)",\
                           "disc": "The marker is a filled circle. This is default for <ul>"}
        
    def query(self, language):
        if language == "python":
            return self.__pythonIndex
        if language == "java":
            return self.__javaIndex
        if language == "html":
            return self.__htmlIndex
        if language == "css":
            return self.__cssIndex


    
    
    
    

if __name__ == '__main__':
    index = Database()
    print "Content-Type: text/html"
    print
    print index.query('python'), index.query('java'), index.query('html'), index.query('css')
    


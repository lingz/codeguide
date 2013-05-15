#!/usr/bin/python
#R3tree data structure
#Created for codeguide.com
#Created by Lingliang Zhang

#Type - Class

class R3tree(object):
    
    def __init__(self, name="null"):
        self.__name = name
        self.__tree = {}
    
    def __str__(self):
        result = "<R3tree: %s; Children: %d>\n" % (self.get_name(), len(self.get_tree()))
        for child in self.get_all_children():
            result += "%s%s\n"%(child, str(self.get_child(child)))
        return result
    
    def get_tree(self):
        return self.__tree
    
    def get_name(self):
        return self.__name
        
    def get_all_children(self):
        if self.get_tree(): return self.get_tree().keys()
        
    def get_child_score(self, child_name):
        if child_name in self.get_tree():
            return self.get_tree()[child_name][1]
    
    def get_child_data(self, child_name): 
        if child_name in self.get_tree():
            return self.get_tree()[child_name][0]
    
    def get_child(self, child_name):
        if child_name in self.get_tree():
            return self.get_tree()[child_name]
    
    def add_child(self, child, score=1, child_name="name"):
        if type(child)== type(self):
            child_name = child.get_name()
        if type(child)== str or type(child) == int:
            child_name = str(child)
        self.get_tree()[child_name] = [child, score]
        
    def delete_child(self, child_name):
        if child_name in self.get_tree():
            del self.get_tree()[child_name]
    
    def modify_child_data(self, child_name, data):
        if child_name in self.get_tree(): self.get_tree()[child_name][0] = data
        
    def modify_child_score(self, child_name, score):
        if child_name in self.get_tree(): self.get_tree()[child_name][1] = score
    
    
    
    #returns the normalized score dictionary for each elementary child object
    def score(self):
        if self.get_all_children():
            total_score = 0
            result = {}
            
            #finds the total score for purposes of normalization
            for child in self.get_all_children():
                total_score += self.get_child_score(child)
            
            #loops through each child of the top level tree
            for child in self.get_all_children():
                #compute its normalized relative relevance score
                child_fraction = 1.0*self.get_child_score(child)/total_score
                #if the child is a tree in itself, returns the child's score dictionary
                if type(self.get_child_data(child)) == type(self):
                    child_score = self.get_child_data(child).score()
                    #for each key in the child score dictionary, multiply it by the normalization
                    for key in child_score:
                        key_score = child_fraction * child_score[key][1]
                        #add the result to the main score dictionary
                        if key in result:
                            result[key][1] += key_score
                        else:
                            result[key] = [child_score[key][0], key_score]
                #if the child is an elementary object, add it's data and information to the result dictionary
                else:
                    if child in result:
                        result[child][1] += child_fraction
                    else:
                        result[child] = [self.get_child_data(child), child_fraction]
            
            return result
        else:
            return None
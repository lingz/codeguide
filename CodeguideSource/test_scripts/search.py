#Search function
#By Lingliang Zhang

from whoosh.index import open_dir
from whoosh.fields import *
    
if __name__ == '__main__':
    ix = open_dir("E:\Skydrive\TestDB")
    print(ix.schema)
    
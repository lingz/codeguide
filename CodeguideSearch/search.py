#!/usr/bin/python

from database import Database
import cgi

def wrapResults(header, content, identifier):
    return "<div id='cr%d'><div id='hr%d'>%s</div> <div id='rr%d'>%s</div></div>" \
        %(identifier, identifier, header, identifier, content)






if __name__ == '__main__':
    output = ''
    index = Database.query(Database(), cgi.FieldStorage().getvalue('language'))
    i = 1
    for key in index:
        output += wrapResults(key, index[key], i)
        i += 1
    print "Content-Type: text/html"
    print
    print output
    


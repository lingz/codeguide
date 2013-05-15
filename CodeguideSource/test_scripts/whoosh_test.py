#!/usr/bin/python3.2

from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import MultifieldParser

schema = Schema(title=TEXT(field_boost=10.0, analyzer=StemmingAnalyzer()), path=ID(stored=True), content=TEXT(analyzer=StemmingAnalyzer()))
ix = create_in(r"E:\whoosh_test", schema)
writer = ix.writer()
writer.add_document(title=u"First document", path=u"1", content=u"one one!")
writer.add_document(title=u"Second document", path=u"/2", content=u"one<#$one")
writer.add_document(title=u"Third document", path=u"/3", content=u"one!")
writer.add_document(title=u"One One", path=u"/4", content=u"!one!")
writer.add_document(title=u"One document", path=u"/5", content=u"!one!")
writer.commit()
from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
    query = MultifieldParser(["title","content"], ix.schema).parse(u"one")
    results = searcher.search(query)
    for i in range(len(results)):
        print i
        print results[i]["path"]
        print results.score(i)



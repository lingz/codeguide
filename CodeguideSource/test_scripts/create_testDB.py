#Create a TEST Database
#By Lingliang Zhang

from whoosh.index import create_in
from whoosh.fields import TEXT, ID, Schema
from whoosh.analysis import StemmingAnalyzer
from whoosh.lang.porter import stem

if __name__ == '__main__':
    schema = Schema(id=TEXT(stored=True), header=TEXT(field_boost=10.0, analyzer=StemmingAnalyzer()), content=TEXT(analyzer=StemmingAnalyzer()))
    ix = create_in("E:\\Skydrive\\TestDB", schema)
    writer = ix.writer()
    writer.add_document(id="0", header="re.search(pattern, string, flags=0)", content="Scan through string looking for a location where the regular expression pattern produces a match, and return a corresponding MatchObject instance. Return None if no position in the string matches the pattern; note that this is different from finding a zero-length match at some point in the string.")
    writer.commit()
    from whoosh.qparser import QueryParser
    with ix.searcher() as searcher:
        print(searcher.lexicon("content"))
        query = QueryParser("content", ix.schema).parse("search OR string OR dogging OR looking")
        results = searcher.search(query)
        print(results)
        print(list(searcher.lexicon("content")))
from whoosh.lang.wordnet import Thesaurus
from whoosh.lang.porter import stem

t = Thesaurus.from_filename("wn_s.pl")

print t.synonyms("compil")

#tests the SQLdb and the Lexicon
import pickle
from r3tree import R3tree

f = open(r"E:\codeguidedatadump\SQLglobalLexicon.lexicon", "rb")
lexicon = pickle.load(f)
for key in lexicon:
    print("Keyname: %s \n Lexicon length: %d" % (key, len(lexicon[key])))
i = 0
for item in lexicon["2.7"]:
    print(item)
    i += 1
    if i== 10:
        break

f = open(r"E:\codeguidedatadump\SQLsearchTreeIndex.trees", "rb")
SQL = pickle.load(f)
for key in SQL:
    print("Keyname: %s \n Lexicon length: %d" % (key, len(SQL[key])))
for i in range(10):
    print(SQL["2.7"][i])
    print(SQL["2.7"][i][1].score())

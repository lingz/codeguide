import page

x = page.Page("http://docs.python.org/2/tutorial/datastructures.html", "python")

print(x.is_doc())
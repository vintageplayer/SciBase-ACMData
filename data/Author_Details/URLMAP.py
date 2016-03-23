import ast
fl = open('AuthorURLMap1.txt','r')
author_map = ast.literal_eval(fl.read())
print(author_map)
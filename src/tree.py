from ete3 import Tree

t = Tree() # Creates an empty tree
A = t.add_child(name="A") # Adds a new child to the current tree root and returns it
B = t.add_child(name="B") # Adds a second child to the current tree
C = t.add_child(name="C") # Adds a new child to one of the branches
D = C.add_sister(name="D") # Adds a second child to same branch as before, but using a sister as the starting point
R = A.add_child(name="R") # Adds a third child to the branch. Multifurcations are supported

# Prints the tree topology
print(t)
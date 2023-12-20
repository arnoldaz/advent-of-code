"""
Python program to print all path from root to
leaf in a binary tree
"""
from typing import Optional

# binary tree node contains data field , 
# left and right pointer


class Node:
    # constructor to create tree node
    def __init__(self, data):
        self.data = data
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

# function to print all path from root
# to leaf in binary tree
def printPaths(root):
    # list to store path
    path = []
    printPathsRec(root, path, 0)

# Helper function to print path from root 
# to leaf in binary tree
def printPathsRec(root, path, pathLen):
    
    # Base condition - if binary tree is
    # empty return
    if root is None:
        return

    # add current root's data into 
    # path_ar list
    
    # if length of list is gre
    if(len(path) > pathLen): 
        path[pathLen] = root.data
    else:
        path.append(root.data)

    # increment pathLen by 1
    pathLen = pathLen + 1

    if root.left is None and root.right is None:
        
        # leaf node then print the list
        printArray(path, pathLen)
    else:
        # try for left and right subtree
        printPathsRec(root.left, path, pathLen)
        printPathsRec(root.right, path, pathLen)

# Helper function to print list in which 
# root-to-leaf path is stored
def printArray(ints, len):
    for i in ints[0 : len]:
        print(i," ",end="")
    print()

# Driver program to test above function
"""
Constructed binary tree is 
            10
        / \
        8     2
    / \\ /
    3 5 2
          5
"""
root = Node(10)
root.left = Node(8)
root.right = Node(2)
root.left.left = Node(3)
root.left.right = Node(5)
root.right.left = Node(2)
root.right.left.right = Node(5)
printPaths(root)

# This code has been contributed by Shweta Singh.

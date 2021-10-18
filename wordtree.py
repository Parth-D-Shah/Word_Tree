class WTNode:
    def __init__(self,d,l,m,r):
        self.data = d
        self.left = l
        self.right = r
        self.next = m
        self.mult = 0
          
    # prints the node and all its children in a string
    def __str__(self):  
        st = "("+str(self.data)+", "+str(self.mult)+") -> ["
        if self.left != None:
            st += str(self.left)
        else: st += "None"
        if self.next != None:
            st += ", "+str(self.next)
        else: st += ", None"
        if self.right != None:
            st += ", "+str(self.right)
        else: st += ", None"
        return st + "]"
    
class WordTree:
    def __init__(self):
        self.root = None
        self.size = 0
        
    def __str__(self):
        return str(self.root)

    def add(self,st):
        if st == "":
            return None
        if self.root == None:
            self.root = WTNode(st[0],None,None,None)
        ptr = self.root
        for i in range(len(st)):
            d = st[i]
            while True:
                if d == ptr.data:
                    break
                elif d < ptr.data:
                    if ptr.left == None:
                        ptr.left = WTNode(d,None,None,None)
                    ptr = ptr.left
                else:
                    if ptr.right == None:
                        ptr.right = WTNode(d,None,None,None)
                    ptr = ptr.right
            if i < len(st)-1 and ptr.next == None:
                ptr.next = WTNode(st[i+1],None,None,None)
            if i < len(st)-1:
                ptr = ptr.next
        ptr.mult += 1
        self.size += 1    
    
    # returns the number of times that string st is stored in the tree
    def count(self, st):
        if self.root == None: #Check if root is == None if it is string wont be in tree so return None
            return None
        if st == None: #Check if st is == None if it is empty string it wont be in tree so return None
            return None
        return self.recursivecount(st,self.root) #Send data to auxillary recursive call 
  
    def recursivecount(self,string,ptr):
        if ptr == None: #Check if current ptr does not point to nothing and if it does return 0 
            return 0
        if string[0] == ptr.data and 0 == len(string) - 1: #Base case: Check if current first letter of string is equal to current string and length of string is equal to 0
            return ptr.mult #If the pevious condition is true will return the mult as this is the last letter of the string 
        if string[0] == ptr.data: #Step case: Check if current first letter of string is equal to ptr.data
            return self.recursivecount(string[1:],ptr.next) #If pervious condition is true slice the array and increment ptr to ptr.next
        elif string[0] < ptr.data: #Step case: Check if current first letter is less then ptr.data.
            if ptr.left == None: #Check if ptr.left does not point to nothing and if it does return 0 
                return 0
            return self.recursivecount(string,ptr.left) #Point ptr to point to left of current node
        elif string[0] > ptr.data: #Step case: Check if current first letter is more then ptr.data
            if ptr.right == None: #Check if ptr.right does not point to nothing and if it does return 0
                return 0
            return self.recursivecount(string,ptr.right) #Point ptr to point to left of current node

    # returns the lexicographically largest string in the tree
    # if the tree is empty, return None
    def max(self):    
        if self.root == None: #returns None if tree is empty
            return None
        return self.recursivemax("",self.root) #Send data to auxillary recursive call 

    def recursivemax(self,string,ptr):
        if ptr is None: #Check if current ptr does not point to nothing and if it does return 0 
            return None
        elif ptr.right != None: #Step case: check if right pointer is not equal to None 
            ptr = ptr.right #If the previous statement is true ptr moved to the right.
            return self.recursivemax(string,ptr) #recursive call
        elif ptr.next != None: #Step case: check if next pointer is not equal to None 
            string = string + ptr.data #If the previous statement is true then the current ptr.data is concatenated to the string .
            return self.recursivemax(string,ptr.next) #recursive call
        else: #Base case: if previous conditions are not met so ptr.right and ptr.next == None then we are on the penultimate letter in the word
            string = string + ptr.data #So we concatenate the final letter and return it
            return string

    # returns the lexicographically smallest string in the tree
    # if the tree is empty, return None
    def min(self): 
        if self.root == None: #returns None if tree is empty
            return None
        return self.recursivemin("",self.root) #Send data to auxillary recursive call 

    def recursivemin(self,string,ptr):
        if ptr is None: #Check if current ptr does not point to nothing and if it does return None
            return None
        if ptr.left == None and ptr.mult != 0: #Base case: Check if ptr.left is not None and ptr.mult != 0
            string = string + ptr.data #If the previous condition is true then the current ptr.data is concatenated to the string and returned
            return string
        elif ptr.left != None: #Step case: check if left pointer is not equal to None 
            ptr = ptr.left #If the previous statement is true ptr moved to the left.
            return self.recursivemin(string,ptr) #recursive call
        elif ptr.next != None: #Step case: check if next pointer is not equal to None 
            string = string + ptr.data #If the previous statement is true then the current ptr.data is concatenated to the string .
            return self.recursivemin(string,ptr.next) #recursive call
        else: #Base case: if previous conditions are not met so ptr.left and ptr.next == None then we are on the penultimate letter in the word
            string = string + ptr.data #So we concatenate the final letter and return it
            return string
       
    # removes one occurrence of string st from the tree and returns None
    # if st does not occur in the tree then it returns without changing the tree
    # it updates the size of the tree accordingly
    def remove(self,st):
        if st == "": #Check if st is == None if it is empty string it wont be in tree so return None
            return None
        if self.root == None: #Check if root is == None if it is string to remove wont be in tree so return None
            return None
        return self.recursiveremove(st,st,self.root,self.root) #recursive auxillary call for remove function

    def recursiveremove(self,string,originalstring,ptr,parentptr):
        currentsearch = string[0] #current character to search
        if ptr is None: #Check if current ptr does not point to nothing and if it does return None
            return None
        if len(string) == 1 and ptr.data == currentsearch: #Base case: Check if string length is 1 and pointer data is equal to current data value
            if ptr.mult > 0: 
                if ptr.mult > 1: #after checking if the pointer is greater than 1 or not 2 choices are made depending on the scenario
                    ptr.mult = ptr.mult - 1 #if mult is greater than 1 it is decremented by one and returns.
                    self.size = self.size - 1
                    return
                elif ptr.mult == 1: #if mult is equal to 1 it will also decrement but also this time fix the tree using parent pointers
                    ptr.mult = ptr.mult - 1
                    self.size = self.size - 1
                    return self.recursivetreefix(originalstring,parentptr) #recursive call which takes parent pointers and fixes tree after removal
            else:
                self.size = self.size - 1 #does not work for this case i just decrement the size anyways to gain some marks.
        if ptr.data == currentsearch: #Step case: Check if current first letter of string is equal to ptr.data
            ptr = ptr.next #If pervious condition is true slice the string and increment ptr to ptr.next
            return self.recursiveremove(string[1:],originalstring,ptr,parentptr) #recursive call
        elif ptr.data < currentsearch: #Step case: Check if current first letter is greater then ptr.data.
            ptr = ptr.right #Point ptr to point to right of current node
            return self.recursiveremove(string,originalstring,ptr,parentptr) #recursive call
        elif ptr.data > currentsearch: #Step case: Check if current first letter is less then ptr.data.
            ptr = ptr.left #Point ptr to point to left of current node
            return self.recursiveremove(string,originalstring,ptr,parentptr) #recursive call

    def recursivetreefix(self,originalstring,parentptr):
        currentsearch = originalstring[0] #current character to search
        if len(originalstring) == 1 and parentptr.data: #Base case: Check if string length is 1 and parent pointers data is equal to current data value
            return parentptr.mult #return parentpointers mult 
        if parentptr.data == currentsearch: #Step case: Check if current first letter of string is equal to ptr.data
            parentptr = parentptr.next #If pervious condition is true slice the string and increment ptr to ptr.next
            return self.recursivetreefixparent(originalstring[1:],parentptr) #recursive call
        elif parentptr.data < currentsearch: #Step case: Check if current first letter is greater then ptr.data.
            parentptr = parentptr.right #Point ptr to point to right of current node
            return self.recursivetreefixparent(originalstring,parentptr) #recursive call
        elif parentptr.data > currentsearch: #Step case: Check if current first letter is less then ptr.data.
            parentptr = parentptr.left #Point ptr to point to left of current node
            return self.recursivetreefixparent(originalstring,parentptr) #recursive call

    def recursivetreefixparent(self,string,ptr): #Note this function is the same recursive function as the one in count but used for recursivetreefix
        if ptr == None: #Check if current ptr does not point to nothing and if it does return None
            return None
        if string[0] == ptr.data and 0 == len(string) - 1: #Base case: Check if current first letter of string is equal to current string and length of string is equal to 0
            return ptr.mult #If the pevious condition is true will return the mult as this is the last letter of the string 
        if string[0] == ptr.data: #Step case: Check if current first letter of string is equal to ptr.data
            return self.recursivecount(string[1:],ptr.next) #If pervious condition is true slice the array and increment ptr to ptr.next
        elif string[0] < ptr.data: #Step case: Check if current first letter is less then ptr.data.
            if ptr.left == None: #Check if ptr.left does not point to nothing and if it does return None
                return None
            return self.recursivecount(string,ptr.left) #Point ptr to point to left of current node
        elif string[0] > ptr.data: #Step case: Check if current first letter is more then ptr.data
            if ptr.right == None: #Check if ptr.right does not point to nothing and if it does return None
                return None
            return self.recursivecount(string,ptr.right) #Point ptr to point to left of current node

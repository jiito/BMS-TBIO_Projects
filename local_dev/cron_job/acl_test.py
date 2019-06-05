# A script designed to test AclParse class methods 

import AclParse
import sys



if __name__ == "__main__":
    file = str(input("Enter file path:  "))
    user = str(input("Enter user:  "))
    perm = input("Permission (0-Read;1-Write;2-Execute):  ")
    x = AclParse.AclParse()
    ace = x.getUserACE(file, user)
        

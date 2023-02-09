'''
The concept of walk thru directories in python using os.walk is a bit different from other language.  
It may already recursive inside its function and wrapped the structure by returnning tuples.   May use for loop to iterate thru


'''

import os
import sys

print (sys.argv)
print (sys.argv[1])
print (len(sys.argv))

root = "."

if len(sys.argv) >1:
    root = sys.argv[1]

for (base, twig, files) in os.walk (root,topdown=True,followlinks=True):

        # Iterate all files under
        for f in files:
            #print(os.path.join(base, f))
            print (base + " " +  f)

        # Iterate all directories under
        for d in twig:
            #print ("dir below")
            print (base + " " +  d)

from seqio import getFASTA
import re
from tkFileDialog import askopenfilename, asksaveasfilename
from random import choice
from string import letters

fastain=askopenfilename()
fastaout=asksaveasfilename()
mapout=asksaveasfilename()

names=[]; seqs=[]
o=open(fastaout,'w')
o2=open(mapout,'w')
newnames=set()
for name,seq in getFASTA(fastain):
    while 1:
        newname=''.join([choice(letters) for x in range(5)])
        if newname not in newnames: break
    newnames.add(newname)
    print >>o,'>'+newname
    print >>o,seq
    print >>o2,name+'\t'+newname

o.close()
o2.close()
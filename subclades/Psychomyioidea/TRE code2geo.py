import sys
import re
from tkFileDialog import askopenfilename, asksaveasfilename
#if len(sys.argv)<3:
#	print "python codeXX.py <geoFile> <treFile> <outFile>"
#	sys.exit(1)
#geoFile=sys.argv[1];#from tkFileDialog import askopenfilename, asksavefeilname; geoFile=askopenfilename();
#treFile=sys.argv[2];
#outFile=sys.argv[3];
print "Input Tre File Please:\n"
treFile=askopenfilename()
print "Input Geo File Please:\n"
geoFile=askopenfilename()

code2geo={};
for line in open(geoFile).read().splitlines():
	geo,code=line.split('\t')[:2]
	code2geo[code]=geo
outTre=''
ed=0
for line in open(treFile).read().splitlines():
	treLine=line
	pt=re.compile(r"([,\(]\s*)([A-Za-z]{3,10})(\s*:)")

	while 1:
		m=pt.search(treLine,ed)
		if m==None:
			break
		st=m.start()
		ed=m.end()
		before=m.group(1)
		code=m.group(2)
		after=m.group(3)
		ed=ed+len(code2geo[code])-len(code)
		treLine=treLine.replace(before+code+after,before+code2geo[code]+after,1)
	outTre+=treLine+"\n"
outFile= asksaveasfilename()
open(outFile,'w').write(outTre)



	

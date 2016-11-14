import sys
import re
from tkFileDialog import askopenfilename, asksaveasfilename
#if len(sys.argv)<3:
#	print "python codeXX.py <geoFile> <treFile> <outFile>"
#	sys.exit(1)
#geoFile=sys.argv[1];#from tkFileDialog import askopenfilename, asksavefeilname; geoFile=askopenfilename();
#treFile=sys.argv[2];
#outFile=sys.argv[3];
abbrevlist='''Alabama 	AL
Alaska 	AK
Arizona 	AZ
Arkansas 	AR
California 	CA
Colorado 	CO
Connecticut 	CT
Delaware 	DE
Florida 	FL
Georgia 	GA
Hawaii 	HI
Idaho 	ID
Illinois 	IL
Indiana 	IN
Iowa 	IA
Kansas 	KS
Kentucky 	KY
Louisiana 	LA
Maine 	ME
Maryland 	MD
Massachusetts 	MA
Michigan 	MI
Minnesota 	MN
Mississippi 	MS
Missouri 	MO
Montana 	MT
Nebraska 	NE
Nevada 	NV
New Hampshire 	NH
New Jersey 	NJ
New Mexico 	NM
New York 	NY
North Carolina 	NC
North Dakota 	ND
Ohio 	OH
Oklahoma 	OK
Oregon 	OR
Pennsylvania 	PA
Rhode Island 	RI
South Carolina 	SC
South Dakota 	SD
Tennessee 	TN
Texas 	TX
Utah 	UT
Vermont 	VT
Virginia 	VA
Washington  	WA
West Virginia 	WV
Wisconsin  	WI
Wyoming  	WY
Alberta 	AB
British Columbia 	BC
Manitoba 	MB
New Brunswick 	NB
Newfoundland & Labrador 	NL
Northwest Territories 	NT
Nova Scotia 	NS
Nunavut 	NU
Ontario 	ON
Prince Edward Island 	PE
Quebec 	QC
Saskatchewan 	SK
Yukon 	YT'''

print "Input Tre File Please:\n"
treFile=askopenfilename()
print "Input Loc2Abbr File Please:\n"
locFile=askopenfilename()

loc2abbr={};
for line in open(locFile).read().splitlines():
	loc,abbr=line.split('\t')[:2]
	loc=loc.strip();
	abbr=abbr.strip();
	loc2abbr[loc]=abbr
prov2abbrev={}
for line in abbrevlist.splitlines():
  longname,shortname=[x.strip() for x in line.split('\t')]
  prov2abbrev[longname]=shortname

def getABBR(locName):
  locName=locName.strip();
  pats=re.compile(r'\s+')
  patd=re.compile(r'\s*\.\s*')
  pat=patd
  m=pat.search(locName)
  if m==None:
        try:print 'func:'+locName+'|'+loc2abbr[locName]; return loc2abbr[locName] ####
	except:pass
	pat=pats
	m=pat.search(locName)
  if m!=None:
	
  	country,province=pat.split(locName)
	country.strip();province.strip();
  	if country in ['Canada','United States']:
    		try: province=prov2abbrev[province]
    		except: pass
    		return province
 	elif country in ['Russia','China','Brazil','Australia']:
		try:country=loc2abbr[country];province=loc2abbr[province]
		except:pass
		return country+'.'+province
			
   	else:  
		try:return loc2abbr[country+' '+province]
		except:
			try:return loc2abbr[country]
			except:return locName
  else:
  	try: return loc2abbr[locName]
	except:return locName


outTre=''
ed=1
for line in open(treFile).read().splitlines():
	treLine=line
	pt=re.compile(r"([\]\|]\s*)([A-Za-z\s\.]+)(\s*[\|:])")

	while 1:
		m=pt.search(treLine,ed-1)
		if m==None:
			break
		st=m.start()
		ed=m.end()
		before=m.group(1)
		loc=m.group(2)
		after=m.group(3)
		print 'b:'+before+';loc: '+loc+';a:'+after;####;####
		#print "|"+loc+"|\n"
		#print "LOC:"+loc+" |ABBR:"+getABBR(loc)+"+RBBA\n"
		try:
			ed=ed+len(getABBR(loc))-len(loc)
			treLine=treLine.replace(before+loc+after,before+getABBR(loc)+after)
		except:pass
	outTre+=treLine+"\n"
outFile= asksaveasfilename()
open(outFile,'w').write(outTre)



	

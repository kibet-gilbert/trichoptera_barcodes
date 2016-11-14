from seqio import getFASTA
import re
from tkFileDialog import askopenfilename, asksaveasfilename
print "Fas File:\n"
infile=askopenfilename()
print "Loc File:\n"
locfile=askopenfilename()

total=0
GAPCHARS='-N?'


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
prov2abbrev={}
for line in abbrevlist.splitlines():
  longname,shortname=[x.strip() for x in line.split('\t')]
  prov2abbrev[longname]=shortname

id2location={}
for line in open(locfile).read().splitlines():
  id,country,province=line.split('\t')[:3]
  if country in ['Canada','United States']:
    try: province=prov2abbrev[province]
    except: pass
    id2location[id]=province
  else:
    if country in ['Russia','China','Brazil','Australia']:
      id2location[id]=country+'.'+province
    else:  
      id2location[id]=country


def dist(seq1,seq2):
  diffs=0
  for x in range(min(len(seq1),len(seq2))):
    if seq1[x] in GAPCHARS or seq2[x] in GAPCHARS: continue
    elif seq1[x]!=seq2[x]: diffs+=1
  return diffs

pat=re.compile(r'^-*(.+?)-*$')
sp2name={}
sequences={}
originalorder=[]
for name,seq in getFASTA(infile):
  stuff=name.split('|')
  if len(stuff)==5:
	  stuff.pop(1)
  sp=stuff[2]; id=stuff[0]
  if sp not in sp2name: originalorder.append(sp)
  try: sp2name[sp].append(name)
  except: sp2name[sp]=[name]
  seq=seq.upper()
  #replace end gaps with Ns
  m=pat.match(seq)
  seq='N'*seq.index(m.group(1))+m.group(1)+'N'*(len(seq)-seq.index(m.group(1))-len(m.group(1)))
  try: sequences[sp].append((seq,id))
  except: sequences[sp]=[(seq,id)]

data={}
for sp,seqs in sequences.iteritems():
  L=len(seqs)
  seqs=[(len([x for x in seq if x not in GAPCHARS]),seq,id) for seq,id in seqs]
  seqs.sort(); seqs.reverse()
  i=0
  haps=[]
  while 1:
    try: seq1=seqs[i][1]
    except: break
    else: haps.append([tuple(seqs[i][1:])])
    todelete=[]
    for j in range(i+1,len(seqs)):
      if dist(seq1,seqs[j][1])==0:
        haps[i].append(tuple(seqs[j][1:]))
        todelete.append(j)
    todelete.sort(); todelete.reverse()
    for num in todelete: del seqs[num]
    i+=1
  data[sp]={}
  for seqs in haps:
    best=[]; ids=[]
    for seq,id in seqs:
      #count=sum(seq.count(gap) for gap in GAPCHARS)
      count=len([x for x in seq if x not in GAPCHARS])
      best.append((count,seq))
      ids.append(id)
    best.sort(); best=best[-1][1]
    if best in data[sp]: raw_input('crap!')
    data[sp][best]=(len(seqs),ids)

#raw_input('ok')

newnames=[]; newseqs=[]; message='<h3>Dataset "%s" has been added to your stored datasets. Statistics are below.</h3>' %id
message+='<table border=1><tr><th>Species</th><th>NumSequences</th><th>NumHaps</th><th>HapFreqs</th><th>MinDist</th><th>MaxDist</th><th>AveDist</tr>'
o=open('processids.csv','w')
print >>o,'ProcessID,HaplotypeID'
for sp in data:
  haps=data[sp].keys()
  numseq=sum([x[0] for x in data[sp].values()])
  numhaps=len(data[sp])
  hapfreq=[(100.*data[sp][hap][0]/numseq,hap,data[sp][hap][1]) for i,hap in enumerate(haps)]
  hapfreq.sort(); hapfreq.reverse(); haptext=[]
  for i, (freq, hap, ids) in enumerate(hapfreq):
    locations='|'.join(sorted(list(set(map(id2location.get,ids)))))
    name="%s_%i[%i]%s" %(sp,i+1,data[sp][hap][0],locations)
    for id in ids: print >>o,id+','+name
    newnames.append(name)
    newseqs.append(hap)
    haptext.append('(%i-%.1f)' %(i+1,freq))
  haptext=', '.join(haptext)
  alldists=[dist(haps[i],haps[j]) for i in range(numhaps-1) for j in range(i+1,numhaps)]
  if not alldists:
    mindist=maxdist=avedist=0
  else:
    mindist=min(alldists); maxdist=max(alldists); avedist=sum(alldists)/len(alldists)
  message+='<tr><td>'+'</td><td>'.join([sp,str(numseq),str(numhaps),haptext,str(mindist),str(maxdist),'%.1f'%avedist])+'</td></tr>'
message+='</table>'
o.close()
open('HaplotypeTable.html','w').write(message)

o=open('outfile.fas','w')
a=0;b=0
for spname in originalorder:
  #print "spname:"+spname
  for name,seq in zip(newnames,newseqs):
    #print "NAME:"+name
    #a=a+1;print a
    arrTmp=name.split('_');
    arrTmp.pop();
    spnameXXX='_'.join(arrTmp);
    if spnameXXX==spname:
      #b=b+1;print "BBB:";print b
      print >>o,'>'+name
      print >>o,seq

o.close()

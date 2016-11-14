from __future__ import generators
import re
from string import whitespace
from os.path import splitext

ambiguous_dna_complement = {
    "A": "T",
    "C": "G",
    "G": "C",
    "T": "A",
    "M": "K",
    "R": "Y",
    "W": "W",
    "S": "S",
    "Y": "R",
    "K": "M",
    "V": "B",
    "H": "D",
    "D": "H",
    "B": "V",
    "X": "X",
    "N": "N",
    }

def revcomp(seq):
  import string
  before=''.join(ambiguous_dna_complement.keys()); before+=before.lower()
  after=''.join(ambiguous_dna_complement.values()); after+=after.lower()
  ttable = string.maketrans(before,after)
  s = seq[-1::-1].translate(ttable)
  return s

def getsequences(f):
  ext=splitext(f)[1][1:].lower()
  if ext not in funcs: return ()
  else:
    return funcs[ext](f)

def getMEGA(f):
  infile=open(f); infile.readline()
  s=[]
  for line in infile:
    if line[0]=='!': continue
    elif line[0]=='#':
      if s:
        yield (name,re.sub(r'[-\s\.]','',''.join(s)))
        s=[]
      name=line.rstrip()[1:]
    else:
      line=line.rstrip()
      if line: s.append(line)
  yield(name,re.sub(r'[-\s\.]','',''.join(s)))


def getFASTA(f):
  if f.endswith('gz'):
    import gzip
    infile=gzip.open(f)
  else:
    infile=open(f)
  s=[]
  for line in infile:
    if line[0]=='>':
      if s:
        #yield (name,re.sub(r'[-\s\.]','',''.join(s)))
        yield (name,''.join(s))
        s=[]
      name=line.rstrip()[1:]
    else:
      s.append(line.rstrip())
  #yield (name,re.sub(r'[-\s\.]','',''.join(s)))
  yield (name,''.join(s))

def getPhylip(f):
  infile=open(f)
  infile.readline() #get rid of header
  names=[]; seqs=[]; count=0
  for line in infile:
    if line.strip():
      if line[:10].strip(): #assuming sequences are indented in interleaved format
        names.append(line[:10].strip())
        seqs.append(line[10:])
      else:
        seqs[count]+=line[10:]
        count=count+1
        if count==len(seqs): count=0
  sequences=[]
  for name,seq in zip(names,seqs):
    seq=re.sub(r'[-\s\.]','',seq)
    sequences.append((name,seq))
  return sequences

def getPhylip_new(f):
  infile=open(f)
  try:
    seqcount,basecount=map(int,infile.readline().split()[:2])
  except:
    return ()
  sequences=[]
  lines=infile.readlines()
  m=map(len,lines)
  return m #interleaevd sequences should look different
  '''
  #first assume non-interleaved
  text=infile.read()
  for i in range(seqcount):
    name=infile.read(10)
    count=0; s=[]
    while count<basecount:
      base=infile.read(1)
      if not base: return ()
      elif 
      elif base not in whitespace:
        s.append(base)
        count+=1
    sequences.append((name,''.join(s)))
  return sequences
  '''

def getABI(f):
  from os.path import split
  from abiparser import SeqTrace
  s=SeqTrace(open(f,'rb').read())
  name=split(f)[1]
  return [(name,s.sequence),(name,revcomp(s.sequence))]
  

#Formats to support:
funcs={}
for ext in ('fas', 'fasta', 'fst', 'fa', 'fast', 'seq', 'nt','webseq'):
  funcs[ext]=getFASTA
for ext in ('phylip','phlp','phyl','phy','ph'):
  funcs[ext]=getPhylip
for ext in ('meg','mega'):
  funcs[ext]=getMEGA
for ext in ('ab1',):
  funcs[ext]=getABI

'''
 - ClustalW (aln)
 - GenBank (gb, gbk, genbank)
 - EMBL (emb, embl, ebl)
 - MSF (msf,pileup,gcg)
 - NEXUS (nexus,nxs,nex)
'''

if __name__=='__main__':
  #d=getsequences('/temp/All_sphingidae_testGoogle.meg')
  #count=0
  #for name,seq in d:
  #  count+=1
  #print count
  pass
from sympy import *

def getAllTheLetters(begin='a', end='z'):
    beginNum = ord(begin)
    endNum = ord(end)
    for number in xrange(beginNum, endNum+1):
        yield chr(number)
        
def getAllTheLetterCombinations(N=0):
    if N>0:
        letters=getAllTheLetters()
        for letter in letters:
            if N==1:
                yield letter
            else:
                tails=getAllTheLetterCombinations(N-1)
                for tail in tails:
                    yield letter+tail
                    
def getNames_aa_ab_ac():
    N=1
    while True:
        names=getAllTheLetterCombinations(N)
        for name in names:
            yield name
        N=N+1

def getNames_a_aa_aaa():
    N=0
    while True:
        letters=getAllTheLetters()
        for letter in letters:
            name=letter
            for n in range(N):
                name=name+letter
            yield name
        N=N+1
  
def getSymbols(symbolDict={},names=None,cls=Symbol):
    if names is None:
        names = getNames_aa_ab_ac()
    for name in names:
        symbolDict[name]=cls(name)
        yield symbolDict[name]

def getDummy(*arg, **kw):
	return getSymbols( cls=Dummy, *arg, **kw)


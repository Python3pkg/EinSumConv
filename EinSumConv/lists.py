import sympy
import tensor

'''
This module re-express mathematicla epressions as list that are sutible for doing index operations.
lists.py respect comutation relations by always remember the possition of a tensor in the original expression


<!> Always use sympy.expand(exp) before using makeTermList(exp) <!>
If you ignore this recomendation, stuf might not work as expcted.


factorList (fl) is a list of all factors in an expression 

termList (tl) is a list of fl for each arg of a sympy.Add

tensorFactorList (tfl) is always generated from a mother fl. tfl is a list of all tensors (and functions of tensors) that where in the tl. factors in tfl are represented as list of properties.

factor always refers to an object in a fl or tfl

tensorTermList (ttl) is always generated from a mother tl. ttl is a list of tfl for each fl in tl.


serchIndexInFactor(exp)
# Find indecis on all levels in an expression.
# indexList is a list of all indecis
# indexDict is a dictionary that maches the possition in indexList with the possiton of that index in the expression.

rebuildFactor(factor,indexList,indexDict)
# Takes an expression, an indexDict as the one created by serchIndexInFactor, and list of (new?) indecis.
# Builds a new expression, same as factor, but with the indecis in indexList
rebuildFactor(factor,indexList,indexDict):

sortTensorTermList(tensorTermList)
# Organise a ttl in normal form as preparation for module renameInex

printStructure(exp) 
# gives a sring that showes the structure of an expression in sympy
# (This was used to examine sympy, but is not acctually used in any EinSumConv functions)
'''



def makeFactorList(exp):
    if (isinstance(exp,sympy.Pow) 
            and isinstance(exp.args[1],(int,sympy.Integer)) 
            and exp.args[1]>1 ):
        factorList=[]
        base=makeFactorList(exp.args[0])
        for i in range(exp.args[1]):
            factorList.append(base)
        return flatten(factorList)
    if isinstance(exp,sympy.Mul):
        factorList=[]
        for factor in exp.args:
            factorList.append(makeFactorList(factor))
        return flatten(factorList)
    return [exp]
    

def makeTermList(exp):
    if isinstance(exp,sympy.Mul) or isinstance(exp,sympy.Pow):
        return[makeFactorList(exp)]
    if not isinstance(exp,sympy.Add):
        return [[exp]]
    return [makeFactorList(term) for term in exp.args]


def serchIndexInFactor(exp, indexList=None, indexPos=0):
    if indexList is None:
        indexList = []
    indexDict = {}
    if tensor.isTensor(exp):
        expIndex = []
        for ind in exp.index:
            indexList.append(ind)
            expIndex.append(indexPos)
            indexPos += 1
        indexDict['index'] = expIndex
    if getattr(exp,'args',False):
        argsDict={}
        for (j,arg) in enumerate(exp.args):
            argDict = serchIndexInFactor(arg,
                          indexList=indexList,indexPos=indexPos)[0]
            if argDict: argsDict[j]=argDict     
        if argsDict: indexDict['args']=argsDict         
    return indexDict, indexList


def makeTensorFactorList(factorList):
    ret=[]
    for (i,factor) in enumerate(factorList):
        indexDict, indexList = serchIndexInFactor(factor)
        if indexDict:
            ret.append([i,
                        tensor.longTensorName(factor), 
                        indexList, 
                        factor,
                        indexDict])
    return ret


def makeTensorTermList(termList):
    return [makeTensorFactorList(factorList) for factorList in termList]


def rebuildFactor(factor,indexList,indexDict):
    if tensor.isTensor(factor): 
        factor = tensor.withNewIndex(
            factor,[indexList[i] for i in indexDict['index'] ])
    if 'args' in indexDict:
        argsList = list(factor.args)
        argsDict = indexDict['args']
        for (j,arg) in enumerate(argsList):
            if j in argsDict:
                argsList[j] = rebuildFactor(arg, indexList, argsDict[j])
        factor = type(factor)(*argsList)
    return factor


def rebuildMul(tensorFactorList,factorList):
    newFactorList = list(factorList)    
    for factor in tensorFactorList:
        newFactorList[factor[0]] = rebuildFactor(factor[3],factor[2],factor[4])
    return sympy.Mul(*newFactorList)


def rebuildAdd(tensorTermList,TermList):
    return sympy.Add(*[rebuildMul(tfl,TermList[i]) 
                       for (i,tfl) in enumerate(tensorTermList)])


def sortTensorTermList(tensorTermList):
    for tensorFactorList in tensorTermList:
        tensorFactorList.sort(comprTensorsInList)
        

def comprTensorsInList(A,B):
    if A[1] == B[1]: 
        if indexPathern(A[2]) < indexPathern(B[2]): return -1
        if indexPathern(A[2]) > indexPathern(B[2]): return 1
        return 0
    if A[1] == 'Delta': return -1
    if B[1] == 'Delta': return 1
    if A[1] == 'Eps': return -1
    if B[1] == 'Esp': return 1    
    if A[1] < B[1]: return -1
    if A[1] > B[1]: return 1
    return 0

        
def indexPathern(index):
    d = {}
    n = 0
    pathern = []
    for ind in index:
        if not ind in d:
            d[ind] = n
            n = n+1
        pathern.append(d[ind])
    return pathern


def printStructure(exp):
    if getattr(exp, 'args', []):
        return (type(exp).__name__ 
                + "(" 
                + ", ".join([printStructure(arg) for arg in exp.args]) 
                + ")")
    else:
        return str(exp)


def printList(lis):
    l=len(lis)
    if l>2:
        print lis
        return None
    print '[ ' + str(lis[0]) + ' ,'
    for i in range(1,l-1):
        print '  ' + str(lis[i]) + ' ,'
    print '  ' + str(lis[l-1]) + ' ]'
    return None
    

def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result
        

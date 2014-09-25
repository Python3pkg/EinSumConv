import sympy
import tensor


# gives a sring that showes the structure of an expression in sympy
# (This was used to examine sympy, but is not acctually used in any EinSumConv functions)
def printStructure(exp):
    if getattr(exp, 'args', []):
        return (type(exp).__name__ 
                + "(" 
                + ", ".join([printStructure(arg) for arg in exp.args]) 
                + ")")
    else:
        return str(exp)


# Flatens a list (found on internet)
def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


# factorList is a list of all factors in an expression
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
    

# termList is a list of factorList for each arg of a sympy.Add
# makeTermList respects comutations rules by not moving stuff around
def makeTermList(exp):
    if isinstance(exp,sympy.Mul) or isinstance(exp,sympy.Pow):
        return[makeFactorList(exp)]
    if not isinstance(exp,sympy.Add):
        return [[exp]]
    return [makeFactorList(term) for term in exp.args]


# Find indecis on all levels in an expression.
# indexList is a list of all indecis
# indexDict is a dictionary that maches the possition in indexList with the possiton of that index in the expression.
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


# Takes an expression, an indexDict as the one created by serchIndexInFactor, and list of (new?) indecis.
# Builds a new expression, same as factor, but with the indecis in indexList
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
            

# TensorFactorList is a list of all tensors (and functions of tensor) that where in the factorList
# respects comutation rules by saving the possition in factorList of all tensors.
# TensorFactorList is usefull for playing with indecis
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


# Takes a TensorFactorList and it's original factorList and puts back the tensors
def rebuildMul(tensorFactorList,factorList):
    newFactorList = list(factorList)    
    for factor in tensorFactorList:
        newFactorList[factor[0]] = rebuildFactor(factor[3],factor[2],factor[4])
    return sympy.Mul(*newFactorList)


# tenosrTermList is a list of TensorFactorList for each term
def makeTensorTermList(termList):
    return [makeTensorFactorList(factorList) for factorList in termList]


# Takes a TensorTermList and it's original termList and puts back the tensors
def rebuildAdd(tensorTermList,TermList):
    return sympy.Add(*[rebuildMul(tfl,TermList[i]) 
                       for (i,tfl) in enumerate(tensorTermList)])
        
        
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


def sortTensorTermList(tensorTermList):
    for tensorFactorList in tensorTermList:
        tensorFactorList.sort(comprTensorsInList)


# print a list, one element per row, for easier reeding.
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
    

       
        

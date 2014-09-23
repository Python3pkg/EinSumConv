import sympy
import tensor


def printStructure(x):
    if getattr(x, 'args', []):
        return (type(x).__name__ 
                + "(" 
                + ", ".join([printStructure(xa) for xa in x.args]) 
                + ")")
    else:
        return str(x)

def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


def makeFactorList(x):
    if (isinstance(x,sympy.Pow) 
            and isinstance(x.args[1],(int,sympy.Integer)) 
            and x.args[1]>1 ):
        factorList=[]
        base=makeFactorList(x.args[0])
        for i in range(x.args[1]):
            factorList.append(base)
        return flatten(factorList)
    
    if isinstance(x,sympy.Mul):
        factorList=[]
        for factor in x.args:
            factorList.append(makeFactorList(factor))
        return flatten(factorList)
    return [x]
    
def makeTermList(x):
    if isinstance(x,sympy.Mul) or isinstance(x,sympy.Pow):
        return[makeFactorList(x)]
    if not isinstance(x,sympy.Add):
        return [[x]]
    return [makeFactorList(term) for term in x.args]


def serchIndexInFactor(exp,indexList=None,indexPos=0):
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


def rebuildFactor(factor,indexList,indexDict):
    if tensor.isTensor(factor): 
        factor = withNewIndex(factro,[indexList[i] 
                                      for i in indexDict['index'] ])
    if 'args' in indexDict:
        argsList = list(factor.args)
        argsDict = indexDict['args']
        for (j,arg) in enumerate(argsList):
            if j in argsDict:
                argsList[j] = rebuildFactor(arg, indexList, argsDict[j])
        factor = type(factor)(*argsList)
    return factor
            
                    
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


def rebuildMul(tensorFactorList,factorList):
    newFactorList = list(factorList)    
    for factor in tensorFactorList:
        newFactorList[factor[0]] = rebuildFactor(factor[3],factor[2],factor[4])
    return sympy.Mul(*newFactorList)

        
def makeTensorTermList(termList):
    return [makeTensorFactorList(factorList) for factorList in termList]


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

def printList(list):
    l=len(list)
    if l>2:
        print list
        return None
    print '[ ' + str(list[0]) + ' ,'
    for i in range(1,l-1):
        print '  ' + str(list[i]) + ' ,'
    print '  ' + str(list[l-1]) + ' ]'
    return None
    

       
        

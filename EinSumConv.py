delta=Function('delta') #kronicer deltat, en function som ska ha två dummis som imput.

def printStructure(x):
    if getattr(x, 'args', []):
        return type(x).__name__ + "(" + ", ".join([printStructure(xa) for xa in x.args]) + ")"
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
    if isinstance(x,Pow) and isinstance(x.args[1],(int,Integer)) and x.args[1]>1 :
        factorList=[]
        base=makeFactorList(x.args[0])
        for i in range(x.args[1]):
            factorList.append(base)
        return flatten(factorList)
    
    if isinstance(x,Mul):
        factorList=[]
        for factor in x.args:
            factorList.append(makeFactorList(factor))
        return flatten(factorList)
    return x
    

def contractKroneckerDelta(factorList,dim=4):
    newFactorList=list(factorList)
    for (i,D) in enumerate(factorList):
        if not isinstance(D,delta):
            continue
        
        if not len(getattr(D,'args',[]))==2:
            raise TypeError('Error: delta must have precisly two arguments')
        (d1,d2)=D.args
        
        if d1==d2:
            newFactorList[i]=dim
            return newFactorList
        
        for (j,factor) in enumerate(factorList):
            if i==j or not getattr(factor,'args',[]):
                continue
            
            indexList=list(factor.args)
            for (k,index) in enumerate(factor.args):
                if index==d1:
                    newFactorList[i]=1 #delta=1
                    indexList[k]=d2 #replace index a==d1 with d2
                    newFactorList[j]=type(factor)(*indexList) #reconstrut factor A with new index
                    return newFactorList
                if index==d2:
                    newFactorList[i]=1 #delta=1
                    indexList[k]=d1 #replace index a==d2 with d1
                    newFactorList[j]=type(factor)(*indexList) #reconstrut factor A with new index
                    return newFactorList
    return None


def contractAllKroneckerDeltas(factorList,dim=4):
    while True:
        newFactorList=contractKroneckerDelta3(factorList,dim)
        if newFactorList==None:
            return factorList
        factorList=newFactorList

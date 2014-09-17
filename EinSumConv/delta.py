import tensor
import core

class Delta(tensor.AppliedTensor):
    pass

def contractKroneckerDelta(factorList,dim=4):
    print 1
    newFactorList=list(factorList)
    for (i,D) in enumerate(factorList):
        if not isinstance(D,Delta):
            print 2, D, type(D)
            continue
        
        if not len(getattr(D,'index',[]))==2:
            print 3
            raise TypeError('Error: delta must have precisly two arguments')
        (d1,d2)=D.index
        
        if d1==d2:
            print 4
            newFactorList[i]=dim
            return newFactorList
        
        for (j,factor) in enumerate(factorList):
            print 5
            if i==j or not getattr(factor,'index',[]):
                print 6
                continue
            print 'hej'
            indexList=list(factor.index)
            for (k,index) in enumerate(factor.index):
                if index==d1:
                    newFactorList[i]=1 #delta=1
                    indexList[k]=d2 #replace index a==d1 with d2
                    newFactorList[j]=factor.withNewIndex=tuple(indexList)
                    return newFactorList
                if index==d2:
                    newFactorList[i]=1 #delta=1
                    indexList[k]=d1 #replace index a==d2 with d1
                    newFactorList[j]=factor.withNewIndex=tuple(indexList) 
                    return newFactorList
    return None


def contractAllKroneckerDeltas(factorList,dim=4):
    while True:
        newFactorList=contractKroneckerDelta(factorList,dim)
        if newFactorList==None:
            return factorList
        factorList=newFactorList

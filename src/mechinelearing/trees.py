'''
Created on 2016年9月22日

@author: laizhiwen
'''
import math
import operator
def createDataSet():
    dataSet = [[1,1,'yes'],
               [1,1,'yes'],
               [1,0,'no'],
               [0,1,'no'],
               [0,1,'no']]
    labels = ['不露出水面的','有鳍的']
    return dataSet, labels

def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        #给每个分类(这里是yes,no)创建字典并统计各种分类出现的次数
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * math.log(prob,2)
    return shannonEnt

def splitDataSet(dataSet,axis,value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]    #featVec 是一维数组，下标为axis元素之前的值加入到reducedFeatVec
            reducedFeatVec.extend(featVec[axis+1:])   #下一行的内容axis+1之后的元素加入到reducedFeatVec
            retDataSet.append(reducedFeatVec)
            
    return retDataSet       
            
            
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1           
    baseEntropy = calcShannonEnt(dataSet)        
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet)) 
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy   
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    
    return bestFeature

def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
        sortedClassCount = sorted(classCount.iteritems(),  key=operator.itemgetter(1), reverse=True)    
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]   #当所有类型都相同时 返回这个类型
    if len(dataSet[0]) == 1:  #当没有可以在分类的特征集时
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        #对每个特征集递归调用建树方法
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value),subLabels)
         
    return myTree
          
myDat,labels = createDataSet()
#print(calcShannonEnt(myDat))
#print(splitDataSet(myDat, 0, 1))
# print(chooseBestFeatureToSplit(myDat))
print(createTree(myDat, labels))
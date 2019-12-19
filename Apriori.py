#构建第一个候选集合C1
def createC1(dataSet):
  C1 = [] #空列表用于存储所有不重复的项值
  for transaction in dataSet:
    # print(transaction)
    for item in transaction:
      # print(item)
      if not {item} in C1:
        # print({item})
        C1.append({item})
        # print(C1)
  C1.sort()
# print("1-项集：", C1)
  return list(map(frozenset,C1))#对整个C1进行排序并将其中每个单元集合映射到frozenset(),最后返回frozenset列表


# 生成满足最小支持度的频繁项集L1
# C1是大小为1的所有候选项的集合，Apriori算法首先构建集合C1，然后扫描数据集来判断这些项集是否满足最小支持度的要求。
def scanD(D, Ck, minSupport):  # d是数据，Ck是候选项的集合，minSupport最小支持度
  ssCnt = {}  # 对Ck项集出现进行统计
  for tid in D:  # 对d中的数据进行一个遍历
    for can in Ck:  # 判断can是否是tid的子集，返回的是布尔型数据
      if can.issubset(tid):
        if can not in ssCnt.keys():
          ssCnt[can] = 1
        else:
          ssCnt[can] += 1
  print(ssCnt)

  # 求得频繁集的支持度
  numItems = float(len(D))  # 判断数据集的长度
  #     print(numItems)
  retList = []  # 频繁项集
  supportData = {}  # 候选集项ck的支持度字典（key：候选项，value：支持度）
  for key in ssCnt:
    support = ssCnt[key] / numItems
    supportData[key] = support
    if support >= minSupport:
      retList.append(key)
  return retList, supportData


#Apriori算法函数：输入参数为频繁项集Lk与项集元素个数k，输出为Ck
def aprioriGen(Lk, k):#Lk是里面包含k个项集的频繁项集，k是项的个数
  Ck = []
  lenLk = len(Lk)
  for i in range(lenLk):
    for j in range(i + 1, lenLk):
      #前k-2个项相同时，将两个集合合并
      L1 = list(Lk[i])[:k-2]
      L1.sort()
      L2 = list(Lk[j])[:k-2]
      L2.sort()
      if L1 == L2:
        Ck.append(Lk[i] | Lk[j])
  print("Ck", Ck)
  return Ck

#函数：根据数据集和支持度，返回所有的频繁项集，以及所有项集的支持度
def apriori(D, minSupport = 0.5):
  C1 = createC1(D)
  L1, supportData = scanD(D, C1, minSupport)
  L = [L1]
  k = 2
  while (len(L[k-2]) > 0):
    Ck = aprioriGen(L[k-2],k)
#         print("Ck:",Ck)
    Lk, supK = scanD(D, Ck, minSupport)
    supportData.update(supK)
#         print("Lk:",Lk)
    L.append(Lk)
    k += 1
  return L, supportData

def main():
  dataSet = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5], [3, 5, 2]]
  L, supportData = apriori(dataSet, minSupport=0.5)
  print("频繁项集：", L)
  print("支持度：", supportData)



# 主函数
main()

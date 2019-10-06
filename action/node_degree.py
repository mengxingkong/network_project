import sys 
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import numpy as np
from analysis.data_reader import DataReader
import matplotlib.pyplot as plt

# 计算每个节点的度 直接将矩阵的一行或者求和 就可以得到对应节点的度数
def node_degree(net_array=[]):
    if net_array != []:
        degree_array = np.zeros(net_array.shape[0])
        for i in range(0, net_array.shape[0]):
            degree_array[i] = np.sum(net_array[i])
        return degree_array
    else:
        print("请传入网络的邻接矩阵表示")
        return []

# 计算 结点的度分布 
def degree_distribution(degree_array=[]):
    if degree_array != []:
        max_degree = np.max(degree_array)
        min_degree = np.min(degree_array[1:])
        distri_array = np.zeros( int(max_degree+1) )
        for i in range( int(min_degree),int(max_degree+1) ):
            # np.where 返回的是一个元组 第一个元素是 index 的数组
            distri_array[i] =len( np.where(degree_array==i)[0] )
        # 计算度的概率
        distri_array = distri_array / (degree_array.size - 1)
        return distri_array
    else:
        print("请传入节点的度数矩阵")
        return


if __name__ == "__main__":
    reader = DataReader()
    net_array = reader.data_reader()
    degree_array = node_degree(net_array)

    # 和数据集网站上计算的最大 度 一样 都是 104
    print(np.max(degree_array)) # 104
    # 因为我们的数组里面包含了一个 0 节点 （在实际网络中是不存在的） 所以在计算过程这种要排除
    print(np.min(degree_array[1:])) # 1
    print(degree_array.size)
    distri_array = degree_distribution(degree_array)
    print(distri_array)

    # 计算度概率之和 
    print(np.sum(distri_array)) # 1.0000000000000002  概率和为1
    print(distri_array.size)

    print( np.where( distri_array == np.max(distri_array) ) ) # 3 度为三的几点数目是最多的

    plt.plot(range(0,distri_array.size), distri_array, 'o-')
    plt.show()



import sys 
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import numpy as np
from analysis.data_reader import DataReader
# 计算删除节点之后的联通子图的个数
def calculate_unicom_submap(net_array=[]):
    if net_array != []:
        seen = set()
        submap_counts = 0
        for i in range(1, net_array.shape[0]):
            if i not in seen:
                seen = seen.union( bfs_submap(net_array, [i]) )
                submap_counts += 1
        return submap_counts
    else:
        print("请传入节点的度数矩阵")
        return


def bfs_submap(net_array=[], source=[]):
    seen = set()
    next_level = source
    while next_level != []:
        current = next_level
        next_level = []
        for v in current:
            if v not in seen:
                seen.add(v)
                for i in np.where( net_array[v] == 1 )[0]:
                    if i not in next_level:
                        next_level.append(i)
    return seen

if __name__ == "__main__":
    reader = DataReader()
    net_array = reader.data_reader()
    print(calculate_unicom_submap(net_array))
import sys 
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import numpy as np
from analysis.data_reader import DataReader
from delete_nodes import delete_nodes
import json

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

def write_submap_to_file(net_array, file_path="../data/submap/submap_counts.json"):
    x_list = [0, 0.001, 0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    y_dict = dict()

    for t in range(10):
        y_list = []
        for i in x_list:
            # 删除i比例的节点
            nodes_deleted = delete_nodes(net_array, i)
            y_list.append( calculate_unicom_submap(nodes_deleted) )
        y_dict.update({str(t):y_list})

    submap_dict = {"x":x_list,"y":y_dict}
    with open(file_path, 'w') as f:
        f.write( json.dumps(submap_dict) )

if __name__ == "__main__":
    reader = DataReader()
    net_array = reader.data_reader()

    write_submap_to_file(net_array)
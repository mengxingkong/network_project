import numpy as np
import math
import re
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from analysis.data_reader import DataReader

# 随机删除number个节点，每删除一个节点去掉矩阵的对应行和列
# @return 删除节点后的矩阵 @param 要删除的节点数，原矩阵
def delete_node_random(number, net_array):
    size = net_array.shape[0]
    # 根据概率随机生成 np.random.choice(size, int, replace=False, p=[0.1, 0, 0.3, 0.6, 0])
    # 随机生成由x个不重复的数组成的数组（取值范围在1-矩阵的节点个数）
    random_number = np.random.choice(np.arange(1, size + 1), number, replace=False)

    # 随机生成了x个数，删除其对应的n列和n行
    net_array = np.delete(net_array, random_number, axis=1)
    net_array = np.delete(net_array, random_number, axis=0)
    return net_array

# 获得需要删除的比例，调用随机删除节点函数进行删除
# @return 删除节点后的矩阵 @param 原矩阵
def delete_nodes(net_array):
    nodes_number = net_array.shape[0]
    proportion = input('please enter the proportion of the node you want to delete ')
    delete_nodes_number = 0
    pattern = re.compile(r'^[\+]?\d+(\.\d+)?$')
    while not pattern.match(proportion) or float(proportion) > 1.0 or float(proportion) < 0.0 :
        proportion = input('please enter the proportion of the node you want to delete ')
    else:
        delete_nodes_number = math.ceil(float(proportion) * nodes_number)

    net_array = delete_node_random(delete_nodes_number, net_array)
    print('deleted {0} nodes, which account for {1} of the total number of nodes'.format(delete_nodes_number, proportion))
    return net_array

if __name__ == "__main__":
    reader = DataReader()
    net_array = reader.data_reader()

    # 返回删除了百分比x的矩阵
    delete_nodes(net_array)

    #在action内导入：from action.delete_nodes import delete_nodes ，调用时net_array=delete_nodes(从data_reader读来的矩阵)
from analysis.data_reader import DataReader
from action.node_degree import node_degree
import os
import numpy as np
import json
import matplotlib.pyplot as plt


# 计算每个节点的coreness 参考networkx中解法
def node_coreness(adj_maxtrix, file_save):
    '''
    :np.where 返回的是tuple 去第一个元素
    :param adj_maxtrix: 邻接矩阵 动态变化 type:np.array
    :file_save : 保存数据的位置
    :return: coreness
    '''

    nodeDegree = node_degree(adj_matrix)
    nodeDegree = np.int64(nodeDegree)
    Degree = {i: [] for i in range(max(nodeDegree) + 1)}  # key是度 values是度为key的节点的集合
    coreness = {i: -1 for i in range(nodeDegree.shape[0])}

    for node, degree in enumerate(nodeDegree):
        Degree[degree].append(node)

    for key, values in Degree.items():
        print("degree:{}".format(key))
        if key == 0:
            continue
        else:
            for value in values:
                coreness[value] = key
                # 与这个点相连接的节点
                adj_nodes = np.where(adj_matrix[value] == 1)[0]
                for adj_node in adj_nodes:
                    if (nodeDegree[adj_node] > nodeDegree[value]):
                        Degree[nodeDegree[adj_node]].remove(adj_node)
                        nodeDegree[adj_node] -= 1
                        Degree[nodeDegree[adj_node]].append(adj_node)
    # 删除字典中第一个键为0的元素
    coreness.pop(0)
    # 保存文件到json
    file_save = os.path.join(file_save, 'coreness.json')
    with open(file_save, 'w') as fp:
        json.dump(coreness, fp)


# 计算节点的coreness分布
def node_coreness_dis(filename):
    path = os.getcwd()
    filepath = os.path.join(path, filename)
    dis = np.zeros((30))
    if (os.path.exists(filepath)):
        with open(filepath, 'r') as fp:
            coreness = json.load(fp)
            for key, value in coreness.items():
                dis[value] += 1
    else:
        print("no file")
        exit(0)

    y_axes = np.delete(dis, 0)
    plt.xticks(range(1, y_axes.shape[0] + 1))  # 显示横坐标
    plt.scatter(range(1, y_axes.shape[0] + 1), y_axes)
    print(y_axes)
    plt.xlabel("coreness")
    plt.ylabel("nodes number of coreness")
    plt.show()


if __name__ == "__main__":
    '''
    adj_matrix 中 index就是真实的node编号 index=1 代表node 1
    '''
    data = DataReader()

    # 保存coreness文件的位置
    file_save = '../data/'

    # 保存的coreness文件名
    filename = '../data/coreness.json'
    adj_matrix = data.data_reader()
    coreness = node_coreness(adj_matrix, file_save)
    node_coreness_dis(filename)

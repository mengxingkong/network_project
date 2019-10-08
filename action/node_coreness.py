from analysis.data_reader import DataReader
from action.node_degree import node_degree
import os
import numpy as np
import json
import matplotlib.pyplot as plt
import sys

rootPath = os.path.dirname(__file__)
sys.path.append(rootPath)

# from action.delete_nodes import delete_nodes


# 计算每个节点的coreness 参考networkx中解法
def node_coreness(adj_matrix):
    '''
    :np.where 返回的是tuple 去第一个元素
    :param adj_matrix: 邻接矩阵 动态变化 type:np.array
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

        for value in values:
            coreness[value] = key
            # 与这个点相连接的节点
            adj_nodes = np.where(adj_matrix[value] == 1)[0]
            for adj_node in adj_nodes:
                if (nodeDegree[adj_node] > nodeDegree[value]):
                    Degree[nodeDegree[adj_node]].remove(adj_node)
                    nodeDegree[adj_node] -= 1
                    Degree[nodeDegree[adj_node]].append(adj_node)
    # 删除字典中第一个键为0的元素 1: 2: .... 3031:
    coreness.pop(0)
    return coreness
    # 保存文件到json
    # file_save = os.path.join(file_save, 'coreness.json')
    # with open(file_save, 'w') as fp:
    #     json.dump(coreness, fp)


#保存coreness内容为前端的json数据格式
def write_corenss_tofile(coreness, rootPath='../data/coreness/corenss_distribution.json'):
    '''

    :param coreness:
    :param rootPath: 根目录 比如data/coreness/
    :return:
    '''

    # 保存的文件名
    # filename = "corenss_distribution.json"
    # file_path = os.path.join(rootPath, filename)
    file_path = rootPath
    max_axes = max(coreness.values())
    dis = [0 for _ in range(1, max_axes + 1)]  # 左闭右开
    print(len(dis))
    for key, value in coreness.items():
        dis[value - 1] += 1

    coreness_dict = {'x': [i for i in range(1, max_axes + 1)], 'y': dis}

    with open(file_path, 'w') as fp:
        json.dump(coreness_dict, fp)


# 计算节点的coreness分布
def node_coreness_dis(coreness, title):
    '''
    :param title: 折线图的title
    :return:
    '''
    dis = np.zeros((30))

    for key, value in coreness.items():
        dis[value] += 1

    y_axes = np.delete(dis, 0)
    plt.xticks(range(1, y_axes.shape[0] + 1))  # 显示横坐标
    # 散点图
    # plt.scatter(range(1, y_axes.shape[0] + 1), y_axes)
    # 折线图
    plt.plot(range(1, y_axes.shape[0] + 1), y_axes, 'o-')
    print(y_axes)
    plt.title(title)
    plt.xlabel("coreness")
    plt.ylabel("nodes number of coreness")
    plt.show()


if __name__ == "__main__":
    '''
    adj_matrix 中 index就是真实的node编号 index=1 代表node 1
    '''
    data = DataReader()
    # title = "coreness distribution(70% nodes deleted)"

    title = "coreness distribution (99% nodes deleted)"

    # 传入邻接矩阵
    adj_matrix = data.data_reader()


    # 随机删除节点
    # tem_matrix = delete_nodes(adj_matrix)

    coreness = node_coreness(adj_matrix)

    # coreness的分布
    node_coreness_dis(coreness, title)

    # 保存文件到data/coreness/
    # rootPath = '../data/coreness/'
    rootPath = '../data/coreness/corenss_distribution.json'
    # write_corenss_tofile(coreness, rootPath)

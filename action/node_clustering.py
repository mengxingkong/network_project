import sys
import os
from analysis.data_reader import DataReader
from action.networkx_pratice import create_graph
import math
import numpy as np
import networkx as nx
import json


# calculate clustering coefficient
# 计算节点的聚类系数就是计算节点 相邻节点对相邻个数和所有相邻节点对数的比值
def cal_clustring(adj_matrix):
    '''

    :param adj_matrix: 邻接矩阵
    :return: 节点的clustering coefficient
    '''

    tem_matrix = adj_matrix
    size = adj_matrix.shape[0]  # adj_matrix 的size是3032 节点的范围是3031
    clustering = {i: -1.0 for i in range(1, size)}  # clustering 长度是1-3031
    for index, _ in enumerate(tem_matrix):
        if (index == 0): continue
        adj_nodes = np.where(tem_matrix[index] == 1)[0]  # 与node相邻的node集合
        fenmu = adj_nodes.shape[0]  #
        # math.factorial(fenmu)
        fenzi = 0
        for sub_node1 in adj_nodes:  #
            for sub_node2 in adj_nodes:
                if (sub_node1 == sub_node2):
                    continue
                else:
                    if (tem_matrix[sub_node1, sub_node2] == 1):
                        fenzi += 1
        if (fenzi == 0):
            clustering[index] = 0
        else:
            # print(fenzi)
            fenzi = fenzi / 2
            clu_fenmu = math.factorial(fenmu) / (
                        math.factorial(fenmu - 2) * math.factorial(2))  # 分母是从与index相邻节点任取2个点的组合数
            clustering[index] = np.float(fenzi / clu_fenmu)
    with open("../data/clustering coefficient.json", 'w') as fp:  # 结果保存在data文件夹下的clustering coefficient.json中
        json.dump(clustering, fp)
    return clustering


# node聚类系数的属性
def clu_pro(filepath=None):
    '''

    :param filepath: 聚类系数json文件保存位置
    :return:最大值和平均值
    '''
    if (filepath == None):
        clustering = cal_clustring(adj_matrix)
    else:
        with open(filepath, 'r') as fp:
            clustering = json.load(fp)

    sum_num = sum(clustering.values())
    max_num = max(clustering.values())
    num = len(clustering)
    ave = float(sum_num / num)
    return max_num, ave


if __name__ == "__main__":
    filename = "../data/clustering coefficient.json"
    data = DataReader()
    adj_matrix = data.data_reader()
    my_cal = cal_clustring(adj_matrix)
    max_num, ave_num = clu_pro(filename)
    print("节点聚类系数最大值{}, 平均值{}".format(max_num, ave_num))
    # 与nexworkx进行对比
    # graph = create_graph()
    # nx_result = nx.clustering(graph)
    # for key, value in my_cal.items():
    #     print(my_cal[key]-nx_result[key])

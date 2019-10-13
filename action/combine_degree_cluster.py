import sys 
import os
import math
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import numpy as np
from analysis.data_reader import DataReader
import json
from node_degree import node_degree

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
    # with open("../data/clustering coefficient.json", 'w') as fp:  # 结果保存在data文件夹下的clustering coefficient.json中
    #     json.dump(clustering, fp)
    return clustering

def write_degree_cluster_json(net_array, file_path="../data/degree_cluster/degree_cluster.json"):
    degree_array = node_degree(net_array)
    clu_array = cal_clustring(net_array)
    node_list = list()
    for i in range(1, degree_array.size):
        node_dict = {"name":str(i),"value":clu_array[i],"symbolSize":degree_array[i]}
        node_list.append(node_dict)
    all_node_degree_json = json.dumps(node_list)
    with open(file_path, 'w') as f:
        f.write(all_node_degree_json)

if __name__ == "__main__":
    reader = DataReader()
    net_array = reader.data_reader()
    write_degree_cluster_json(net_array)

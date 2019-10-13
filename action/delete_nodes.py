import numpy as np
import math
import re
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from analysis.data_reader import DataReader
from action.node_degree import node_degree, degree_distribution, write_node_degree_distribution_to_file
from action.node_distance import NetDistance
from action.node_coreness import node_coreness, write_corenss_tofile
from action.node_clustering import cal_clustring, write_cluster_tofile


# 随机删除number个节点，每删除一个节点去掉矩阵的对应行和列
# @return 删除节点后的矩阵 @param 要删除的节点数，原矩阵
def delete_node_random(number, net_array):
    if number == 0:
      return net_array
    size = net_array.shape[0]
    # 根据概率随机生成 np.random.choice(size, int, replace=False, p=[0.1, 0, 0.3, 0.6, 0])
    # 随机生成由x个不重复的数组成的数组（取值范围在1-矩阵的节点个数）
    random_number = np.random.choice(np.arange(1, size + 1), number, replace=False)

    # 随机生成了x个数，删除其对应的n列和n行
    net_array = np.delete(net_array, random_number, axis=1)
    net_array = np.delete(net_array, random_number, axis=0)
    return net_array


# 获得需要删除的比例，调用随机删除节点函数进行删除
# @return 删除节点后的矩阵 @param net_array原矩阵 proportion要删除的比例
def delete_nodes(net_array, proportion = -1):
    nodes_number = net_array.shape[0]
    if proportion < 0:
       proportion = input('please enter the proportion of the node you want to delete ')

    delete_nodes_number = 0
    is_number = True
    if not isinstance(proportion, (int, float)):
      pattern = re.compile(r'^[\+]?\d+(\.\d+)?$')
      is_number = pattern.match(proportion)
    while not is_number or float(proportion) > 1.0 or float(proportion) < 0.0:
        proportion = input('please enter the proportion of the node you want to delete ')
    else:
        delete_nodes_number = math.ceil(float(proportion) * nodes_number)

    net_array = delete_node_random(delete_nodes_number, net_array)
    print(
        'deleted {0} nodes, which account for {1} of the total number of nodes'.format(delete_nodes_number, proportion))

    return net_array


if __name__ == "__main__":
    reader = DataReader()
    net_array = reader.data_reader()

    for i in [0.001, 0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
      # 删除i比例的节点
      nodes_deleted = delete_nodes(net_array, i)

      # 生成对应的度分布
      node_degree_distribution = degree_distribution(node_degree(nodes_deleted))
      node_degree_path = "../data/attack/degree_distribution_{}.json".format(i)
      # 生成degree_distribution_删除比例.json文件
      write_node_degree_distribution_to_file(node_degree_distribution, node_degree_path)


      # 生成对应的coreness
      coreness = node_coreness(nodes_deleted)
      coreness_path = "../data/attack/coreness_distribution_{}.json".format(i)
      write_corenss_tofile(coreness, coreness_path)

      # 生成对应的node_clustering
      node_clustering = cal_clustring(nodes_deleted)
      cluster_path = "../data/attack/cluster_{}.json".format(i)
      write_cluster_tofile(node_clustering, cluster_path)

      # 生成distance_distribution_删除比例.json文件
      net_distance = NetDistance(nodes_deleted)
      all_dict = net_distance.all_pair_node_distance()
      distri_array = net_distance.all_pair_lenth_distribution(all_dict)
      node_distance_path = "../data/attack/distance_distribution_{}.json".format(i)
      net_distance.write_distance_distribution_to_file(distri_array, node_distance_path)
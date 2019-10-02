from scipy.io import mmread
import os
import sys
import numpy as np
import pandas as pd

class DataReader(object):

    def __init__(self, data_dir="./../data", data_file_mtx="web-edu.mtx", data_file_npy="net_matrix.npy"):
        self.data_dir = data_dir
        self.mtx_file_path = os.path.join(data_dir,data_file_mtx)
        self.npy_file_path = os.path.join(data_dir,data_file_npy)

    # 在 原来的 mtx 文件 每行后面加 1
    def pre_process(self, result_file="web-edu-process.mtx"):
        result_path = os.path.join(self.data_dir, result_file)
        if os.path.exists(self.mtx_file_path):
            fread = open(self.mtx_file_path,'r')
        else:
            try:
                sys.exit(0)
            except:
                print("数据文件不存在")
        fwrite = open(result_path,'w')
        lines = fread.readlines()
        for i, line in enumerate(lines):
            if i<2:
                fwrite.write(line)
            else:
                fwrite.write(line.strip("\n")+" 1"+"\n")

    # 加载 .npy 文件 返回 numpy 数组
    def data_reader(self):
        net_array = np.load(self.npy_file_path)
        return net_array
        
       
    # 将 mtx 文件 按行读取，然后存成 numpy 数组，保存为 .npy文件
    def mtx2npy(self):
        if os.path.exists(self.mtx_file_path):
            f = open(self.mtx_file_path,'r')
        else:
            try:
                sys.exit(0)
            except:
                print("数据文件不存在")

        lines = f.readlines()
        total_info = lines[1].split(' ')
        width,height,edges = total_info[0], total_info[1], total_info[2]
        print(width,height,edges)
        net_array = np.zeros([int(width)+1, int(height)+1])
        for line in lines[2:]:
            x,y = line.split(' ')[0], line.split(' ')[1]
            net_array[int(x)][int(y)] = 1
            net_array[int(y)][int(x)] = 1
        np.save(os.path.join(self.data_dir, "net_matrix.npy"),net_array)
        

# 测试 数据加载类
if __name__ == "__main__":
    
    reader = DataReader()
    reader.mtx2npy() #执行一次 保存为 npy 文件就行了
    net_array = reader.data_reader()
    print(net_array.shape)
    print(np.sum(net_array)) # 输出数组总和为 6474 说明 加载的边数是对的

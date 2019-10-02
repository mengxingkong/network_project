from pandas import DataFrame

# 尝试使用 pandas 的版本
def load_data():
    '''
    从原始文件中读入数据并且保存
    :return:
    '''
    file_path = "data/" # 输入文件所在文件夹
    file_name = file_path + "web-edu.mtx"

    df = DataFrame(0, columns=range(1, 3032), index=range(1, 3032))\

    with open(file_name) as f:
        lines = f.readlines()
        lines = lines[2:]
        for line in lines:
            line = line.strip().split(' ')
            df.loc[int(line[0]), int(line[1])] = 1; df.loc[int(line[1]), int(line[0])] = 1
    df.to_csv("data.csv")

if __name__ == "__main__":
    load_data()



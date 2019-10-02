import sys
sys.path.append('./action')
from delete_nodes import delete_nodes
from node_coreness import node_coreness
from node_degree import node_degree

def select_action(action):
    action_list = ['node_degree', 'node_coreness', 'delete_nodes']
    if action < 1 :
        return
    globals()[action_list[action - 1]]()
    return


def show_action():
    action_number = 4
    print(
        'Please select one number\n 1. Show node-degree distribution\n 2. Show node coreness\n 3. Random delete nodes\n 4. End')
    action = input("Please enter：")

    while not action.isdigit() or int(action) != 4:
        if action.isdigit() and int(action) > 0 and int(action) <= action_number:
            select_action(int(action))
            action = input("Please enter：")
        else:
            print(
                'Please select one number\n 1. Show node-degree distribution\n 2. Show node coreness\n 3. Random delete nodes\n 4. End')
            action = input("Please enter：")
    else:
        print('Thanks')
    return


if __name__ == "__main__":
    show_action()





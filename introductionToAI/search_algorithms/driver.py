'''
Author: zhushun0008
Email: zhushun0008@gmail.com
'''

import math
import sys
import resource
import time
import codecs
#### SKELETON CODE ####

## The Class that Represents the Puzzle

class PuzzleState(object):
    """docstring for PuzzleState"""

    def __init__(self, config, n, parent=None, action="Initial", cost=0):

        if n * n != len(config) or n < 2:
            raise Exception("the length of config is not correct!")

        self.n = n

        self.cost = cost

        self.parent = parent

        self.action = action

        self.dimension = n

        self.config = config

        self.children = []

        for i, item in enumerate(self.config):

            if item == 0:
                self.blank_row = int(i / self.n)

                self.blank_col = int(i % self.n)

                break

    def display(self):

        for i in range(self.n):

            line = []

            offset = i * self.n

            for j in range(self.n):
                line.append(self.config[offset + j])

            print(line)

    def move_left(self):

        if self.blank_col == 0:

            return None

        else:

            blank_index = int(self.blank_row * self.n + self.blank_col)

            target = int(blank_index - 1)

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):

        if self.blank_col == self.n - 1:

            return None

        else:

            blank_index = int(self.blank_row * self.n + self.blank_col)

            target = int(blank_index + 1)

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):

        if self.blank_row == 0:

            return None

        else:

            blank_index = int(self.blank_row * self.n + self.blank_col)

            target = int(blank_index - self.n)

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):

        if self.blank_row == self.n - 1:

            return None

        else:

            blank_index = int(self.blank_row * self.n + self.blank_col)

            target = int(blank_index + self.n)

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):

        """expand the node"""

        # add child nodes in order of UDLR

        if len(self.children) == 0:

            up_child = self.move_up()

            if up_child is not None:
                self.children.append(up_child)

            down_child = self.move_down()

            if down_child is not None:
                self.children.append(down_child)

            left_child = self.move_left()

            if left_child is not None:
                self.children.append(left_child)

            right_child = self.move_right()

            if right_child is not None:
                self.children.append(right_child)

        return self.children


# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters

def writeOutput(statistics_dict):
    ### Student Code Goes here
    key_name_list = ["path_to_goal", "cost_of_path", "nodes_expanded", "search_depth", "max_search_depth", "running_time", "max_ram_usage"]
    with codecs.open('output.txt', "w+") as fw:
        for temp_key in key_name_list:
            temp_value = statistics_dict.get(temp_key)
            fw.write(temp_key)
            fw.write(": ")
            if type(temp_value) == list:
                fw.write("[{0}]".format("'" + "', '".join(temp_value) + "'"))
            else:
                fw.write(str(temp_value))
            fw.write("\n")



def bfs_search(initial_state):
    """BFS search"""

    ### STUDENT CODE GOES HERE ###
    fifo_queue = []
    fifo_queue.insert(0, initial_state)
    level_dict = {}
    level_dict[",".join(map(str, initial_state.config))] = 0
    max_search_depth = 0
    explored = set()
    num_node_expand = 0
    path_to_goal = []
    statistics_dict = {}
    while (len(fifo_queue) > 0):
        new_initial_state = fifo_queue.pop()
        parent = ",".join(map(str, new_initial_state.config))
        if test_goal(new_initial_state):
            temp_state = new_initial_state
            while(temp_state.parent):
                path_to_goal.insert(0, temp_state.action)
                temp_state = temp_state.parent
            statistics_dict["cost_of_path"] = new_initial_state.cost
            statistics_dict["nodes_expanded"] = num_node_expand
            statistics_dict["search_depth"] = level_dict[",".join(map(str, new_initial_state.config))]
            statistics_dict["path_to_goal"] = path_to_goal
            statistics_dict["max_search_depth"] = max_search_depth
            return statistics_dict
        explored.add(parent)

        new_initial_state.expand()
        num_node_expand += 1
        # print("\n")
        # print("num_node_expand: ", num_node_expand)
        for child in new_initial_state.children:
            if (",".join(map(str, child.config)) not in explored and child not in fifo_queue):
                child.parent = new_initial_state
                level_dict[",".join(map(str, child.config))] = level_dict[",".join(map(str, child.parent.config))] + 1
                if (max_search_depth < level_dict[",".join(map(str, child.config))]):
                    max_search_depth = level_dict[",".join(map(str, child.config))]
                # if (test_goal(child)):
                #     return True
                fifo_queue.insert(0, child)
                # print(",".join(map(str, fifo_queue[0].config)))


def dfs_search(initial_state):
    """DFS search"""

    ### STUDENT CODE GOES HERE ###

    stack = []
    stack.append(initial_state)
    explored = set()
    num_node_expand = 0
    path_to_goal = []
    statistics_dict = {}
    while (len(stack) > 0):
        new_initial_state = stack.pop()
        parent = ",".join(map(str, new_initial_state.config))
        if test_goal(new_initial_state):
            temp_state = new_initial_state
            while(temp_state.parent):
                path_to_goal.insert(0, temp_state.action)
                temp_state = temp_state.parent
            statistics_dict["cost_of_path"] = new_initial_state.cost
            statistics_dict["nodes_expanded"] = num_node_expand
            statistics_dict["search_depth"] = len(path_to_goal)
            statistics_dict["path_to_goal"] = path_to_goal
            statistics_dict["max_search_depth"] = len(path_to_goal) + 1
            return statistics_dict
        explored.add(parent)

        new_initial_state.expand()
        num_node_expand += 1
        # print("\n")
        # print("num_node_expand: ", num_node_expand)
        for child in new_initial_state.children:
            if (",".join(map(str, child.config)) not in explored and child not in stack):
                child.parent = new_initial_state
                # if (test_goal(child)):
                #     return True
                stack.append(child)
                # print(",".join(map(str, fifo_queue[0].config)))


def A_star_search(initial_state):
    """A * search"""

    ### STUDENT CODE GOES HERE ###


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""

    ### STUDENT CODE GOES HERE ###


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""

    ### STUDENT CODE GOES HERE ###


def test_goal(puzzle_state):
    """test the state is the goal state or not"""

    ### STUDENT CODE GOES HERE ###
    if puzzle_state.config == (0, 1, 2, 3, 4, 5, 6, 7, 8):
        return True
    return False


# Main Function that reads in Input and Runs corresponding Algorithm

def main():
    sm = sys.argv[1].lower()

    begin_state = sys.argv[2].split(",")

    begin_state = tuple(map(int, begin_state))

    size = int(math.sqrt(len(begin_state)))

    hard_state = PuzzleState(begin_state, size)

    if sm == "bfs":
        start_time = time.time()
        statistics_dict = bfs_search(hard_state)
        end_time = time.time()
        statistics_dict["running_time"] = end_time - start_time
        statistics_dict["max_ram_usage"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
        writeOutput(statistics_dict)

    elif sm == "dfs":

        dfs_search(hard_state)

    elif sm == "ast":

        A_star_search(hard_state)

    else:

        print("Enter valid command arguments !")


if __name__ == '__main__':
    main()

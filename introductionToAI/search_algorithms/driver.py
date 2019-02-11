'''
Author: zhushun0008
Email: zhushun0008@gmail.com
'''

import math
import sys
import resource
import time
import codecs
import Queue as Q


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
    key_name_list = ["path_to_goal", "cost_of_path", "nodes_expanded", "search_depth", "max_search_depth",
                     "running_time", "max_ram_usage"]
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
    fifo_queue_set = set()
    str_init_state = ",".join(map(str, initial_state.config))
    fifo_queue_set.add(str_init_state)
    level_dict = {}
    level_dict[str_init_state] = 0
    max_search_depth = 0
    explored = set()
    num_node_expand = 0
    path_to_goal = []
    statistics_dict = {}
    while (len(fifo_queue) > 0):
        new_initial_state = fifo_queue.pop()
        str_new_init_state = ",".join(map(str, new_initial_state.config))
        fifo_queue_set.remove(str_new_init_state)
        if test_goal(new_initial_state):
            temp_state = new_initial_state
            while (temp_state.parent):
                path_to_goal.insert(0, temp_state.action)
                temp_state = temp_state.parent
            statistics_dict["cost_of_path"] = new_initial_state.cost
            statistics_dict["nodes_expanded"] = num_node_expand
            statistics_dict["search_depth"] = level_dict[",".join(map(str, new_initial_state.config))]
            statistics_dict["path_to_goal"] = path_to_goal
            statistics_dict["max_search_depth"] = max_search_depth
            return statistics_dict
        explored.add(str_new_init_state)

        new_initial_state.expand()
        num_node_expand += 1
        # print("\n")
        # print("num_node_expand: ", num_node_expand)
        for child in new_initial_state.children:
            child_state_str = ",".join(map(str, child.config))
            if (child_state_str not in explored) and (child_state_str not in fifo_queue_set):
                child.parent = new_initial_state
                level_dict[",".join(map(str, child.config))] = level_dict[",".join(map(str, child.parent.config))] + 1
                if (max_search_depth < level_dict[",".join(map(str, child.config))]):
                    max_search_depth = level_dict[",".join(map(str, child.config))]
                # if (test_goal(child)):
                #     return True
                fifo_queue.insert(0, child)
                fifo_queue_set.add(child_state_str)
                # print(",".join(map(str, fifo_queue[0].config)))


def dfs_search(initial_state):
    """DFS search"""

    ### STUDENT CODE GOES HERE ###
    stack = []
    stack.append(initial_state)
    stack_set = set()
    str_init_state = ",".join(map(str, initial_state.config))
    stack_set.add(str_init_state)
    explored = set()

    level_dict = {}
    level_dict[str_init_state] = 0
    max_search_depth = 0
    num_node_expand = 0
    path_to_goal = []
    statistics_dict = {}
    while len(stack) > 0:
        new_initial_state = stack.pop()
        str_new_init_config = ",".join(map(str, new_initial_state.config))
        stack_set.remove(str_new_init_config)
        # print("pop:  " + str_new_init_config)

        if test_goal(new_initial_state):
            temp_state = new_initial_state
            while (temp_state.parent):
                path_to_goal.insert(0, temp_state.action)
                temp_state = temp_state.parent
            statistics_dict["cost_of_path"] = new_initial_state.cost
            statistics_dict["nodes_expanded"] = num_node_expand
            statistics_dict["search_depth"] = level_dict[",".join(map(str, new_initial_state.config))]
            statistics_dict["path_to_goal"] = path_to_goal
            statistics_dict["max_search_depth"] = max_search_depth
            return statistics_dict

        explored.add(str_new_init_config)
        new_initial_state.expand()
        num_node_expand += 1
        # print("num_node_expand: ", num_node_expand)
        # reverse-UDLR order
        # print("\n")
        for child_index in reversed(range(len(new_initial_state.children))):
            child = new_initial_state.children[child_index]
            child_state_str = ",".join(map(str, child.config))
            if (child_state_str not in explored) and (child_state_str not in stack_set):
                # print("push: " + ",".join(map(str, child.config)))
                child.parent = new_initial_state
                level_dict[child_state_str] = level_dict[",".join(map(str, new_initial_state.config))] + 1

                # print("({0}, {1})".format(child_state_str, level_dict[",".join(map(str, child.config))]))
                if (max_search_depth < level_dict[child_state_str]):
                    max_search_depth = level_dict[child_state_str]
                # if (test_goal(child)):
                #     return True
                stack.append(child)
                stack_set.add(child_state_str)


def A_star_search(initial_state):
    """A * search"""

    ### STUDENT CODE GOES HERE ###
    priority_queue = Q.PriorityQueue()
    priority_queue.put((calculate_total_cost(initial_state), initial_state))
    priority_queue_set = set()
    str_init_state = ",".join(map(str, initial_state.config))
    priority_queue_set.add(str_init_state)
    explored = set()

    level_dict = {}
    level_dict[str_init_state] = 0
    max_search_depth = 0
    num_node_expand = 0
    path_to_goal = []
    statistics_dict = {}
    while not priority_queue.empty():
        new_initial_state = priority_queue.get()[1]
        str_new_init_config = ",".join(map(str, new_initial_state.config))
        priority_queue_set.remove(str_new_init_config)
        explored.add(str_new_init_config)
        # print("pop:  " + str_new_init_config)

        if test_goal(new_initial_state):
            temp_state = new_initial_state
            while (temp_state.parent):
                path_to_goal.insert(0, temp_state.action)
                temp_state = temp_state.parent
            statistics_dict["cost_of_path"] = new_initial_state.cost
            statistics_dict["nodes_expanded"] = num_node_expand
            statistics_dict["search_depth"] = level_dict[",".join(map(str, new_initial_state.config))]
            statistics_dict["path_to_goal"] = path_to_goal
            statistics_dict["max_search_depth"] = max_search_depth
            return statistics_dict

        new_initial_state.expand()
        num_node_expand += 1
        # print("num_node_expand: ", num_node_expand)
        # reverse-UDLR order
        # print("\n")
        for child in new_initial_state.children:
            child_state_str = ",".join(map(str, child.config))
            if (child_state_str not in explored) and (child_state_str not in priority_queue_set):
                # print("push: " + ",".join(map(str, child.config)))
                child.parent = new_initial_state
                level_dict[child_state_str] = level_dict[",".join(map(str, new_initial_state.config))] + 1

                # print("({0}, {1})".format(child_state_str, level_dict[",".join(map(str, child.config))]))
                if (max_search_depth < level_dict[child_state_str]):
                    max_search_depth = level_dict[child_state_str]
                # if (test_goal(child)):
                #     return True
                priority_queue.put((calculate_total_cost(child), child))
                priority_queue_set.add(child_state_str)


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""

    ### STUDENT CODE GOES HERE ###
    gn_cost = state.cost
    hn_cost = 0.0
    for i in xrange(len(state.config)):
        hn_cost += calculate_manhattan_dist(i, state.config[i], state.n)
    return gn_cost + hn_cost


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""

    ### STUDENT CODE GOES HERE ###
    idx_row = idx / n
    idx_col = idx % n
    value_row = value / n
    value_col = value % n
    return int(abs(value_row - idx_row) + abs(value_col - idx_col))


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
        start_time = time.time()
        statistics_dict = dfs_search(hard_state)
        end_time = time.time()
        statistics_dict["running_time"] = end_time - start_time
        statistics_dict["max_ram_usage"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
        writeOutput(statistics_dict)
    elif sm == "ast":
        start_time = time.time()
        statistics_dict = A_star_search(hard_state)
        end_time = time.time()
        statistics_dict["running_time"] = end_time - start_time
        statistics_dict["max_ram_usage"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
        writeOutput(statistics_dict)

    else:

        print("Enter valid command arguments !")


if __name__ == '__main__':
    main()

import numpy as np
import math
from random import choice

"""
0. heuristic = Manhattan distance
"""


class Node:
    def __init__(self, x, y, is_obstacle):
        self.x = x
        self.y = y
        self.is_obstacle = is_obstacle
        self.parent = None

    def calculate_heuristic(self, target_node):
        return abs(target_node.y - self.y) + abs(target_node.x - self.x)


class Scene:
    def __init__(self, input):
        self.nodes = []
        self.looking_list = []

        # since coordinate is the opposite way of indexing
        for y in range(input.shape[0]):
            for x in range(input.shape[1]):
                if input[y, x] == 1:
                    is_obstacle = True
                elif input[y, x] == 0:
                    is_obstacle = False
                else:
                    raise ValueError("index {}, {} has an invalid cell value".format(y, x))
                self.nodes.append(Node(x, y, is_obstacle))

        self.nodes_print = self.nodes

    def get_node(self, x, y):
        for i in self.nodes_print:
            if x == i.x and y == i.y:
                return i

        raise ValueError("No node with index ({}, {})".format(x, y))

    def calculate_distance(self, current_node, steps=0):
        if current_node.parent is None:
            return steps
        else:
            return self.calculate_distance(current_node.parent, steps=steps + 1)

    def create_path(self, current_node, end_node):
        self.nodes.remove(current_node)  # remove visited nodes

        if current_node == end_node:
            print("The shortest distance is: {}".format(self.calculate_distance(end_node)))
            print("The shortest path is: {}".format(self.show_path(end_node)))
            return
        else:
            possible_x = [current_node.x + 1, current_node.x, current_node.x - 1]
            possible_y = [current_node.y + 1, current_node.y, current_node.y - 1]
            for i in self.nodes:
                if i.x in possible_x and i.y in possible_y and not i.is_obstacle:
                    i.parent = current_node
                    self.looking_list.append(i)

            # remove duplicates
            self.looking_list = list(dict.fromkeys(self.looking_list))

            smallest_dist = math.inf
            opt_node = None
            for j in self.looking_list:
                if j.calculate_heuristic(end_node) + self.calculate_distance(j) < smallest_dist:
                    smallest_dist = j.calculate_heuristic(end_node) + self.calculate_distance(j)
                    opt_node = j

            if opt_node is None:
                print("Cannot find a way to reach destination")

                # TODO:
                # for i = 1 to 20
                # in each iteration, remove i obstacles, see whether there is a path using create_path()
                # if there is a path, return i and the removed obstacles
                return
            else:
                self.looking_list.remove(opt_node)

            return self.create_path(opt_node, end_node)

    def show_path(self, end_node):
        current_node = end_node
        path = []
        while current_node.parent is not None:
            path.insert(0, (current_node.x, current_node.y))
            current_node = current_node.parent
        path.insert(0, (current_node.x, current_node.y))
        return path


def phase_1():
    # the scene is input as an array
    # if the value of a cell is 1, it's an obstacle

    test = np.zeros((10, 10), dtype=int)
    test[7, 7] = 1
    test[7, 8] = 1
    test[7, 9] = 1
    test[8, 7] = 1
    print(test)
    sc = Scene(test)
    start_node = sc.get_node(0, 0)
    end_node = sc.get_node(9, 9)
    sc.create_path(start_node, end_node)




def phase_2():
    # the scene is input as an array
    # if the value of a cell is 1, it's an obstacle
    test = np.zeros((10, 10), dtype=int)
    test[7, 7] = 1
    test[7, 8] = 1
    test[7, 9] = 1
    test[8, 7] = 1

    # add random obstacles
    added_obs = 0
    while added_obs < 20:
        x = np.random.randint(10)
        y = np.random.randint(10)
        if test[y, x] == 0:
            added_obs += 1
            test[y, x] = 1

    print(test)
    sc = Scene(test)
    start_node = sc.get_node(0, 0)
    end_node = sc.get_node(9, 9)
    sc.create_path(start_node, end_node)


if __name__ == "__main__":
    # phase_1()
    phase_2()

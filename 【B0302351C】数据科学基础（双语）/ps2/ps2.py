# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
'''结点代表每一个建筑，主要就是地图上标记出的建筑
边代表着两个建筑物之间的路线，从出发地到目的地的路
距离代表着两建筑物之间的距离，也意味着从起始地到目的地的时间，
其中距离包括全程距离和户外距离两种'''
#
# Answer:
#


# Problem 2b: Implementing load_map
# Problem 2b: Implementing load_map
def load_map(map_filename):
    print("Loading map from file...")
    # 创建一个空的Digraph用来存result
    result = Digraph()
    # 打开文件
    with open(map_filename) as file:
        # 将数据按行分开
        read_data = file.read().split("\n")
        read_data = read_data[:-1]
        # 逐行处理数据
        for entry in read_data:
            # 通过空格分开数据，分别为source destination distance out_distance
            raw_data = entry.split(" ")
            # 将具体数据读取出来
            src = Node(raw_data[0])
            dest = Node(raw_data[1])
            total = int(raw_data[2])
            outdoor = int(raw_data[3])
            # 检查源节点和目标节点是否已经存在于图中，如果不存在则添加到图中
            if not result.has_node(src):
                result.add_node(src)
            if not result.has_node(dest):
                result.add_node(dest)

            # 将边加入图
            edge = WeightedEdge(src, dest, total, outdoor)
            result.add_edge(edge)
    # 关闭文件
    file.close()
    # 返回结果
    return result

    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """

    # TODO
# print("Loading map from file...")
#
# # Problem 2c: Testing load_map
# # Include the lines used to test load_map below, but comment them out
# graph = load_map("test_load_map.txt")
# print(graph)


#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
'''这个问题中我们旨在根据起始和终止点找到最短路径以及最短路径长度。
我们需要找到在满足限制条件的前提下的最短路径。目标函数是get_best_path，
限制条件是户外路线长度需要不大于某一给定值且路径应尽可能的短。'''


# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist, best_path):
    # 如果有点不在图中，riase Valueerror
    if not (digraph.has_node(Node(start)) and digraph.has_node(Node(end))):
        raise ValueError
    # path是一个[[list of strings], int, int],含义为[已经走的路,总的路长，总的室外路长]
    # 因此将其分离出来
    curr_path, total_dist, outdoor_dist = path
    # 将当前start加入到curr_path中
    curr_path = curr_path + [start]

    # 递归终止条件：start与end相等
    if start == end:
        # 如果当前总距离小于best_dist，则更换最佳路径
        if total_dist <= best_dist:
            best_dist = total_dist
            best_path = curr_path
            return (best_path, best_dist)
        # 否则不做处理
        return None
        # 否则进行递归判断，继续探路
    else:
        ## 将所有子节点遍历一次
        for edge in digraph.get_edges_for_node(Node(start)):
            # 如果该子节点之前还没有走过的话
            if str(edge.get_destination()) not in curr_path:

                # 以此为start开始探测
                new_total_distance = total_dist + edge.get_total_distance()
                new_outdoor_distance = outdoor_dist + edge.get_outdoor_distance()
                outdoor_distance_left = max_dist_outdoors - new_outdoor_distance

                # 如果户外距离尚未超出限制
                if (outdoor_distance_left >= 0 and new_total_distance <= best_dist):

                    # 以新节点为出发点继续探路
                    new_path = get_best_path(digraph, str(edge.get_destination()), end,
                                             [curr_path, new_total_distance, new_outdoor_distance],
                                             outdoor_distance_left, best_dist, best_path)

                    if new_path != None:
                        best_path, best_dist = new_path

    return (best_path, best_dist)

    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    # TODO
    pass


# Problem 3c: Implement directed_dfs
# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    #初始化path
    path = [[],0,0]
    #利用已经完成的get_best_path得到最优解
    best_path_result = get_best_path(digraph, start, end, path, max_dist_outdoors, max_total_dist, None)
    #如果最优解符合题意，则返回路径
    if best_path_result[0] != None and best_path_result[1] <= max_total_dist:
        return best_path_result[0]
    #否则返回Valueeror
    else:
        raise ValueError

    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    # TODO
    pass


# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()

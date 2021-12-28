from os import path
from string import ascii_uppercase


class Node:
    def __init__(self, name: str):
        self.visited = False
        self.neighbors = set()
        self.name = name
        self.big = any((c in ascii_uppercase for c in name))

    def __hash__(self) -> int:
        return int(self.name, 36)

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, o) -> bool:
        return self.name == o.name


class CaveGraph:
    def __init__(self):
        self.nodes = {}
        self.small_visited_twice = False

    def __getitem__(self, key):
        return self.nodes[key]

    def __setitem__(self, key, value):
        self.nodes[key] = value

    def values(self):
        return self.nodes.values()

    def __contains__(self, item):
        return item in self.nodes


def read_file(name: str) -> CaveGraph:
    with open(name) as f:
        graph = CaveGraph()

        for line in f.read().split("\n"):
            src, dst = line.split("-")
            if src not in graph:
                graph[src] = Node(src)
            if dst not in graph:
                graph[dst] = Node(dst)

            graph[src].neighbors.add(graph[dst])
            graph[dst].neighbors.add(graph[src])

        return graph


def copy_graph(graph: CaveGraph, small_visited_twice: bool = False) -> CaveGraph:
    new_graph = CaveGraph()
    new_graph.nodes = {node.name: Node(node.name) for node in graph.values()}
    new_graph.small_visited_twice = graph.small_visited_twice or small_visited_twice

    for node in graph.values():
        new_graph[node.name].visited = node.visited
        for n in graph[node.name].neighbors:
            new_graph[node.name].neighbors.add(new_graph[n.name])

    return new_graph


def discover_node(graph: CaveGraph, node: Node, target: Node, depth: int = 1) -> int:
    # print(node.name, end="\t")
    if node == target:
        return 1

    source = graph["start"]
    destination = graph["end"]

    node.visited = True
    reachable = [
        neighbor
        for neighbor in node.neighbors
        if neighbor.big
        or not neighbor.visited
        or (
            not graph.small_visited_twice
            and neighbor != source
            and neighbor != destination
        )
    ]

    paths = 0
    for i, n in enumerate(reachable):
        # if i > 0:
        # print("\n" + (2 * depth - 1) * "\t", end="")
        # print("->", end="\t")
        graph_copy = copy_graph(graph, not n.big and n.visited)
        paths += discover_node(graph_copy, graph_copy[n.name], target, depth + 1)

    return paths


def count_paths(graph: CaveGraph) -> int:
    source = graph["start"]
    destination = graph["end"]

    if not source or not destination:
        raise Error("Something is not right")

    return discover_node(graph, source, destination)


print("This is going to run for a while.")

graph = read_file(path.join(path.dirname(__file__), "./input-1.txt"))
paths = count_paths(graph)
assert paths == 36

graph = read_file(path.join(path.dirname(__file__), "./input-2.txt"))
paths = count_paths(graph)
assert paths == 103

graph = read_file(path.join(path.dirname(__file__), "./input-3.txt"))
paths = count_paths(graph)
assert paths == 3509

graph = read_file(path.join(path.dirname(__file__), "./input-4.txt"))
paths = count_paths(graph)
print(paths)

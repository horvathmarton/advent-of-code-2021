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


CaveGraph = dict[Node]


def read_file(name: str) -> CaveGraph:
    with open(name) as f:
        graph = {}

        for line in f.read().split("\n"):
            src, dst = line.split("-")
            if src not in graph:
                graph[src] = Node(src)
            if dst not in graph:
                graph[dst] = Node(dst)

            graph[src].neighbors.add(graph[dst])
            graph[dst].neighbors.add(graph[src])

        return graph


def copy_graph(graph: CaveGraph) -> CaveGraph:
    new_graph = {node.name: Node(node.name) for node in graph.values()}

    for node in graph.values():
        new_graph[node.name].visited = node.visited
        for n in graph[node.name].neighbors:
            new_graph[node.name].neighbors.add(new_graph[n.name])

    return new_graph


def discover_node(graph: CaveGraph, node: Node, target: Node, depth: int = 1) -> int:
    # print(node.name, end="\t")
    if node == target:
        return 1

    node.visited = True
    reachable = [
        neighbor for neighbor in node.neighbors if neighbor.big or not neighbor.visited
    ]

    paths = 0
    for i, n in enumerate(reachable):
        # if i > 0:
        # print("\n" + (2 * depth - 1) * "\t", end="")
        # print("->", end="\t")
        graph_copy = copy_graph(graph)
        paths += discover_node(graph_copy, graph_copy[n.name], target, depth + 1)

    return paths


def count_paths(graph: CaveGraph) -> int:
    source = graph["start"]
    destination = graph["end"]

    if not source or not destination:
        raise Error("Something is not right")

    return discover_node(graph, source, destination)


graph = read_file(path.join(path.dirname(__file__), "./input-1.txt"))
paths = count_paths(graph)
assert paths == 10

graph = read_file(path.join(path.dirname(__file__), "./input-2.txt"))
paths = count_paths(graph)
assert paths == 19

graph = read_file(path.join(path.dirname(__file__), "./input-3.txt"))
paths = count_paths(graph)
assert paths == 226

graph = read_file(path.join(path.dirname(__file__), "./input-4.txt"))
paths = count_paths(graph)
print(paths)

import copy
import networkx as nx
import matplotlib.pyplot as plt
import  time

class Sequence:
    def __init__(self, sequence):
        self.sequence = sequence
        self.isChildren = False
        self.name = ','.join(map(str, self.sequence))
        self.length = len(sequence) - sequence.count(0)
        self.parents = []


def bfs(sequence):
    stack = [sequence]
    while stack:
        current_sequence = stack.pop(0)
        k = 0
        while k < current_sequence.length -1:
            index = [i for i, value in enumerate(current_sequence.sequence) if value < current_sequence.sequence[k]]
            index = -1 if len(index) == 0 else index[0]
            if index > -1:
                stack = get_queue(index, k, current_sequence, stack)
            index = len(current_sequence.sequence) - current_sequence.sequence[::-1].index(
                current_sequence.sequence[k]) - 1
            stack = get_queue(index, k, current_sequence, stack)
            index = [i for i, j in enumerate(current_sequence.sequence[:: -1])if j != current_sequence.sequence[k]]
            index = -1 if len(index) == 0 else len(current_sequence.sequence) - index[0] - 1
            if index > -1:
                stack = get_queue(index, k, current_sequence, stack)
            if k == current_sequence.length - 2 and not current_sequence.isChildren:
                maximum_graphic_sequences.append(current_sequence)
            k += 1


def get_queue(index_reduction, index_increase, node, stack):
    sequence = node.sequence
    if ((index_increase != index_reduction and index_reduction > 0
        and index_reduction < node.length-1 and sequence[index_reduction] - 1 >= sequence[index_reduction+1])
		or index_reduction == node.length - 1 and sequence[index_increase] - sequence[index_reduction] == 0
		or index_reduction == node.length - 1 and index_reduction - index_increase == 1):
        if index_increase > 0 and sequence[index_increase - 1] >= sequence[index_increase] + 1 or index_increase == 0:
            copy_sequence = copy.deepcopy(sequence)
            copy_sequence[index_reduction] -= 1
            copy_sequence[index_increase] += 1

            if is_graphic_sequence(copy_sequence, node.length):
                name = ','.join(map(str, copy_sequence))
                node.isChildren = True

                if name not in used:
                    new_sequence = Sequence(copy_sequence)
                    stack.append(new_sequence)
                    used.append(new_sequence.name)
                    sequences.append(new_sequence)
                    find_graphs.update({new_sequence.name: []})

    return stack


def is_graphic_sequence(sequence, length_sequence):
    b = c = s = 0
    w = length_sequence
    i = 0
    while i < length_sequence:
        b += sequence[i]
        c = c + w - 1
        while sequence[w-1] <= i < w - 1:
            s += sequence[w-1]
            c -= i + 1
            w -= 1
        if b > c + s:
            return False
        if w-1 == i:
            return True
        i += 1
    return False


def generating_maximal_graphs():
    max_graphs = []
    for sequence in maximum_graphic_sequences:
        j = 0
        graph = nx.Graph()
        graph.add_edge(0, 1)
        while j < sequence.length:
            degree = sequence.sequence[j]
            i = 2
            while i <= degree:
                if graph.degree(j) < degree and i != j:
                    graph.add_edge(j, i)
                i += 1
            j += 1

        max_graphs.append({'graph': graph, 'sequence': sequence.sequence, 'name': sequence.name})
    return max_graphs


def add_graph(sequence, graph, neighbor, vertex1, vertex2):
    if is_graphic_sequence(sequence, len(sequence) - sequence.count(0)):
        new_sequence = Sequence(sequence)
        new_graph = copy.deepcopy(graph)
        new_graph.add_edge(neighbor, vertex2)
        new_graph.remove_edge(vertex1, neighbor)
        if (True not in [nx.is_isomorphic(new_graph, g) for g in find_graphs[new_sequence.name]]):
            find_graphs[new_sequence.name].append(new_graph)
            graphs.append({'graph': new_graph, 'sequence': seq, 'name': new_sequence.name})


def fun(graphs):
    for graph in graphs:
        find_graphs[graph['name']].append(graph['graph'])

    while graphs:
        print(len(graphs))
        data_of_graph = graphs.pop(0)
        graph = data_of_graph['graph']
        sequence = copy.deepcopy(data_of_graph['sequence'])
        for vertex1 in graph.node:
            for neighbor in graph.neighbors(vertex1):
                for vertex2 in graph.node:
                    if (vertex2 != neighbor and vertex2 != vertex1 and graph.degree(vertex1) - graph.degree(vertex2) >= 1):
                        if(neighbor not in graph.adjacency_list()[vertex2] and sequence[vertex1] >= 1):
                            seq = copy.deepcopy(sequence)
                            seq[vertex1] -= 1
                            seq[vertex2] += 1
                            s = copy.deepcopy(seq)
                            s.sort(reverse=True)

                            new_sequence = Sequence(s)
                            new_graph = copy.deepcopy(graph)
                            new_graph.add_edge(neighbor, vertex2)
                            new_graph.remove_edge(vertex1, neighbor)
                            if (True not in [nx.is_isomorphic(new_graph, g) for g in find_graphs[new_sequence.name]]):
                                find_graphs[new_sequence.name].append(new_graph)
                                graphs.append({'graph': new_graph, 'sequence': seq, 'name': new_sequence.name })


                if(neighbor != len(sequence) - sequence.count(0) and sequence[vertex1] > 1):
                    seq = copy.deepcopy(sequence)
                    seq[vertex1] -= 1
                    seq[len(seq) - seq.count(0)] += 1
                    s = copy.deepcopy(seq)
                    s.sort(reverse=True)
                    new_sequence = Sequence(s)
                    new_graph = copy.deepcopy(graph)
                    new_graph.add_edge(neighbor, len(s) - s.count(0) - 1)
                    new_graph.remove_edge(vertex1, neighbor)
                    if (True not in [nx.is_isomorphic(new_graph, g) for g in find_graphs[new_sequence.name]]):
                        find_graphs[new_sequence.name].append(new_graph)
                        graphs.append({'graph': new_graph, 'sequence': seq, 'name': new_sequence.name})



def drawing_graphs():
    count = 1
    for name_of_graph in find_graphs:
        for graph in find_graphs[name_of_graph]:
            nx.draw(graph)
            name = '%d-%s.png' % (count, name_of_graph)
            plt.savefig(name)
            plt.clf()
            count += 1

start = time.time()
seq = Sequence([1] * 22)
used = []
sequences = []
find_graphs = {}
maximum_graphic_sequences = []
sequences.append(seq)
find_graphs.update({seq.name: []})
bfs(seq)
graphs = generating_maximal_graphs()
fun(graphs)
drawing_graphs()
end = time.time()
print(end - start)

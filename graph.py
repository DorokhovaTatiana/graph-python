import copy
import networkx as nx
import matplotlib.pyplot as plt


class Sequence:
    def __init__(self, sequence):
        self.sequence = sequence
        self.isChildren = False
        self.name = ','.join(map(str, self.sequence))
        self.length = len(sequence) - sequence.count(0)
        self.parents = []

used = []
sequences = []
maximumGraphicsSequence = []

def bfs(sequence):
    stack = [sequence]
    while stack:
        currentSequence = stack.pop(0)
        k = 0
        while k < currentSequence.length -1:
            index = [i for i, value in enumerate(currentSequence.sequence) if value < currentSequence.sequence[k]]
            index = -1 if len(index) == 0 else index[0]
            if index > -1:
                stack = get_queue(index, k, currentSequence, stack)
            index = len(currentSequence.sequence) - currentSequence.sequence[::-1].index(
                currentSequence.sequence[k]) - 1
            stack = get_queue(index, k, currentSequence, stack)
            index = [i for i, j in enumerate(currentSequence.sequence[:: -1])if j != currentSequence.sequence[k]]
            index = -1 if len(index) == 0 else len(currentSequence.sequence) - index[0] - 1
            if index > -1:
                stack = get_queue(index, k, currentSequence, stack)

            if (k == currentSequence.length - 2 and not currentSequence.isChildren):
                maximumGraphicsSequence.append(currentSequence)
                # print(currentSequence.name)
            k+=1


def get_queue(indexReduction, indexIncrease, node, stack):
    sequence = node.sequence
    if ((indexIncrease != indexReduction and indexReduction > 0
        and indexReduction < node.length-1 and sequence[indexReduction] - 1 >= sequence[indexReduction+1])
		or indexReduction == node.length - 1 and sequence[indexIncrease] - sequence[indexReduction] == 0
		or indexReduction == node.length - 1 and indexReduction - indexIncrease == 1):

        if (indexIncrease > 0 and sequence[indexIncrease - 1] >= sequence[indexIncrease] + 1 or indexIncrease == 0):
            copySequence = copy.deepcopy(sequence)
            copySequence[indexReduction] -= 1
            copySequence[indexIncrease] += 1

            if is_Graphic_Sequence(copySequence, node.length):
                name = ','.join(map(str, copySequence))
                node.isChildren = True

                if name not in used:
                    newSequence = Sequence(copySequence)
                    stack.append(newSequence)
                    used.append(newSequence.name)
                    sequences.append(newSequence)
                    findGraphs.update({newSequence.name: []})

                newSequence = [value for value in sequences if value.name == name][0]
                parent = { 'valueIncrease': copySequence[indexIncrease],
                         'indexReduction': indexReduction,
                        'sequence': node }
                newSequence.parents.append(parent)


    return stack

def is_Graphic_Sequence(sequence, lengthSequence):
    b = c = s = 0
    w = lengthSequence
    i = 0
    while i < lengthSequence:
        b+=sequence[i]
        c = c + w - 1
        while w - 1 > i and sequence[w-1] <= i:
            s+=sequence[w-1]
            c-= i + 1
            w-= 1
        if b > c + s:
             return False
        if w-1 == i:
            return True
        i+=1
    return False



def generatingMaximumGraphs():
    graphs = []
    for sequence in maximumGraphicsSequence:
        j = 0
        graph = nx.Graph()
        graph.add_edge(0, 1)
        while j < sequence.length:
            degree = sequence.sequence[j]
            i = 2
            while i <= degree:
                if graph.degree(j) < degree and i != j:
                    graph.add_edge(j, i)
                i+=1
            j+=1

        graphs.append({'graph': graph, 'sequence': sequence})
    return graphs
            

def all_drawing_Sequence(graphs):
    for graph in graphs:
        g = findGraphs[graph['sequence'].name]
        g.append(graph['graph']);
        findGraphs.update({graph['sequence'].name :g})
    count = 1
    while graphs:
        print("count ==", 1)
        data = graphs.pop(0)
        graph = data['graph']
        sequence = data['sequence']
        nx.draw(graph)
        name = '%d-%s.png' % (count, sequence.name)
        plt.savefig(name)
        plt.clf()
        count += 1
        for parent in sequence.parents:
            valueIncrease = parent['valueIncrease']
            indexReduction = parent['indexReduction']
            seq = parent['sequence']


            for vertex in graph.node:
                if graph.degree(vertex) == valueIncrease:
                    for neighbor in graph.neighbors(vertex):
                        for n in graph.node:

                            if n != neighbor and vertex != neighbor and vertex!= n:
                                copygraph = copy.deepcopy(graph)
                                if sequence.length == indexReduction and neighbor != indexReduction:
                                    copygraph.add_edge(neighbor, indexReduction)
                                    copygraph.remove_edge(vertex, neighbor)
                                    if True not in [nx.is_isomorphic(copygraph, g) for g in findGraphs[seq.name]]:
                                        g = findGraphs[seq.name]
                                        g.append(copygraph);
                                        findGraphs.update({seq.name: g})
                                        graphs.append({'graph': copygraph, 'sequence': seq})
                                        for  h in findGraphs[seq.name]:
                                            for ver1 in h:
                                                rebra = h.adjacency_list()[ver1]
                                                for k in rebra:
                                                    for ver2 in h:
                                                        if (ver2 != ver1 and h.degree(ver1) - h.degree(
                                                                ver2) == 1 and k != ver2
                                                                and k not in h.adjacency_list()[ver2]):
                                                            copyGraph = copy.deepcopy(h)
                                                            copyGraph.add_edge(k, ver2)
                                                            copyGraph.remove_edge(k, ver1)
                                                            if True not in [nx.is_isomorphic(copyGraph, g) for g in findGraphs[seq.name]]:
                                                                g = findGraphs[seq.name]
                                                                g.append(copyGraph)
                                                                findGraphs.update({seq.name: g})
                                                                graphs.append({'graph': copyGraph, 'sequence': seq})


                                elif copygraph.degree(n) == sequence.sequence[indexReduction] and n not in copygraph.adjacency_list()[neighbor]:

                                    copygraph.add_edge(n, neighbor)
                                    copygraph.remove_edge(vertex, neighbor)
                                    if True not in [nx.is_isomorphic(copygraph, g) for g in findGraphs[seq.name]]:
                                        g = findGraphs[seq.name]
                                        g.append(copygraph)
                                        findGraphs.update({seq.name: g})

                                        graphs.append({'graph': copygraph, 'sequence': seq})
                                        for  h in findGraphs[seq.name]:
                                            for ver1 in h:
                                                rebra = h.adjacency_list()[ver1]
                                                for k in rebra:
                                                    for ver2 in h:
                                                        if (ver2 != ver1 and h.degree(ver1) - h.degree(
                                                                ver2) == 1 and k != ver2
                                                                and k not in h.adjacency_list()[ver2]):
                                                            copyGraph = copy.deepcopy(h)
                                                            copyGraph.add_edge(k, ver2)
                                                            copyGraph.remove_edge(k, ver1)
                                                            if True not in [nx.is_isomorphic(copyGraph, g) for g in findGraphs[seq.name]]:
                                                                g = findGraphs[seq.name]
                                                                g.append(copyGraph)
                                                                findGraphs.update({seq.name: g})
                                                                graphs.append({'graph': copyGraph, 'sequence': seq})


seq = Sequence([1] * 12)
findGraphs = {}
sequences.append(seq)
bfs(seq)
graphs = generatingMaximumGraphs()
all_drawing_Sequence(graphs)

# graph = nx.Graph()
# a = [5,2,2,1,1,1]
# j=0
# graph.add_edge(0,1)
# while j < 6:
#     degree = a[j]
#     i = 2
#     while i <= degree:
#         if graph.degree(j)< degree:
#             graph.add_edge(j, i)
#         i+=1
#     j+=1
# print(111)
# nx.draw(graph)
# name = '%s.png' % "5,2,2,1,1,1"
# plt.savefig(name)
# plt.clf()
# g = []
# print(len(graph.node))
# g.append(graph)
# for vertex in graph.node:
#     if graph.degree(vertex) == 5:
#         for neighbor in graph.neighbors(vertex):
#             for n in graph.node:
#
#                 if n != neighbor and vertex != neighbor and vertex != n:
#                     copygraph = copy.deepcopy(graph)
#                     if len(a)== 6 and neighbor != 1:
#                         copygraph.add_edge(neighbor, 6)
#                         copygraph.remove_edge(vertex, neighbor)
#
#                     elif copygraph.degree(n) == a[1] :
#                         list = copygraph.adjacency_list()
#                         if neighbor not in list[n]:
#                             print(neighbor)
#                         # copygraph.add_edge(n, neighbor)
#                         # copygraph.remove_edge(vertex, neighbor)
#
#                     f = False
#                     for a in g:
#
#                         if nx.is_isomorphic(a, copygraph):
#                             f = True
#                     if not f:
#                         g.append(copygraph)
#                         nx.draw(graph)
#                         name = '%s.png' % n
#                         plt.savefig(copygraph)
#                         plt.clf()


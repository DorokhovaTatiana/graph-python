import copy
import networkx as nx
import matplotlib.pyplot as plt


class Sequence:
    def __init__(self, sequence):
        self.sequence = sequence
        self.isChildren = False
        self.name = ','.join(map(str, self.sequence))
        self.length = len(sequence) - sequence.count(0)

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

                newSequence = [value for value in sequences if value.name == name][0]

                print(node.name, "    ", newSequence.name)
                print("___________________________________")


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
        i+=1;
    return False



# def generatingMaximumGraphs():
#     for sequence in sequences:
#         k = 0
#         graph = nx.Graph()
#         while k < sequence.length:
#             graph.add_node(k)
#         for degree in sequence.sequence:
#             index = degree
#             k = 0
#             while index >0 and graph.degree(k) < degree:
#                 graph.add_edge(k, index)
#                 index-=1
#                 k+=1
#         nx.draw(graph)
#         plt.savefig("path.png")
            



# print(12)
# seq = Sequence([1] * 12)
#
# sequences.append(seq)
# bfs(seq)
graph = nx.Graph()

graph.add_edge(1,2);
# nx.draw(graph)
# plt.savefig("path1.png")

graph.add_edge(2,3)
graph.add_edge(3, 4)
graph.add_edge(3, 5)
# nx.draw(graph)
# plt.savefig("path2.png")
print(graph.degree(3))
print(1)





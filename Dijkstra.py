from typing import List


class MinHeap():
    """
    Min heap the data structure where the root is always the smallest element of them all.
    """
    ROOT_INDEX = 1

    def __init__(self, size = 1):
        self.array = [None]* size
        self.length = 0

    def rise(self, index: int):
        item = self.array[index]
        while index > 1 and self.array[index//2] > item:
            self.array[index] = self.array[index//2]
            index = index//2
        self.array[index] = item

    def add(self, item):
        self.length += 1
        self.array.append(item)
        self.rise(self.length)

    def smallest_child(self, index):
        if 2 * index == self.length or \
                self.array[2 * index] < self.array[2 * index + 1]:
            return 2 * index
        else:
            return 2 * index + 1

    def sink(self, index):
        item = self.array[index]

        while 2 * index <= self.length:
            min_child = self.smallest_child(index)
            if self.array[min_child] >= item:
                break
            self.array[index] = self.array[min_child]
            index = min_child
        self.array[index] = item

    def get_min(self):
        if self.length == 0:
            raise IndexError("Empty Heap")

        min_elem = self.array[MinHeap.ROOT_INDEX]
        self.length -= 1
        if self.length > 0:
            self.array[MinHeap.ROOT_INDEX] = self.array[self.length + 1]
            self.sink(MinHeap.ROOT_INDEX)
        self.array.pop() #O(1)
        return min_elem

    def update(self, item , new_value):
        #O(n) n being the number of elements in the heap
        item_index = None
        for index in range(1,self.length+1):
            if item == self.array[index][1]:
                self.array[index] = (new_value,item)
                item_index = index
                break
        if item_index is not None:
            self.rise(item_index)
        else:
            raise KeyError(f"{item} is not in the heap therefore cannot be updated")

class Vertex():

    def __init__(self,id):
        self.id = id
        self.edge = []
        self.distance = None

    def __str__(self):
        return f"{self.id}"

class Edge():

    def __init__(self,u:Vertex,v:Vertex,w:int):
        self.u = u
        self.v = v
        self.w = w
        self.flow = None

class Graph():

    def __init__(self, edges , num_of_vertices ,  bidirectional:bool):
        # O(L) locations
        self.vertices = [None]*num_of_vertices
        for edge in edges:
            if self.vertices[edge[0]] is None and self.vertices[edge[1]] is None:
                self.vertices[edge[0]] = Vertex(edge[0])
                self.vertices[edge[1]] = Vertex(edge[1])
                self.vertices[edge[0]].edge.append(Edge(self.vertices[edge[0]],self.vertices[edge[1]],edge[2]))
                if bidirectional:
                    self.vertices[edge[1]].edge.append(Edge(self.vertices[edge[1]],self.vertices[edge[0]],edge[2]))
            else:
                if self.vertices[edge[1]] is None:
                    self.vertices[edge[1]] = Vertex(edge[1])
                self.vertices[edge[0]].edge.append(Edge(self.vertices[edge[0]],self.vertices[edge[1]],edge[2]))
                if bidirectional:
                    self.vertices[edge[1]].edge.append(Edge(self.vertices[edge[1]],self.vertices[edge[0]],edge[2]))

    def dijkstra(self, source:Vertex , max_limit: int):
        discoverd_queue = MinHeap()
        source.distance = 0
        discoverd_queue.add((source.distance,source.id))
        discovered_list = [False]*len(self.vertices)
        visited_list = [False]*len(self.vertices)
        output_list = []
        while discoverd_queue.length > 0 :
            u: Vertex = self.vertices[discoverd_queue.get_min()[1]]
            visited_list[u.id] = True
            if u.distance > max_limit:
                break
            output_list.append(u.id)
            # output_list.append((u.id,u.distance)) # Delete later, Tester code
            for edge in u.edge:
                v : Vertex = edge.v
                if visited_list[v.id] == True:
                    pass
                else:
                    if discovered_list[v.id] == False:
                        v.distance = edge.w + u.distance
                        discovered_list[v.id] = True
                        discoverd_queue.add(( v.distance, v.id))
                    else:
                        if v.distance > (u.distance + edge.w):
                            v.distance = edge.w + u.distance
                            discoverd_queue.update(v.id,v.distance)
        return output_list

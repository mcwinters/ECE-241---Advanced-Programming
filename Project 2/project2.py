from pythonds.basic import Queue
import sys


class PriorityQueue:
    def __init__(self):
        self.heapArray = [(0, 0)]
        self.currentSize = 0

    def buildHeap(self, alist):
        self.currentSize = len(alist)
        self.heapArray = [(0, 0)]
        for i in alist:
            self.heapArray.append(i)
        i = len(alist) // 2
        while i > 0:
            self.percDown(i)
            i = i - 1

    def percDown(self, i):
        while (i * 2) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapArray[i][0] > self.heapArray[mc][0]:
                tmp = self.heapArray[i]
                self.heapArray[i] = self.heapArray[mc]
                self.heapArray[mc] = tmp
            i = mc

    def minChild(self, i):
        if i * 2 > self.currentSize:
            return -1
        else:
            if i * 2 + 1 > self.currentSize:
                return i * 2
            else:
                if self.heapArray[i * 2][0] < self.heapArray[i * 2 + 1][0]:
                    return i * 2
                else:
                    return i * 2 + 1

    def percUp(self, i):
        while i // 2 > 0:
            if self.heapArray[i][0] < self.heapArray[i // 2][0]:
                tmp = self.heapArray[i // 2]
                self.heapArray[i // 2] = self.heapArray[i]
                self.heapArray[i] = tmp
            i = i // 2

    def add(self, k):
        self.heapArray.append(k)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)

    def delMin(self):
        retval = self.heapArray[1][1]
        self.heapArray[1] = self.heapArray[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapArray.pop()
        self.percDown(1)
        return retval

    def isEmpty(self):
        if self.currentSize == 0:
            return True
        else:
            return False

    def decreaseKey(self, val, amt):
        # this is a little weird, but we need to find the heap thing to decrease by
        # looking at its value
        done = False
        i = 1
        myKey = 0
        while not done and i <= self.currentSize:
            if self.heapArray[i][1] == val:
                done = True
                myKey = i
            else:
                i = i + 1
        if myKey > 0:
            self.heapArray[myKey] = (amt, self.heapArray[myKey][1])
            self.percUp(myKey)

    def __contains__(self, vtx):
        for pair in self.heapArray:
            if pair[1] == vtx:
                return True
        return False


class Vertex:
    def __init__(self, key):
        self.id = key
        self.connectedTo = {}
        self.color = 'white'
        self.dist = sys.maxsize
        self.pred = None
        self.disc = 0
        self.fin = 0
        self.pweight = 0  # path weight variable for newBST function

    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def setColor(self, color):
        self.color = color

    def setDistance(self, d):
        self.dist = d

    def setPred(self, p):
        self.pred = p

    def setDiscovery(self, dtime):
        self.disc = dtime

    def setFinish(self, ftime):
        self.fin = ftime

    def getFinish(self):
        return self.fin

    def getDiscovery(self):
        return self.disc

    def getPred(self):
        return self.pred

    def getDistance(self):
        return self.dist

    def getColor(self):
        return self.color

    def getConnections(self):
        return self.connectedTo.keys()

    def getWeight(self, nbr):
        return self.connectedTo[nbr]

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getId(self):
        return self.id


def BFS(g, start):
    start.setDistance(0)
    start.setPred(None)
    vertQueue = Queue()
    vertQueue.enqueue(start)
    while vertQueue.size() > 0:
        currentVert = vertQueue.dequeue()
        for nbr in currentVert.getConnections():
            if nbr.getColor() == 'white':
                nbr.setColor('gray')
                nbr.setDistance(currentVert.getDistance() + 1)
                nbr.setPred(currentVert)
                vertQueue.enqueue(nbr)
        currentVert.setColor('black')
        # print(currentVert)  # prints the status of the current visited vertex


def newBFS(g, start):  # new BFS method for task 5, to "ONLY consider the path w/ the shortest distance between 2 users"
    start.setDistance(0)
    start.setPred(None)
    vertQueue = Queue()
    vertQueue.enqueue(start)
    while vertQueue.size() > 0:
        currentVert = vertQueue.dequeue()
        for nbr in currentVert.getConnections():
            if nbr.getColor() == 'white':
                nbr.setColor('gray')
                nbr.setDistance(currentVert.getDistance() + 1)
                for node in nbr.getConnections():  # for loop that runs through all of nbr's connections
                    if (node.getDistance() + 1) == nbr.getDistance():  # checks if node is parent
                        total_pweight = node.pweight + node.getWeight(nbr)  # sets total pweight variable
                        if nbr.pweight < total_pweight:  # if node's path is shorter
                            nbr.pweight = total_pweight  # updates nbr's pweight and pred
                            nbr.setPred(node)
                vertQueue.enqueue(nbr)
        currentVert.setColor('black')


class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self, key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.vertList

    def addEdge(self, f, t, cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())


def prim(g, start):
    pq = PriorityQueue()
    for v in g:
        v.setDistance(sys.maxsize)
        v.setPred(None)
    start.setDistance(0)
    pq.buildHeap([(v.getDistance(), v) for v in g])
    while not pq.isEmpty():
        currentVert = pq.delMin()
        for nextVert in currentVert.getConnections():
            newCost = currentVert.getWeight(nextVert)
            if nextVert in pq and newCost < nextVert.getDistance():
                nextVert.setPred(currentVert)
                nextVert.setDistance(newCost)
                pq.decreaseKey(nextVert, newCost)


class OSN:
    def __init__(self):
        self.network = Graph()  # initializes network graph
        self.negative_network = Graph()  # initializes negative network graph
        self.MST = Graph()  # initializes MST graph

    def buildGraph(self, filename):  # task 1
        import csv  # imports data file
        with open(filename) as file:  # reads data file
            csvreader = csv.reader(file)
            for row in csvreader:  # for loop that runs through each row
                self.network.addEdge(row[0], row[1], int(row[2]))  # adds edge from user 1 to user 2
                self.network.addEdge(row[1], row[0], int(row[2]))  # adds edge from user 2 to user 1
                self.negative_network.addEdge(row[0], row[1], -1 * int(row[2]))  # adds neg. edge from user 1 to user 2
                self.negative_network.addEdge(row[1], row[0], -1 * int(row[2]))  # adds neg. edge from user 2 to user 1

    def reset(self):  # reset function used in following methods, given in piazza
        for v in self.network:
            v.dist = sys.maxsize
            v.pred = None
            v.color = 'white'
            v.pweight = 0
        for v in self.MST:
            v.dist = sys.maxsize
            v.pred = None
            v.color = 'white'

    def findDistance(self, user1, user2):  # task 2
        BFS(self.network, self.network.vertList[user1])  # runs BFS on network graph

        for node in self.network:  # for loop that runs through each node in the network
            if self.network.vertList[user1] == node:  # if user 1 vertex is equal to the current node in for loop
                temp = self.network.vertList[user2].getDistance()  # defines temp variable as distance for user 2 vertex
                self.reset()  # resets
                return temp  # returns temp variable (distance of user 2)

    def buildMST(self):  # task 3
        prim(self.negative_network, self.negative_network.getVertex('Armstrong'))  # runs prim algorithm on neg. network

        for node in self.negative_network:  # for loop that runs through each node in negative network
            for connection in node.getConnections():  # for loop that runs through each node's connections
                if node == connection.getPred():  # if current node is its neighbor's predecessor
                    self.MST.addEdge(connection.getId(), node.getId(), -1 * node.getWeight(connection))  # adds to MST
                    self.MST.addEdge(node.getId(), connection.getId(), -1 * node.getWeight(connection))  # adds to MST

    def findPath(self, user1, user2):  # task 4
        self.reset()  # resets
        BFS(self.MST, self.MST.vertList[user1])  # runs BFS on MST

        path = [user2]  # initializes path as a list including user 2's vertex ID
        separator = " -> "  # separator for return string
        temp = self.MST.vertList[user2]  # sets temp variable as user 2 vertex
        while temp.getPred() is not None:  # while temp's predecessor exists
            path.append(temp.getPred().getId())  # appends temp's predecessor's ID to path list
            temp = temp.getPred()  # updates temp variable to its predecessor
        path = path[::-1]  # reverses path list
        return separator.join(path)  # returns string of path list, with each ID separated by an arrow

    def findClosePath(self, user1, user2):  # task 5
        self.reset()  # resets
        newBFS(self.network, self.network.vertList[user1])  # runs updates BFS on network graph

        path = [user2]  # initializes path as a list with the user 2 vertex's ID
        separator = " -> "  # defines separator as an arrow for return string
        temp = self.network.vertList[user2]  # sets temp variable as user 2 vertex
        while temp.getPred() is not None:  # while temp's predecessor exists
            path.append(temp.getPred().getId())  # appends temp's predecessor's ID to path list
            temp = temp.getPred()  # updates temp to its predecessor
        path = path[::-1]  # reverses path list
        return separator.join(path) + " (" + str(self.network.vertList[user2].pweight) + ")"  # returns string


if __name__ == "__main__":
    x = OSN()
    x.buildGraph('facebook_network.csv')
    x.buildMST()
    print(x.findClosePath('Murray', 'Clark'))

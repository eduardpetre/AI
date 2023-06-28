class NodArbore:
    def __init__(self, info, parinte=None):
        self.info = info
        self.parinte = parinte

    def drumRadacina(self):
        nod = self
        l = []
        while nod is not None:
            l.append(nod)
            nod = nod.parinte
        return l[::-1]

    def vizitat(self):
        nod = self.parinte
        while nod is not None:
            if nod.info == self.info:
                return True
            nod = nod.parinte
        return False

    def __str__(self):
        return str(self.info)

    def __repr__(self):
        return "({}, ({}))".format(self.info, [str(x) for x in self.drumRadacina()].join("->"))

class Graph:
    def __init__(self, matr, start, scopuri):
        self.matr = matr
        self.start = start
        self.scopuri = scopuri

    def scop(self, infoScop):
        return infoScop in self.scopuri

    def succesori(self, nod):
        l = []
        for i in range(len(self.matr)):
            if self.matr[nod.info][i] == 1:
                nod_i = NodArbore(i, nod)
                if not nod_i.vizitat():
                    l.append(nod_i)
        return l

from queue import Queue
def BFS(graf, NSOL):
    q = Queue()
    q.put(NodArbore(graf.start))

    l = []
    while not q.empty() and len(l) < NSOL:
        nod = q.get()
        if graf.scop(nod.info):
            l.append(nod.drumRadacina())

        for succesor in graf.succesori(nod):
            q.put(succesor)

    for x in l:
        print([str(nod) for nod in x])

def DFS(graf, NSOL):
    def DFS_rec(nod):
        if graf.scop(nod.info):
            l.append(nod.drumRadacina())
            if len(l) == NSOL:
                return
        for succesor in graf.succesori(nod):
            DFS_rec(succesor)

    l = []
    DFS_rec(NodArbore(graf.start))
    for x in l:
        print([str(nod) for nod in x])

matr = [[0, 1, 1],
        [1, 0, 1],
        [1, 1, 0]]

start = 0
scopuri = [2]
graf = Graph(matr, start, scopuri)
print("BFS: ")
BFS(graf, 2)
print("DFS: ")
DFS(graf, 2)

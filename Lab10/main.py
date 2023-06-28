class NodArbore:
    def __init__(self, info, parinte=None, g=0, h=0):
        self.info = info
        self.parinte = parinte
        self.g = g
        self.h = h
        self.f = g + h

    def drumRadacina(self):
        l = []
        nod = self
        while nod is not None:
            l.insert(0, nod)
            nod = nod.parinte
        return l

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
        return "({}, ({}), cost: {})".format(self.info, "->".join([str(x) for x in self.drumRadacina()]), self.f)


class Graf:
    def __init__(self, matr, start, scopuri, h):
        self.matr = matr
        self.start = start
        self.scopuri = scopuri
        self.estimatii = h

    def scop(self, infoNod):
        return infoNod in self.scopuri

    def succesori(self, nod):
        l = []
        for i in range(len(self.matr)):
            if self.matr[nod.info][i] != 0:
                nodNou = NodArbore(i, nod, nod.g + self.matr[nod.info][i], self.calculeaza_H(i))
                if not nodNou.vizitat():
                    l.append(nodNou)
        return l

    def calculeaza_H(self, infoNod):
        return self.estimatii[infoNod]


def aStarSolMultiple(gr, nsol):
    c = [NodArbore(gr.start)]
    while c:
        nodCurent = c.pop(0)
        if gr.scop(nodCurent.info):
            print(repr(nodCurent))
            nsol -= 1
            if nsol == 0:
                return
        lSuccesori = gr.succesori(nodCurent)
        for s in lSuccesori:
            indice = bin_search(c, s, 0, len(c) - 1)
            if (indice == len(c)):
                c.append(s)
            else:
                c.insert(indice, s)


def bin_search(listaNoduri, nodNou, ls, ld):
    if len(listaNoduri) == 0:
        return 0
    if ls == ld:
        if nodNou.f < listaNoduri[ls].f:
            return ls
        elif nodNou.f > listaNoduri[ls].f:
            return ld + 1
        else:  # f-uri egale
            if nodNou.g < listaNoduri[ls].g:
                return ld + 1
            else:
                return ls
    else:
        mij = (ls + ld) // 2
        if nodNou.f < listaNoduri[mij].f:
            return bin_search(listaNoduri, nodNou, ls, mij)
        elif nodNou.f > listaNoduri[mij].f:
            return bin_search(listaNoduri, nodNou, mij + 1, ld)
        else:
            if nodNou.g < listaNoduri[mij].g:
                return bin_search(listaNoduri, nodNou, mij + 1, ld)
            else:
                return bin_search(listaNoduri, nodNou, ls, mij)


def a_Star(gr):
    open = [NodArbore(gr.start)]
    closed = []
    while open:
        nod_curent = open.pop(0)
        if gr.scop(nod_curent.info):
            print(repr(nod_curent))
            return
        closed.append(nod_curent)
        lSuccesori = gr.succesori(nod_curent)
        for s in lSuccesori:
            nod_nou = None
            # daca s nu apartine drumului lui nod_curent
            if not s.vizitat():
                # daca s e in open
                for elem in open:
                    if s.info == elem.info:
                        if s.f < elem.f or (s.f == elem.f and s.g > elem.g):
                            open.remove(elem)
                            nod_nou = s
                            break
                # daca s e in closed (expandat)
                for elem in closed:
                    if s.info == elem.info:
                        if s.f < elem.f or (s.f == elem.f and s.g > elem.g):
                            closed.remove(elem)
                            nod_nou = s
                            break
                # daca s nu e in open si nici in closed
                if nod_nou == None:
                    nod_nou = s

                open.append(nod_nou)
                open.sort(key=lambda nod: (nod.f, -nod.g))
    return None


m = [
    [0, 3, 5, 10, 0, 0, 100],
    [0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 4, 9, 3, 0],
    [0, 3, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 5],
    [0, 0, 3, 0, 0, 0, 0],
]

start = 0
scopuri = [4, 6]
h = [0, 1, 6, 2, 0, 3, 0]

gr = Graf(m, start, scopuri, h)
# aStarSolMultiple(gr, 3)
a_Star(gr)

import copy


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
        return "{} ({}, {})".format(self.info, self.g, self.f)

    def __repr__(self):
        return "({}, ({}), cost:{})".format(self.info, "->".join([str(x) for x in self.drumRadacina()]), self.f)


class Graf:
    def __init__(self, start, scopuri):
        self.start = start
        self.scopuri = scopuri
        if not self.valideaza():
            print("Eroare fisier")
            exit(0)

    def scop(self, infoNod):
        return infoNod in self.scopuri

    def succesori(self, nod):
        l = []
        for istiva, stiva in enumerate(nod.info):
            if not stiva:
                continue

            copieStive = copy.deepcopy(nod.info)
            bloc = copieStive[istiva].pop()

            for istiva2, stiva2 in enumerate(copieStive):
                if istiva == istiva2:
                    continue

                stiveNoi = copy.deepcopy(copieStive)
                stiveNoi[istiva2].append(bloc)

                nodNou = NodArbore(stiveNoi, nod, nod.g + 1, self.calculeaza_h(stiveNoi))
                if not nodNou.vizitat():
                   l.append(nodNou)
        return l

    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):

        # "banala" - caz în care va returna costul minim pe o mutare daca starea nu e scop și 0 dacă e scop
        if tip_euristica=="euristica banala":
            if infoNod not in self.scopuri:
                return 1
            return 0

        # calculez cate blocuri nu sunt la locul lor fata de fiecare stare scop,
        # returneaza minimul dintre aceste valori
        elif tip_euristica=="euristica mutari":
            euristici=[]
            for (iScop, scop) in enumerate(self.scopuri):
                h=0
                for iStiva, stiva in enumerate(infoNod):
                        for iElem, elem in enumerate(stiva):
                            try:
                                # pe pozitia iElem nu se afla blocul din infoNod
                                if elem!=scop[iStiva][iElem]:
                                    h+=1
                            except IndexError:
                                # nu exista pozitia iElem in stiva cu indicele iStiva din scop
                                h+=1
                euristici.append(h)
            return min(euristici)

        # calculez cate blocuri nu sunt la locul fata de fiecare stare scop,
        # returnez minimul dintre aceste valori
        elif tip_euristica=="euristica costuri":
            euristici=[]
            for (iScop,scop) in enumerate(self.scopuri):
                h=0
                for iStiva, stiva in enumerate(infoNod):
                        for iElem, elem in enumerate(stiva):
                            try:
                                # pe pozitie iElem nu se afla blocul din infoNod
                                if elem!=scop[iStiva][iElem]:
                                    h+=1
                                else:
                                    # elem==scop[iStiva][iElem]:
                                    if stiva[:iElem]!=scop[iStiva][:iElem]:
                                     h+=2
                            except IndexError:
                                # nu exista pozitia iElem in stiva cu indicele iStiva din scop
                                h+=1
                euristici.append(h)
            return min(euristici)
        # tip_euristica == "euristica neadmisibila"
        else:
            euristici=[]
            # Supraestimez costurile
            for (iScop,scop) in enumerate(self.scopuri):
                h=0
                for iStiva, stiva in enumerate(infoNod):
                        for iElem, elem in enumerate(stiva):
                            try:
                                # pe pozitie iElem nu se afla blocul din infoNod
                                if elem!=scop[iStiva][iElem]:
                                    h+=3
                                else:
                                    # elem==scop[iStiva][iElem]:
                                    if stiva[:iElem]!=scop[iStiva][:iElem]:
                                        h+=2
                            except IndexError:
                                # nu exista pozitia iElem in stiva cu indicele iStiva din scop
                                h+=3
                euristici.append(h)
            return max(euristici)

    def valideaza(self):
        cond1 = all([len(self.start) == len(scop) for scop in self.scopuri])
        listaBlocuri = sorted(sum(self.start, start=[]))
        cond2 = all([listaBlocuri == sorted(sum(scop, start=[])) for scop in self.scopuri])
        return cond1 and cond2


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


def aStarSolMultiple(gr, nrSolutiiCautate=1):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodArbore(gr.start)]

    while len(c) > 0:
        # print("Coada actuala: " + str(c))
        # input()
        nodCurent = c.pop(0)

        if gr.scop(nodCurent.info):
            print("Solutie:")
            drum = nodCurent.drumRadacina()
            print(("->").join([str(n.info) for n in drum]))
            print("cost:", nodCurent.g)
            print("\n----------------\n")
            # input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        # [2,4,7,8,10,14]
        # c+=gr.succesori(nodCurent)
        for s in gr.succesori(nodCurent):
            indice = bin_search(c, s, 0, len(c) - 1)
            if indice == len(c):
                c.append(s)
            else:
                c.insert(indice, s)


def a_star(gr):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    l_open = [NodArbore(gr.start)]

    # l_open contine nodurile candidate pentru expandare (este echivalentul lui c din A* varianta neoptimizata)

    # l_closed contine nodurile expandate
    l_closed = []
    while len(l_open) > 0:
        # print("Coada actuala: " + str(l_open))
        # input()
        nodCurent = l_open.pop(0)
        l_closed.append(nodCurent)
        if gr.scop(nodCurent.info):
            print("Solutie:")
            drum = nodCurent.drumRadacina()
            print(("->").join([str(n.info) for n in drum]))
            print("cost:", nodCurent.g)
            return
        lSuccesori = gr.succesori(nodCurent)
        for s in lSuccesori:
            gasitC = False
            for nodC in l_open:
                if s.info == nodC.info:
                    gasitC = True
                    if s.f >= nodC.f:
                        lSuccesori.remove(s)
                    else:  # s.f<nodC.f
                        l_open.remove(nodC)
                    break
            if not gasitC:
                for nodC in l_closed:
                    if s.info == nodC.info:
                        if s.f >= nodC.f:
                            lSuccesori.remove(s)
                        else:  # s.f<nodC.f
                            l_closed.remove(nodC)
                        break
        for s in gr.succesori(nodCurent):
            indice = bin_search(l_open, s, 0, len(l_open) - 1)
            if indice == len(l_open):
                l_open.append(s)
            else:
                l_open.insert(indice, s)


def calculeazaStive(sirStiva):
    listaSiruriStive = sirStiva.strip().split('\n')
    return [sir.strip().split() if sir != '#' else [] for sir in listaSiruriStive]


f = open('input.txt', "r")
continut = f.read()
[sirStart, sirScopuri] = continut.strip().split("=========")
start = calculeazaStive(sirStart)
siruriScopuri = sirScopuri.strip().split("---")
scopuri = [calculeazaStive(sir) for sir in siruriScopuri]

print(start)
print(scopuri)

gr = Graf(start, scopuri)
a_star(gr)
class NodArbore:
    def __init__(self, info, parinte=None):
        self.info = info
        self.parinte = parinte

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
        return "({}, ({}))".format(self.info, "->".join([str(x) for x in self.drumRadacina()]))

    def afisSolFisier(self, fisier):
        drum = self.drumRadacina()
        for pas in drum:
            if pas.info[2] == 1:
                stanga = "(Stanga:<barca>) "
            else:
                stanga = "(Stanga) "
            malStanga = f"{pas.info[1]} canibali si {pas.info[0]} misionari ... "

            if pas.info[2] == 0:
                dreapta = " (Dreapta:<barca>) "
            else:
                dreapta = " (Dreapta) "
            malDreapta = f"{Graf.N - pas.info[1]} canibali si {Graf.N - pas.info[0]} misionari"

            if pas.parinte is not None:
                if pas.parinte.info[2] == 1:
                    deplasare = f">>> Barca s-a deplasat de la malul stang la malul drept cu {abs(pas.parinte.info[1] - pas.info[1])} canibali si {abs(pas.parinte.info[0] - pas.info[0])} misionari\n"
                else:
                    deplasare = f">>> Barca s-a deplasat de la malul drept la malul stang cu {abs(pas.parinte.info[1] - pas.info[1])} canibali si {abs(pas.parinte.info[0] - pas.info[0])} misionari\n"
            else:
                deplasare = ''

            fisier.write(deplasare + stanga + malStanga + dreapta + malDreapta + '.\n')
            fisier.write('\n')

class Graf:
    def __init__(self, start, scopuri):
        self.start = start
        self.scopuri = scopuri

    def scop(self, infoNod):
        return infoNod in self.scopuri

    def succesori(self, nod):
        def test(m, c):
            return m == 0 or m >= c

        l = []
        if nod.info[2] == 1:  # mal initial e mal curent (cu barca)
            misionariMalCurent = nod.info[0]
            canibaliMalCurent = nod.info[1]
            misionariMalOpus = Graf.N - nod.info[0]
            canibaliMalOpus = Graf.N - nod.info[1]
        else:
            misionariMalCurent = Graf.N - nod.info[0]
            canibaliMalCurent = Graf.N - nod.info[1]
            misionariMalOpus = nod.info[0]
            canibaliMalOpus = nod.info[1]

        maxMisionariBarca = min(Graf.M, misionariMalCurent)

        for mb in range(maxMisionariBarca + 1):
            if mb == 0:
                minCanibaliBarca = 1
                maxCanibaliBarca = min(Graf.M, canibaliMalCurent)
            else:
                minCanibaliBarca = 0
                maxCanibaliBarca = min(mb, Graf.M - mb, canibaliMalCurent)

            misionariMalCurentNou = misionariMalCurent - mb
            misionariMalOpusNou = misionariMalOpus + mb
            for cb in range(minCanibaliBarca, maxCanibaliBarca + 1):
                canibaliMalCurentNou = canibaliMalCurent - cb
                canibaliMalOpusNou = canibaliMalOpus + cb

                if not test(misionariMalCurentNou, canibaliMalCurentNou):
                    continue
                if not test(misionariMalOpusNou, canibaliMalOpusNou):
                    continue
                if nod.info[2] == 1:
                    infoNou = (misionariMalCurentNou, canibaliMalCurentNou, 0)
                else:
                    infoNou = (misionariMalOpusNou, canibaliMalOpusNou, 1)
                nodNou = NodArbore(infoNou, nod)

                if not nodNou.vizitat():
                    l.append(nodNou)

        return l


def breadth_first(gr, nsol):
    c = [NodArbore(gr.start)]
    while c:
        nodCurent = c.pop(0)
        if gr.scop(nodCurent.info):
            print(repr(nodCurent))
            nodCurent.afisSolFisier(open("output.txt", "w"))
            nsol -= 1
            if nsol == 0:
                return
        lSuccesori = gr.succesori(nodCurent)
        c += lSuccesori


f = open("input.txt", 'r')
n, m = f.read().strip().split()

Graf.N = int(n)
Graf.M = int(m)

start = [Graf.N, Graf.N, 1]
scopuri = [(0, 0, 0)]

gr = Graf(start, scopuri)
breadth_first(gr, 1)

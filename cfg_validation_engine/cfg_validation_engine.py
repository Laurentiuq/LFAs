import sys


def cfg_validation_engine():
    f = open(sys.argv[1], 'r')
    V = []
    E = ['*']
    R = []
    S = []
    valid = 1
    lines = f.readlines()
    # print(lines)
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    i = 0
    while i < (len(lines)):
        if valid == 0:
            break
        if len(lines[i]) > 0 and lines[i].rstrip()[0] == '#':
            ""
        else:
            if lines[i] == "variables":
                i += 1
                while lines[i] != "end":
                    # daca variabila a mai fost citita sau se afla in multimea de terminals nu e valid -- un terminal nu poate sa fie variabila si invers
                    if len(lines[i]) != 0 and (lines[i] in V or lines[i] in E):
                        print(lines[i])
                        valid = 0
                        break
                    elif len(lines[i]) != 0:
                        V.append(lines[i])
                    i += 1
            if lines[i] == "terminals":
                i += 1
                while lines[i] != "end":
                    # daca variabila a mai fost citita sau se afla in multimea de terminals nu e valid -- un terminal nu poate sa fie variabila si invers
                    if len(lines[i]) != 0 and (lines[i] in V or lines[i] in E):
                        print(lines[i])
                        valid = 0
                        break
                    elif len(lines[i]) != 0:
                        E.append(lines[i])
                    i += 1
            if lines[i] == "productions":
                i += 1
                while lines[i] != "end":
                    if len(lines[i]) != 0:
                        product = lines[i].lstrip('(')  # eliminare paranteza
                        product = product.rstrip(')')
                        # print(product)
                        sepProduct = product.split(',')  # separat produsul cartezian
                        # eliminare spatii etc.
                        sepProduct[0] = sepProduct[0].lstrip()
                        sepProduct[0] = sepProduct[0].rstrip()
                        sepProduct[1] = sepProduct[1].lstrip()
                        sepProduct[1] = sepProduct[1].rstrip()
                        R.append(tuple(sepProduct))
                    i += 1
            if lines[i] == "start point":
                i += 1
                while lines[i] != "end":
                    if len(lines[i]) != 0:
                        S.append(lines[i])
                    i += 1
        i += 1
    if len(V) == 0 or len(R) == 0 or len(E) == 1 or len(S) == 0:
        valid = 0
        print("Nu este valid")
        return 0
    # daca vreo variabila/terminal din products nu se afla in multimea de variabile terminale
    toTerminals = []  # variabilele care se pot substitui cu un terminal
    for x in R:
        if x[0] not in V:
            valid = 0
        for var in x[1]:
            if var not in V and var not in E:
                valid = 0
        for var in x[1].split('|'):
            if var in E:
                toTerminals.append(x[1])
    st = 0  # cel putin un product trebuie sa inceapa cu variabila de start
    bTerminal = 0
    for x in R:
        nxt = ""
        if x[0] == S[0]:
            st = 1
            nxt = x[1]
            while nxt not in toTerminals:
                if nxt in toTerminals:
                    bTerminal = 1
                    break
                if bTerminal == 1:
                    break
                for l in nxt:
                    if nxt in V:
                        for el in R:
                            if el[0] == l:
                                nxt = el[1]

    if valid == 0 and st == 1 and bTerminal == 1:
        print("Nu este valid")
        return 0
    else:
        print(f"Variables/Non-terminals: {V}")
        print(f"Terminals: {E}")
        print(f"Productions: {R}")
        print(f"Start point: {S}")
        return 1


cfg_validation_engine()

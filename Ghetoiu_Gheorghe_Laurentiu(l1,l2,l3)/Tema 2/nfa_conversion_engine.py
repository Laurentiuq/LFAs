# nfa parser

import re
import sys

sigma = set()  # alfabetul
Q = {}  # multimea starilor
q0 = {}  # starea initiala
d = []  # functia de tranzitie
F = {}  # starile finale
ls_d = []  # lista cu elementele liste de trei elemente pentru functia de tranzitie

fin = open(sys.argv[1])
f = fin.readlines()  # continutul fisierului
ends = 0
valid = True
index = 0
while index < len(f) and ends < 3 and valid is True:
    lin = f[index]
    lin_aux = ""  # linie auxiliara pentru a lua randul pana la primul '#'
    for element in lin.strip():
        if element == '#':
            break
        lin_aux += element
    lin = lin_aux
    index += 1

    # Skip la comentarii
    if len(lin.strip()) > 0 and lin.strip()[0] == "#":
        "skip"

    """
    Sigma
    """

    if lin.strip() == 'Sigma:':
        while index < len(f) and lin.strip() not in {"End", "end"} and valid is True:
            lin = f[index]
            index += 1
            if len(lin.strip()) > 0 and lin.strip()[0] == "#":
                "skip"
            elif lin.strip() not in {"End", "end", ""}:
                lin_aux = ""  # linie auxiliara pentru a lua randul pana la primul '#'
                for element in lin.strip():
                    if element == '#':
                        break
                    lin_aux += element
                if lin_aux.strip() in sigma:  # daca a mai aparut nu e valid - nu puteam avea aceeasi litera de doua ori in alfabet
                    valid = False
                for element in lin_aux.split():
                    sigma.add(element)

        else:
            ends += 1

    """
    States
    """
    if lin.strip() == "States:":
        i = 0
        while index < len(f) and lin.strip() not in {"End", "end", ""} and valid is True:
            lin = f[index]
            index += 1
            ls_aux = []  # lista auxiliara pentru elementele de pe un rand
            if len(lin.strip()) > 0 and lin.strip()[0] == "#":
                "skip"
            elif lin.strip() not in {"End", "end", ""}:
                lin_aux = ""  # linie auxiliara pentru a lua randul pana la primul '#'
                for element in lin.strip():
                    if element == '#':
                        break
                    lin_aux += element
                stari = re.split(" |,",
                                 lin_aux.strip())  # lista care contine starea si, daca e cazul, daca e finala sau de inceput

                if stari[0] in Q:  # nu putem avea aceeasi stare de doua ori in multimea de stari
                    valid = False

                for stare in stari:
                    if stare != "F" and stare != "S" and "#" not in stare:
                        Q[stari[0]] = i
                    if "F" == stare.strip():
                        F[stari[0]] = i
                    if "S" == stare.strip():
                        q0[stari[0]] = i
                i += 1
        else:
            ends += 1

    if lin.strip() == "Transitions:":
        i = 0
        while index < len(f) and lin.strip() not in {"End", "end", ""} and valid is True:
            lin = f[index]
            index += 1
            if len(lin.strip()) > 0 and lin.strip()[0] == "#":
                "skip"
            elif lin.strip() not in {"End", "end", ""}:
                lin_aux = ""  # linie auxiliara pentru a lua randul pana la primul '#'
                for element in lin.strip():
                    if element == '#':
                        break
                    lin_aux += element
                ls = re.split(" |, |,", lin_aux.strip())  # lista pentru fiecare element de pe rand

                if len(ls) == 3:
                    ls_d.append(ls)
                i += 1
        else:
            ends += 1

fin.close()

d = [[-1 for i in range(len(Q))] for j in range(len(Q))]

# print(ls_d)

for tp in ls_d:
    # In caz ca e posibil ca litera de tranzitie sa nu fie in alfabet
    if tp[1] not in sigma:
        valid = False
        break
    # Q[tp[0]] - din dictionarul Q, identifica linia asociata starii "stateX" si coloana
    # asociata starii "stateY" si pune in matrice litera prin care se realizeaza tranzitia
    # daca e posibil sa se defineasca o functie pe o stare care nu se afla in multimea de stari atunci apare keyerror
    # pentru care avem try-except
    try:
        if d[Q[tp[0]]][Q[tp[2]]] != -1:
            d[Q[tp[0]]][Q[tp[2]]].append(tp[1])
        else:
            d[Q[tp[0]]][Q[tp[2]]] = [tp[1]]

    except:
        valid = False
        break

# daca avem mai multe stari de inceput nu e valid - nu e determinist
if len(q0) != 1:
    valid = False

# daca nu avem vreuna dintre multimi

if len(sigma) <= 0 or len(Q) <= 0 or len(d) <= 0 or len(F) <= 0:
    valid = False

# print(f"sigma: {sigma}")
# print(f"Q: {Q}")
# print(f"q0: {q0}")
# print(f"d: {d}")
# print(f"F: {F}")
# print("")

if valid is False:
    print("Automatul nu e valid")
else:
    print("Automatul e valid\n")

    q0_nou = [str(x) for x in q0.keys()]
    stari_aux = [q0_nou]
    urmatoarele_stari = []
    tranzitii_noi = []
    stari_noi = []
    lista_stari = []
    stari_verificate = []
    # ok retine cate stari noi avem de parcurs
    ok = 1
    stari_verificate = []
    while ok >= 1 and len(stari_aux) > 0:
        urmatoarele_stari = []
        for stare_aux in stari_aux:
            stari_verificate.append(stare_aux)
            ok -= 1
            # pentru fiecare litera vedem unde poate merge o stare

            for litera in sorted(list(sigma)):
                # urmatoarele stari o sa fie toate starile catre care merge o alta stare pentru o anumita litera
                stari_catre_care_merge = []
                for st in stare_aux:
                    for tranzitie in ls_d:
                        if tranzitie[0] == st and tranzitie[1] == litera and tranzitie[2] not in stari_catre_care_merge:
                            stari_catre_care_merge.append(tranzitie[2])
                    # print(f"stari catre : {stari_catre_care_merge}")
                if sorted(stari_catre_care_merge) not in urmatoarele_stari and len(
                        stari_catre_care_merge) > 0 and sorted(stari_catre_care_merge) not in stari_verificate:
                    ok += 1
                    urmatoarele_stari.append(sorted(stari_catre_care_merge))
                    urmatoarele_stari = sorted(urmatoarele_stari)
                if sorted(list(stari_catre_care_merge)) not in sorted(lista_stari) and len(stari_catre_care_merge) > 0:
                    lista_stari.append(sorted(list(stari_catre_care_merge)))
                if [sorted(list(stare_aux)), litera, sorted(list(stari_catre_care_merge))] not in tranzitii_noi:
                    tranzitii_noi.append([sorted(list(stare_aux)), litera, sorted(list(stari_catre_care_merge))])
        # print(f"urmatoarele_stari: {urmatoarele_stari}")
        stari_aux = sorted(urmatoarele_stari)
    # print(f"tranzitii_noi{tranzitii_noi}")
    # print(f"lista stari {lista_stari}")

    d_nou = []  # noua functie de tranzitie
    Q_nou = []  # noile stari
    F_nou = []  # noile stari finale
    stari_parcurse = []  # starile deja redenumite
    indice_stare_noua = len(Q)
    for tranzitie in tranzitii_noi:
        if len(tranzitie[0]) == 1:
            tranzitie[0] = str(tranzitie[0][0])
            if tranzitie[0] not in Q_nou:
                Q_nou.append(tranzitie[0])
        elif type(tranzitie[0]) == list and len(tranzitie[2]) > 0:
            if sorted(tranzitie[0]) not in stari_parcurse:
                stare_before = tranzitie[0]
                stari_parcurse.append(sorted(tranzitie[0]))
                nume_nou = 'q' + str(indice_stare_noua)
                Q_nou.append(nume_nou)
                indice_stare_noua += 1
                for trz in tranzitii_noi:
                    if type(trz[0]) == list:
                        # print("--------------", trz[0], tranzitie[0])
                        if sorted(trz[0]) == sorted(stare_before):
                            trz[0] = nume_nou
                    if type(trz[2]) == list:
                        if sorted(trz[2]) == sorted(stare_before):
                            # print("--------------")
                            trz[2] = nume_nou
                for stare_veche in stare_before:
                    if stare_veche in F and nume_nou not in F_nou:
                        F_nou.append(nume_nou)

        if len(tranzitie[2]) == 1:
            tranzitie[2] = str(tranzitie[2][0])
            if tranzitie[2] not in Q_nou:
                Q_nou.append(tranzitie[2])
        elif type(tranzitie[2]) == list and len(tranzitie[2]) > 0:
            if sorted(tranzitie[2]) not in stari_parcurse:
                stare_before = tranzitie[2]
                stari_parcurse.append(sorted(tranzitie[2]))
                nume_nou = 'q' + str(indice_stare_noua)
                Q_nou.append(nume_nou)
                indice_stare_noua += 1
                for trz in tranzitii_noi:
                    if type(trz[0]) == list:
                        if sorted(trz[0]) == sorted(stare_before):
                            trz[0] = nume_nou
                    if type(trz[2]) == list:
                        if sorted(trz[2]) == sorted(stare_before):
                            trz[2] = nume_nou
                for stare_veche in stare_before:
                    if stare_veche in F and nume_nou not in F_nou:
                        F_nou.append(nume_nou)

    # print(tranzitii_noi)
    print("Sigma:")
    for litera in sigma:
        print(litera)
    print("\nEnd\n")
    print("States: ")
    for stare in Q_nou:
        if stare in F_nou and stare in q0_nou:  # aici ar trebui sa fie doar una
            print(f"{stare}, S, F")
        elif stare in q0_nou:  # aici ar trebui sa fie doar una
            print(f"{stare}, S")
        elif stare in F_nou:
            print(f"{stare}, F")
        else:
            print(stare)

    print("\nEnd\n")
    print("Transitions:")
    for tranzitie in tranzitii_noi:
        if tranzitie[2]!=[]:
            print(f"{tranzitie[0]}, {tranzitie[1]}, {tranzitie[2]}")
    print("\nEnd")

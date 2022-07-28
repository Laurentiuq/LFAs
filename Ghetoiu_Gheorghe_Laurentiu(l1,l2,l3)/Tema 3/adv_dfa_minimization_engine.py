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
    # Q[tp[0]] - din dictul Q, identifica linia asociata starii "stateX" si coloana
    # asociata starii "stateY" si pune in matrix litera prin care se realizeaza tranzitia
    # daca e posibil sa se defineasca o functie pe o stare care nu se afla in multimea de stari atunci apare keyerror
    # pentru care avem try-except
    try:
        d[Q[tp[0]]][Q[tp[2]]] = tp[1]

    except:
        valid = False
        break

# test pentru determinism - nu putem merge din aceeasi stare in doua directie pentru acelasi input(aceeasi litera)
# deci daca apare o litera de doua ori pe o linie in functia de tranzitie nu o sa stim pe care sa o alegem si deci
# automatul nu mai este determinist
determinist = True
for litera in sigma:
    for linie in d:
        if linie.count(litera) > 1:
            valid = False
            determinist = False

# daca avem mai multe stari de inceput nu e valid - nu e determinist
if len(q0) != 1:
    valid = False
    determinist = False

# daca nu avem vreuna dintre multimi

if len(sigma) <= 0 or len(Q) <= 0 or len(d) <= 0 or len(F) <= 0:
    valid = False

# print(f"sigma: {sigma}")
# print(f"Q: {Q}")
# print(f"q0 {q0}")
# print(f"d: {d}")
# print(f"F: {F}")


# n = len(Q)  # numarul starilor
# fin = open("input.txt")  # fisier cu inputuri pentru testare
#
# for cuvant in fin.readlines():
#     aux = q0[list(q0.keys())[0]]  # q0 trebuie transformat in valoarea asociata primei key (singura daca este valid)
#     ok = 1
#     print(f"{cuvant.strip()}:", end="")
#     for lit in cuvant.strip():
#         try:
#             aux = d[aux].index(lit)
#         except:
#             ok = 0
#     if aux in F.values() and ok == 1:
#         print("OK")
#     else:
#         print("NOT OK")
# fin.close()
# ok=1
# if ok == 1:

# transformam tranzitiile in dictionar de tipul dict[(nod1,litera)]= nod2
def trans_dict(ls_d):
    dict = {}
    for element in ls_d:
        t = (Q[element[0]], element[1])
        dict[t] = Q[element[2]]
    return dict


def AFD_minimal_Myhill():
    global ls_d, q0, sigma, Q

    dict = trans_dict(ls_d)
    final = [F[x] for x in F.keys()]
    n = len(Q)
    # cream tabelul
    matrix = [[0 for j in range(n)] for i in range(n)]
    # for i in range(n):
    #     for j in range(i):
    #         matrix[i][j] = 0
    # completare tabel
    for i in range(1, n):
        for j in range(i):
            if (i in final and j not in final) or (i not in final and j in final):
                matrix[i][j] = 1

    # print(final)
    # print(matrix)

    marcat = 1
    # print(f"dict: {dict}")
    while marcat == 1:
        marcat = 0
        for i in range(n):
            for j in range(i):
                if matrix[i][j] == 0:
                    # daca elementul nu e marcat, ne uitam pentru perechea (i,j) daca gasim un x pentru care (i,x) si (j,x) sunt marcate
                    for caracter in sigma:
                        # print(matrix)
                        stare1 = dict[(i, caracter)]
                        stare2 = dict[(j, caracter)]
                        if matrix[stare1][stare2] == 1 or matrix[stare2][stare1] == 1:
                            # matrix[j][i] = 1
                            matrix[i][j] = 1
                            marcat = 1
                            break
                        # elif matrix[stare2][stare1] == 1:
                        #     matrix[j][i] = 1
                        #     matrix[i][j] = 1
                        #     marcat = 1
                        #     nr += 1
                        #     break


    # print(f"matrix: {matrix}")
    # acum ca am terminat de marcat toate perechile posibile, combinam starile nemarcate
    lista_noduri = []
    k = 1  # numarul claselor de echivalenta
    # vom crea un vector pentru impartire pe componente
    v = [0 for i in range(n)]
    # luam perechile nemarcate din tabel
    for i in range(n):
        for j in range(i):
            if matrix[i][j] == 0:
                marcat = 0
                for cnt in range(len(lista_noduri)):
                    if i in lista_noduri[cnt] or j in lista_noduri[cnt]:
                        lista_noduri[cnt].add(i)
                        lista_noduri[cnt].add(j)
                        marcat = 1
                        if v[i] == 0:
                            v[i] = v[j]
                        else:
                            v[j] = v[i]
                if marcat == 0:
                    multime = set()
                    multime.add(i)
                    multime.add(j)
                    lista_noduri.append(multime)
                    v[i], v[j] = k, k
                    k = k + 1

    for i in range(n):
        if v[i] == 0:
            multime = set()
            multime.add(i)
            lista_noduri.append(multime)
            # trebuie adaugat k in v[i], altfel starile care raman singure sunt vazute in tranzitie ca o singura stare
            v[i] = k
            #v[i] = i  # aici nu mai este numarul clasei de echivalenta, e  un fel de reprezentant
            k = k + 1
    # print(f"v: {v}")
    # vectorul v e ca o partitie si ne spune despre fiecare nod in ce multime este
    # grupam nodurile ca sa vedem ce stari noi avem
    new_transition = {}
    new_final = set()
    for noduri in lista_noduri:
        for caracter in sigma:
            next_states = 0
            for nod in noduri:
                if nod == 0:
                    new_start = nod
                if nod in final:
                    new_final.add(nod)
                next_states = dict[(nod, caracter)]
                # k ia valoarea initiala ascoiata starii.....
                k = nod
            for multime in lista_noduri:
                if next_states in multime:
                    t = (k, caracter)
                    # in new_transition am pus valoarea initiala asociata starii, nu cea din v, dupa redenumire
                    # aceasta o sa fie aceeasi cu a celorlalte stari din clasa de echivalenta
                    new_transition[t] = next_states

    # print(f"new_transition: {new_transition}")
    # print(f"lista_noduri: {lista_noduri}")
    index_stare_noua = len(Q)
    nume_noi = {}
    for noduri in lista_noduri:
        if len(noduri) > 1:
            nume_nou = "q" + str(index_stare_noua)
            for nod in noduri:
                if nod not in nume_noi:
                    nume_noi[nod] = nume_nou
            index_stare_noua += 1
        else:
            for stare in Q.keys():
                if Q[stare] == list(noduri)[0]:
                    nume_noi[Q[stare]] = stare
    # print(f"nume noi: {nume_noi}")

    d_new = []
    Q_new = {}
    F_new = {}
    q0_new = {}

    # print("Transitions : ")
    for transition in new_transition.keys():
        # print(f"{nume_noi[transition[0]]}, {transition[1]}, {nume_noi[new_transition[transition]]}")
        d_new.append([nume_noi[transition[0]], transition[1], nume_noi[new_transition[transition]]])
    # print(d_new)
    # print("States:")
    ind = 0
    for stari in lista_noduri:
        ok_stare_de_inceput = 0
        ok_stare_de_final = 0
        for i in stari:
            if i == new_start:
                ok_stare_de_inceput = 1
            elif i in new_final:
                ok_stare_de_final = 1
        Q_new[nume_noi[list(stari)[0]]] = ind

        if ok_stare_de_inceput == 1 and ok_stare_de_final == 1:
            # print(f"{nume_noi[list(stari)[0]]}, S, F")
            q0_new[nume_noi[list(stari)[0]]] = ind
            F_new[nume_noi[list(stari)[0]]] = ind
        elif ok_stare_de_inceput == 1:
            # print(f"{nume_noi[list(stari)[0]]}, S")
            q0_new[nume_noi[list(stari)[0]]] = ind
        elif ok_stare_de_final == 1:
            # print(f"{nume_noi[list(stari)[0]]}, F")
            F_new[nume_noi[list(stari)[0]]] = ind
        else:
            "skip"
            # print(f"{nume_noi[list(stari)[0]]}")
        ind += 1
    # print(f"new_start: {new_start}")
    # print(f"new_final: {new_final}")

    # print(f"d_new: {d_new}")
    # print(f"Q_new: {Q_new}")
    # print(f"q0_new: {q0_new}")
    # print(f"F_new: {F_new}")

    tranzitii_F = []  # tranzitiile care pornesc din starea finala
    for final_state in F_new.keys():
        for tranzitie in d_new:
            if tranzitie[0] == final_state and tranzitie[2] not in F_new.keys():
                tranzitii_F.append(tranzitie)
    # print(f"tranzitii_F: {tranzitii_F}")

    stari_eliminate = []    # starile care vor fi eliminate
    # pentru fiecare tranzitie care porneste din starea finala
    for tranzitie_F in tranzitii_F:
        possible_states = []    # starile in care putem sa ajungem
        for tranzitie in d_new:
            if tranzitie_F[2] == tranzitie[0]:
                if tranzitie[0] not in possible_states:
                    possible_states.append(tranzitie[2])
                    cont = 1
        while cont == 1:    # cat timp mai gasim stari noi in care putem sa ajungem si nu am fost
            cont = 0
            for stare in possible_states:
                for tranzitie in d_new:
                    if stare == tranzitie[0]:
                        if tranzitie[2] not in possible_states:
                            possible_states.append(tranzitie[2])
                            cont = 1
        # print(f"possible_states: {possible_states}")
        # daca printre starile in care putem ajunge nu e si vreuna dintre starile finale atunci eliminam stare
        # care are acel traseu
        contine_stari_finale = 0
        for stare_F in F_new.keys():
            if stare_F in possible_states:
                contine_stari_finale = 1
        if contine_stari_finale == 0:
            stari_eliminate.append(tranzitie_F[2])

    # print(f"stari_eliminate: {stari_eliminate}")

    # aici stergem tranzitiile care contin dead states
    tranzitii_anterioare = d_new.copy()
    for tranzitie in tranzitii_anterioare:
        if tranzitie[0] in stari_eliminate or tranzitie[2] in stari_eliminate:
            d_new.remove(tranzitie)
    # aici eliminam dead states din multimea de stari
    stari_anterioare = [state for state in Q_new.keys()]
    for state in stari_anterioare:
        if state in stari_eliminate:
            Q_new.pop(state)
    print("Sigma :")
    for s in sigma:
        print(s)
    print("\nEnd\n")
    print("States: ")
    for state in Q_new.keys():
        if state in q0_new.keys() and state in F_new.keys():
            print(f"{state}, S, F")
        elif state in q0_new.keys():
            print(f"{state}, S")
        elif state in F_new.keys():
            print(f"{state}, F")
        else:
            print(state)
    print("\nEnd\n")
    print("Transitions: ")
    for tranzitie in d_new:
        print(f"{tranzitie[0]}, {tranzitie[1]}, {tranzitie[2]}")
    print("\nEnd\n")


if valid is False:
    print("Automatul nu e valid")
else:
    print("Automatul e valid\n")
    AFD_minimal_Myhill()

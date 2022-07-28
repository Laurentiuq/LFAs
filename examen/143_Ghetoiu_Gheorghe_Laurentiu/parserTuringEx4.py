"""
Cucos Maria-Marianita
Ghetoiu Gheorghe-Laurentiu
"""

def parser():
    import re
    import sys
    sigma = []  # alfabetul
    Q = []  # lista starilor
    gamma = []  # alfabetul benzii
    q0 = []  # starea initiala
    # delta = {}  # functia de tranzitie
    tranzitii = {}  # functia de tranzitie
    q_acc = []
    q_rej = []

    ls_d = []  # lista cu elementele liste de 7 elemente pentru functia de tranzitie

    fin = open("ex4_config_file")
    if(len(sys.argv) >= 2):
        fin = open(sys.argv[1])
    f = fin.readlines()  # continutul fisierului
    ends = 0
    valid = True
    index = 0

    while index < len(f) and ends < 4 and valid is True:

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
                        sigma.append(element)

            else:
                ends += 1

        """
            Gamma
        """

        if lin.strip() == 'Gamma:':
            while index < len(f) and lin.strip() not in {"End", "end"} and valid is True:
                lin = f[index]
                index += 1
                if lin.strip() not in {"End", "end", ""}:
                    lin_aux = ""  # linie auxiliara pentru a lua randul pana la primul '#'
                    for element in lin.strip():
                        lin_aux += element
                    if lin_aux.strip() in gamma:  # daca a mai aparut nu e valid - nu puteam avea aceeasi litera de doua ori in alfabet
                        valid = False
                    for element in lin_aux.split():
                        gamma.append(element)

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
                    stari = re.split(" |,",lin_aux.strip())  # lista care contine starea si, daca e cazul, daca e finala sau de inceput

                    if stari[0] in Q:  # nu putem avea aceeasi stare de doua ori in multimea de stari
                        valid = False

                    for stare in stari:
                        if stare != "F" and stare != "S" and "#" not in stare:
                            if stari[0] not in Q:
                                Q.append(stari[0])
                        if "F" == stare.strip():
                            q_acc.append(stari[0])

                        if "S" == stare.strip():
                            q0.append(stari[0])
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
                        lin_aux += element
                    ls = re.split(", ", lin_aux.strip())  # lista pentru fiecare element de pe rand
                    if len(ls) == 7:
                        ls_d.append(ls)
                    i += 1
            else:
                ends += 1

    fin.close()


    for tp in ls_d:
        # In caz ca e posibil ca litera de tranzitie sa nu fie in alfabet
        if tp[1] not in gamma:
            valid = False
            break
        # --------------------
        if tp[3] not in gamma:
            valid = False
            break
        # --------------------
        if tp[4] not in gamma:
            valid = False
            break
        # --------------------
        if tp[5] not in "RL":
            valid = False
            break
        # --------------------
        if tp[6] not in "RL":
            valid = False
            break

        #     dictionarul de tranzitii
        tranzitii[(tp[0], tp[1])] = (tp[2], tp[3], tp[4], tp[5], tp[6])

        # sigma inclus in gamma
        for s in sigma:
            if s not in gamma:
                valid = False

    # daca avem mai multe stari de inceput nu e valid
    if len(q0) != 1:
        valid = False

    # daca avem mai multe stari de accept nu e valid
    if len(q_acc) != 1:
        valid = False

    # daca nu avem vreuna dintre multimi
    if len(sigma) <= 0 or len(Q) <= 0 or len(gamma) <= 0 or len(tranzitii) <= 0:
        valid = False

    # print(f"Q: {Q}")
    # print(f"sigma: {sigma}")
    # print(f"gamma: {gamma}")
    # print(f"functie tranzitii: {tranzitii}")
    # print(f"q0: {q0}")
    # print(f"q_acc: {q_acc}")

    if valid is False:
        print("Fisierul nu e valid\n")
    else:
        print("Fisierul e valid\n")

    return Q, sigma, gamma, tranzitii, q0, q_acc, q_rej
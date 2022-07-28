"""
Cucos Maria-Marianita
Ghetoiu Gheorghe-Laurentiu
"""

# Limbajul pe care Masina Turing il recunoaste:  L = {0^n1^n2^n | n≥1}
# Pentru acest exercitiu am modifcat config_file adaugand simbolul i in alfabetul benzii si stari noi pentru
# a verifica daca cele doua benzi sunt identice, acestea sunt marcate cu V si sunt adaugata in multimea de stari q_ver

# validare config file
import re
import sys
from parserTuring import parser

# ----------------------------------------------------------------------------------------

Q, sigma, gamma, tranzitii, q0, q_acc, q_rej, q_ver = parser()

input_string = '001122'


# functia care implementeaza masina turing,
# primeste ca parametru stringul pe care se doreste verificarea
def turingMachine(input_string):
    validF = False  # validitatea pe prima banda
    validS = False  # validitatea pe a doua banda
    backup_tape = input_string  # stringul din input
    # transformam cele doua benzi in una singura de forma:
    # "$input_string$backup_string$"
    twoTapesInOne = list('$' + input_string + '$' + backup_tape + '$')

    # twoTapesInOne[3] = '2' # test pentru a verifica daca recunoaste cand o banda a fost modificata

    # lungimea inputului
    inputLength = len(input_string)  # lungimea inputului

    currentStateF = q0[0]  # starea curenta pentru prima banda, initializata cu starea de inceput
    currentStateS = q0[0]  # starea curenta pentru a doua banda, initializata cu starea de inceput
    currentPositionF = 1  # pozitia curenta de pe prima banda, incepand cu cel mai din stanga element care apartine inputului
    currentPositionS = currentPositionF + len(backup_tape) + 1  # pozitia curenta de pe a doua banda

    tapeModified = False  # retinem si daca au loc schimbari pe vreuna dintre benzi

    # parcurgem inputul alternand de la o banda la alta(in zig-zag)
    # inputul permite sa se mearga in doua simboluri diferite pentru fiecare dintre benzi, deoarece pentru una dintre
    # benzi puteam avea conventia ca un simbol din alfabetul inputului sa fie marcat cu un alt simbol din alfabetul benzii
    # rezultatul final fiind acelasi

    # cat timp nu suntem in starea de accepatre masina continua sa ruleze
    while currentStateF != q_acc[0] and currentStateS != q_acc[0]:
        # actualizam argumentul functiei delta pentru fiecare banda
        currentArgumentF = (currentStateF, twoTapesInOne[currentPositionF])
        currentArgumentS = (currentStateS, twoTapesInOne[currentPositionS])
        # daca la un moment dat cele doua argumente difera, sau starile in care a ramas masina dupa citirea
        # de pe fiecare banda difera atunci e posibil ca una dintre benzi sa fie modificata
        if currentStateF != currentStateS or currentArgumentF != currentArgumentS:
            tapeModified = True
        # deoarece functia de tranzitie este un dictionar verificam daca avem o cheie corespunzatoare cu argumentul actual
        try:
            # Pentru prima banda
            currentStateF = tranzitii[currentArgumentF][0]  # actualizam starea curenta pentru prima banda
            twoTapesInOne[currentPositionF] = tranzitii[currentArgumentF][
                1]  # scriem pe banda simbolul indicat de functia de tranzitie
            # mergem la dreapta sau la stanga verificand daca acest lucru este posibil (daca ne aflam la captul din
            # stanga al benzii si functia de tranzitie indica o deplasare spre dreapta ramanem pe loc
            # daca ne aflam la capatul benzii verificam iar functia de tranzitie indica o deplasare spre dreapta
            # verificam daca ne aflam in starea de accept si ne oprim
            if tranzitii[currentArgumentF][3] == 'R':
                if twoTapesInOne[currentPositionF] == '$':
                    if currentStateF == q_acc[0]:
                        validF = True
                else:
                    currentPositionF += 1
            elif tranzitii[currentArgumentF][3] == 'L':
                if twoTapesInOne[currentPositionF] != '$':
                    currentPositionF -= 1

            # Pentru a doua banda
            currentStateS = tranzitii[currentArgumentS][0]
            twoTapesInOne[currentPositionS] = tranzitii[currentArgumentS][2]  #
            if tranzitii[currentArgumentS][4] == 'R':
                if twoTapesInOne[currentPositionS] == '$':
                    if currentStateS == q_acc[0]:
                        validS = True
                else:
                    currentPositionS += 1
            elif tranzitii[currentArgumentS][4] == 'L':
                if twoTapesInOne[currentPositionS] != '$':
                    currentPositionS -= 1

            # daca am ajuns in stare de accept ne putem opri
            if validS == True or validF == True:
                break
            if currentStateS == q_acc[0] or currentStateF == q_acc[0]:
                if currentStateF == q_acc[0]:
                    validF = True
                if currentStateS == q_acc[0]:
                    validS = True
                break


        # daca in functia de tranzitie nu este definit un caz in care ne aflam, iar starea nu este de accept deducem
        # ca masina respinge inputul
        except:
            if currentStateS == q_acc[0] or currentStateF == q_acc[0]:
                if currentStateS != currentStateF:
                    tapeModified = True
                if currentStateF == q_acc[0]:
                    validF = True
                if currentStateS == q_acc[0]:
                    validS = True
            else:
                q_rej.append(currentStateS)
            break

    identicalTapes = True
    currentPosition = 1
    currentArgument = ()
    # masina se intoarce in sa citeasca de la primul simbol de pe prima banda
    # gaseste starea corespunzatoare pentru respectivul simbol din noua multime de stari adaugate
    # daca din starea respectiva rezulta trecerea intr-o noua stare si pentru simbolul echivalent ca pozitie de pe a doua banda
    # (in acest caz noile stari adaugate duc doar catre ele insasi)
    # atunci inseamna ca acelasi simbol se afla pe aceeasi pozitie in ambele benzi
    # se trece la urmatorul simbol
    while twoTapesInOne[currentPosition] != '$':
        for state in q_ver:
            currentArgument = (state, twoTapesInOne[currentPosition])
            currentState = state
            if currentArgument in tranzitii.keys():
                break
        for ind in range(2):
            twoTapesInOne[currentPosition] = 'i'
            try:
                currentState = tranzitii[currentArgument][0]
                currentArgument = (currentState, twoTapesInOne[currentPosition + inputLength + 1])
            except:  # daca vreodata nu se gaseste un argument potrivit pentru noile tranzitii inseamna ca benzile nu sunt egale
                identicalTapes = False
        currentPosition += 1
    # masina trece in noua stare finala
    if identicalTapes == True:
        currentStateF = q_ver[len(q_ver) - 1]
        currentStateS = q_ver[len(q_ver) - 1]
        currentState = q_ver[len(q_ver) - 1]
    """
    Exemplu:
     #xyz#xzy
     --prima pozitie--
     currentArgument = (q10, x) -> (q10, i, i, R, R)
     currentArgument = (q10, x) -> (q10, i, i, R, R)
     --a doua pozitie--
     currentArgument = (q11, y) -> (q11, i, i, R, R)
     currentArgument = (q11, z) -> KEY_ERROR
    """

    if tapeModified == True:
        print("Una dintre benzi a suferit modificari")
    if validS == validF == True:
        print(f"{input_string} -> Acceptat")
        if currentState == q_ver[len(q_ver) - 1]:
            print("Benzile sunt identice")
        return True
    else:
        print(f"{input_string} -> Respins")
        if currentState == q_ver[len(q_ver) - 1]:
            print("Benzile sunt identice")
        return False


if len(sys.argv) >= 3:
    input_string = sys.argv[2]
turingMachine(input_string)

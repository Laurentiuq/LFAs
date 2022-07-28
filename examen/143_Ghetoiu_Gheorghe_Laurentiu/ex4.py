"""
Cucos Maria-Marianita
Ghetoiu Gheorghe-Laurentiu
"""

#  L = { w#w | w is a string}


# validare config file
import re
import sys
from parserTuringEx4 import parser

# ----------------------------------------------------------------------------------------

Q, sigma, gamma, tranzitii, q0, q_acc, q_rej = parser()
# functia care implementeaza masina turing,
# primeste ca parametru stringul pe care se doreste verificarea
def turingMachine(input_string):
    validF = False  # validitatea pe prima banda
    validS = False  # validitatea pe a doua banda
    backup_tape = input_string  # stringul din input

    # transformam cele doua benzi in una singura de forma:
    # "$input_string$backup_string$"
    twoTapesInOne = list('$' + input_string + '$' + backup_tape + '$')
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

            twoTapesInOne[currentPositionF] = tranzitii[currentArgumentF][1]  # scriem pe banda simbolul indicat de functia de tranzitie
            currentStateF = tranzitii[currentArgumentF][0]  # actualizam starea curenta pentru prima banda
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
                if currentPositionF != 0 and twoTapesInOne[currentPositionF - 1] != '$':
                    currentPositionF -= 1

            # Pentru a doua banda
            twoTapesInOne[currentPositionS] = tranzitii[currentArgumentS][2]  #
            currentStateS = tranzitii[currentArgumentS][0]
            if tranzitii[currentArgumentS][4] == 'R':
                if twoTapesInOne[currentPositionS] == '$':
                    if currentStateS == q_acc[0]:
                        validS = True
                else:
                    currentPositionS += 1
            elif tranzitii[currentArgumentS][4] == 'L':
                if currentPositionS != 0 and twoTapesInOne[currentPositionS - 1] != '$':
                    currentPositionS -= 1

            # daca am ajuns in stare de accept ne putem opri
            if validS is True or validF is True:

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
                q_rej.append((currentStateF, currentStateS))
            break

    if tapeModified == True:
        print("Banda a fost modificata")
        if validF == True:
            print("Inputul initial este acceptat")
        else:
            print("Inputul initial este respins")
        if validS == True:
            print("Inputul de backup este acceptat")
        else:
            print("Inputul de backup este respins")
    else:
        if validS == validF == True:
            print(f"{input_string} -> Acceptat")
            return True
        else:
            print(f"{input_string} -> Respins")
            return False


input_string = '101110101#101110101'
if len(sys.argv) >= 3:
    input_string = sys.argv[2]
turingMachine(input_string)

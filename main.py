from graphesFunctions import *
from menu import menu
from dictionnaires import *

GrapheCLSCs = None

fakeDict = {
    'A' : {'B':1,'D':5},
    'B' : {'A':1,'C':5,'E':1},
    'C' : {'B':5, 'D':3},
    'D' : {'A':3,'E':4},
    'E' : {'B':4,'D':1}
}

def main():
    creerGraphe("centresLocaux.txt")
    
    a = testLongChemin('1', 50)
    print(a)
main()
from functions import *

def test1():
    my_dictionary = dict()
    my_dictionary[1] = {2 : 85}
    my_dictionary[1][3] = 217
    my_dictionary[1][4] = 173

    my_dictionary[2] = {5 : 80}
    my_dictionary[2][6] = 56

    print(my_dictionary)

def main():
    CLSC = readFile("centresLocaux.txt")
    #print(CLSC)

main()
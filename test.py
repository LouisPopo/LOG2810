from functions import my_function

def main():
    my_function("Hello World")
    file = open("textTest.txt","r")
    print (file.read())

main()
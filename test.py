def my_function(word):
    print(word)

def main():
    my_function("Hello World")
    file = open("textTest.txt","r")
    print (file.read())

main()
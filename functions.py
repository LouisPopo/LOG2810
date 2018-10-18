def creerGraphe(filename):
    bornes = dict()
    with open(filename,"r") as f:
        data = f.readlines()
    for line in data:
        if line != "\n":
            nom, hasCharge = line.split(",")
            bornes[nom] = hasCharge.rstrip()
        else :
            break
    print(bornes)


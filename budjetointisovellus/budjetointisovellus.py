import csv

budjetti = {}
if input("kopioidaanko aiempi kuukausi K/E: ") == "K":
    with open("budjetointisovellus.csv", mode = "r")as file:
        tiedosto = csv.reader(file)
        for lines in tiedosto:
            print(lines[0])

    with open("budjetointisovellus.csv", mode = "r")as file:
        tiedosto = csv.reader(file)
        kuukausi = str(input("mikä kuukausi kopioidaan(kk.vvvv): "))
        for lines in tiedosto:
            
            if kuukausi == lines[0]:
                budjetti = eval(lines[1])
           
   
else:
    budjetti = {"vuokra":float(input("anna vuokra: ")),
                "vakuutukset":float(input("anna vakuutukset: ")),
                "kouluruokailu":float(input("anna kouluruokailu: ")),
                "sähkö":float(input("anna sahko: ")),
                "liikkuminen":float(input("anna liikkuminen: "))}
while True:
    x = input("(n)äytä (l)isää (p)oista (m)uokkaa (loppu):  ")
    if x == "l":
        uusi = input("uusi meno: ") 
        if uusi in budjetti:
            print("no")
        else:
             uusimaara = float(input("anna määrä: "))
             budjetti[uusi] = uusimaara
    elif x == "n":
        for i in budjetti:
            print(i , budjetti[i])


    elif x == "p":
        poista = input("mikä poistetaan: ")
        if poista in budjetti:
            del budjetti[poista]
        else:
            print("no")

    elif x == "m":
        muokkaa = input("mikä muutetaan: ")
        if muokkaa in budjetti:
            budjetti[muokkaa] = float(input("anna määrä: "))


        
    elif x == "loppu":
        break
            
if input("tallennetaanko K/E: ") == "K":
    pvm = str(input("anna päivämäärä muodossa (kk.vvvv): "))
    rivi = [pvm, budjetti]
    with open("budjetointisovellus.csv", "w")as file:
        tiedosto = csv.writer(file)
        tiedosto.writerow(rivi)
else:
    print("ei tallennettu")


if input("haluatko nädä viime kuukausien ruokakulut (K/E): ") == "K":
    with open("budjetointisovellus.csv", mode = "r")as file:
        tiedosto = csv.reader(file)
        lista = []
        nimet = []
        for lines in tiedosto:
            lista.append(eval(lines[1])["kouluruokailu"])
            nimet.append(lines[0])

    import matplotlib.pyplot as plt
    import numpy as np

    x = np.array(nimet)
    y = np.array(lista)

    plt.bar(x,y)
    plt.show()
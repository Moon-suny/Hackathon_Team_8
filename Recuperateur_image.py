import os
'''Ici nous souhaitons récuperer des images, des antennes existente a partir des données de l'anfr'''

def recuperation_coo(fichier)->list: #cette fonction, renverra une liste de coordonée ou ce trouve les antenne ainsi que le Nat_ID le Sup_Id afin de connaitre leur support ainsi que de les identifier.
    out = []
    with open(fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            l = ligne.split(";")
            l2 = []

            for i in range(0,len(l)-1):
                if i == 0 or (i >= 2 and i <= 10):
                    l2.append(l[i])
                    
            "calcule coordonée"
            lat = int(l2[2]) + (int(l2[3])/60) + (int(l2[4])/3600)
            long = int(l2[6]) + (int(l2[7])/60) + (int(l2[8])/3600)
            if l2[5] == "N" :
                pass
            elif l2[5] == "S":
                lat = lat*-1

            if l2[9] == "W":
                long = long*-1
            elif l2[9] == "E":
                pass

            l3 = []
            l3.append(l2.pop(0))
            l3.append(l2.pop(0))
            l3.append((lat,long))
            out.append(l3)
        return out
    
l = recuperation_coo("C:/Users/maxim/Documents/Isep/Hackaton_ANFR/Hackathon_Team_8/data/test.txt")
for el in l:
    print(el)
#!/bin/Python
#coding=utf-8
import copy
import random
import sys


### LE CHATEAU ###

## créer le chateau 
def cree_chateau(x0,y0):
    ly=[]
    for y in range(y0):
        lx=[]
        for x in range(x0):
            lx.append("*")
        ly.append(lx)
    return ly

## définir les salles
def ajout_salle(grille,coordonnees,valeur):
    for c in coordonnees :
        grille[c[1]][c[0]]=valeur
    return grille


## définir toutes les salles et couloirs du chateau avec leur coordonées
def definir_chateau():    
    xlen=15
    ylen=11
    chateau=cree_chateau(xlen,ylen)     # on crée le chateau
    
    coordonnees_vide=[]                        # on vide les cases hors du chateau
    for x in [0,xlen-1]:
        for y in range(ylen):
            coordonnees_vide.append([x,y])
    for x in range(xlen):
        for y in [0,ylen-1]:
            coordonnees_vide.append([x,y])
    for x in [1,2,8,9,10,12,13]:
        for y in [1,2,8,9]:
            coordonnees_vide.append([x,y])
    for x in [2,4,5,6,8,9,10,12]:
        for y in [2,4,6,8]:
            coordonnees_vide.append([x,y])
    for y in [8,9]:
        coordonnees_vide.append([11,y])
    chateau=ajout_salle(chateau,coordonnees_vide," ")
    coordonnees_salles=[]                      # on définit les cases salles et on les place dans le chateau 
    for x in [1,5,9,13]:
        for y in [3,5,7]:
            coordonnees_salles.append([x,y])
    chateau=ajout_salle(chateau,coordonnees_salles,"S")
    coordonnees_paradis=[[11,1]]               # on définit la case paradis et on les place dans le chateau
    chateau=ajout_salle(chateau,coordonnees_paradis,"P")
    coordonnees_reception=[[5,9]]              # on définit la case réception et on les place dans le chateau 
    chateau=ajout_salle(chateau,coordonnees_reception,"R")

    monstres=["maitre_chateau","savant_fou","bibbendum_chamallow1","bibbendum_chamallow2","bibbendum_chamallow3"]   # on définit les monstres présents dans le chateau
    energie=[]                           # on définit les pintes d'énergie présentes dans les salles
    for pinte in range(5):
        energie.append("pinte"+str(pinte+1))
    coordonnees_monstres,coordonnees_energie=place_objet(chateau,monstres,energie)        # on place les pintes d'énergie et les monstres dans le chateau

    return chateau,coordonnees_monstres,coordonnees_energie,xlen,ylen 
    

## afficher le chateau
def affiche_chateau(grille):
    for ligne in grille:
        for case in ligne :
            print case,
        print " "

## trouver la position du joueur à tout moment dans le chateau
def position_joueur(grille):
    for y in range(len(grille)):
        for x in range(len(grille[y])):
            if grille[y][x]=="X":
                idx=x
                idy=y
    return idx,idy

def trouve_coordonnees(grille,element):
    coordonnees=[]
    for ligne in range(len(grille)):
        for colonne in range(len(grille[ligne])):
            if grille[ligne][colonne]==element:
                coordonnees.append([colonne,ligne])
    return coordonnees


### LE FANTOME ###
def fantome(energie):
    fantome={}
    fantome["energie"]=energie
    return fantome


### L'ENERGIE ###

## mettre en place les pintes d'énergie
def action_energie(x,y,joueur,coordonnees_energie):
    pintes=0
    for pos_pinte in coordonnees_energie.items():
        if [x,y] == pos_pinte[1] :
            joueur["energie"]+=1
            pintes+=1
            del coordonnees_energie[pos_pinte[0]]            
    if pintes != 0 :
        print "Vous avez trouvé",pintes,"pintes d'énergie ! Gasper a maintenant",joueur["energie"],"points d'énergie"
    return joueur


### LES MECHANTS ###

## définir l'action du maitre du chateau
def action_maitre(grille,x,y):
    print "Oh non ! Vous êtes nez à nez avec le maître du chateau !\nIl vous a renvoyé dans la case réception"
    grille[y][x]="S"
    coordonnees=trouve_coordonnees(grille,"R")
    x,y=coordonnees[0]
    tmp=copy.deepcopy(grille[y][x])
    grille[y][x]="X"
    affiche_chateau(grille)
    return x,y,tmp

## définir l'action du savant fou 
def action_savant(joueur,grille,x,y,xlen,ylen):
    print "Oh non ! Le savant vous attaque !\nVous perdez 1 pinte de vie et vous êtes envoyé dans une autre salle"
    joueur["energie"]=joueur["energie"]-1
    if joueur["energie"]<=0:
        fin_jeu_energie()
    grille[y][x]="S"
    x=0
    y=0
    coordonnees_vide=trouve_coordonnees(grille," ")
    coordonnees_paradis=trouve_coordonnees(grille,"P")
    while ([x,y] in coordonnees_vide) or ([x,y] in coordonnees_paradis):
        x=random.randrange(xlen)
        y=random.randrange(ylen)
    tmp=copy.deepcopy(grille[y][x])
    grille[y][x]="X"
    print "Gasper a maintenant",joueur["energie"],"points d'énergie"
    affiche_chateau(grille)
    return x,y,joueur,tmp

## définir l'action du Bibbendum Chamallow
def action_bibbendum(joueur):
    print "Oh non ! Bibbendum Chamallow vous a paralysé avec sa mousse !\nVous perdez 2 pintes d'énergies"
    joueur["energie"]=joueur["energie"]-2
    print "Gasper a maintenant",joueur["energie"],"points d'énergie"
    if joueur["energie"]<=0:
        fin_jeu_energie()
    return joueur
    
## mettre en place les méchants et les pintes d'énergie
def place_objet(grille,monstres,pintes):
    coordonnees=trouve_coordonnees(grille,"S")
    coordonnees_monstres={}
    for monstre in monstres:
        coordonnees_monstres[monstre]=random.choice(coordonnees)
        coordonnees.remove(coordonnees_monstres[monstre])
    coordonnees_energie={}
    while pintes!=[]:
        if len(pintes) > 3:
            nb_pintes=random.randrange(3)+1
        else:
            nb_pintes=random.randrange(len(pintes))+1
        tmp=random.choice(coordonnees)
        coordonnees.remove(tmp)
        for nb in range(nb_pintes):
            coordonnees_energie[pintes[nb]]=tmp
        pintes=pintes[nb_pintes:]
    return coordonnees_monstres,coordonnees_energie

## appeler les méchants
def action_monstre(x,y,joueur,grille,coordonnees_monstres,xlen,ylen,tmp):
    if [x,y] in coordonnees_monstres.values():
        if [x,y] == coordonnees_monstres["maitre_chateau"] :
            x,y,tmp=action_maitre(grille,x,y)
        elif [x,y] == coordonnees_monstres["savant_fou"]:
            x,y,joueur,tmp=action_savant(joueur,grille,x,y,xlen,ylen)
        else : 
            joueur=action_bibbendum(joueur)
    return x,y,joueur,tmp

## définir les cordonnées sur lesquels apparaissent les avertissements
def coordonnees_avertissement(coordonnees_monstres):
    coordonnees={}
    for monstre in coordonnees_monstres.keys():
        pos1=copy.deepcopy(coordonnees_monstres[monstre])
        pos1[0]-=1
        pos2=copy.deepcopy(coordonnees_monstres[monstre])
        pos2[0]+=1
        pos3=copy.deepcopy(coordonnees_monstres[monstre])
        pos3[1]-=1
        pos4=copy.deepcopy(coordonnees_monstres[monstre])
        pos4[1]+=1
        coordonnees[monstre]=[pos1,pos2,pos3,pos4]
    return coordonnees

## définir les cris d'avertissement
def cri(coordonnees,x,y):
    maitre=coordonnees["maitre_chateau"]
    savant=coordonnees["savant_fou"]
    bibbendum=["bibbendum_chamallow1","bibbendum_chamallow2","bibbendum_chamallow3"]
    bc=[]
    for b in bibbendum :
        for coordonnee in coordonnees[b]:
            bc.append(coordonnee)
    if [x,y] in maitre:
        print "Qu'est-ce qu'on entend ? On dirait le son de clés..."
    elif [x,y] in savant:
        print "Ha ha ha ha !!"
    elif [x,y] in bc:
        print "Ca sent le chamallow fraise..."


### JEU ###

## affiche le menu de jeu
def affiche_menu():
    raw_input("COMMANDES\n4: gauche\n8: haut\n6: droit\n2: bas\n0: quitter\n<tapez sur une touche pour commencer>")
    
## début du jeu
def init_jeu(grille):
    print("Gasper, le gentil fantôme d’un chateau, aimerait pouvoir retourner dans le monde des fantômes où il fait toujours beau et où tous ses amis l’attendent. \nMais il est perdu dans un labyrinthe de pièces dont il ne trouve plus la sortie... Voulez-vous l'aider à braver tous les dangers ?")
    affiche_menu()
    coordonnees=trouve_coordonnees(grille,"R")
    grille=ajout_salle(grille,coordonnees,"X")
    return grille

## fin du jeu : manque d'énergie
def fin_jeu_energie():
    print "Gasper n'a plus d'énergie ! \nVous avez perdu"
    sys.exit()

## fin du jeu : arrivée au paradis
def fin_jeu_paradis():
    print "Gasper le gentil fantôme a atteint le paradis. Bravo ! grâce à vous il a retrouvé tous ses amis ! \nVous avez gagné"
    sys.exit()

## gestion des déplacements
def jeu(grille,joueur,coordonnees_monstres,coordonnees_energie,xlen,ylen):
    option=10
    x,y=position_joueur(grille)
    tmp="R"
    tmp_coordonnees=copy.deepcopy([x,y])
    avertissement=coordonnees_avertissement(coordonnees_monstres)
    while True:
        option=raw_input("Déplacement : ")
        while option not in ["0","2","4","6","8"]:
		    option=raw_input("Pas une option\nDéplacement : ")
        if (option=="4") and (grille[y][x-1] != " "):
        	x-=1
        elif (option=="6") and (grille[y][x+1] != " "):
            x+=1
        elif (option=="8") and (grille[y-1][x] != " "):
            y-=1
        elif (option=="2") and (grille[y+1][x] != " "):
            y+=1
        elif option=="0":
            break
        else:
            print "C'est un mur"
        grille[tmp_coordonnees[1]][tmp_coordonnees[0]]=tmp
        tmp=copy.deepcopy(grille[y][x])
        grille[y][x]="X"
        affiche_chateau(grille)
        if tmp=="*":
            cri(avertissement,x,y)
        elif tmp=="S":
            x,y,joueur,tmp=action_monstre(x,y,joueur,grille,coordonnees_monstres,xlen,ylen,tmp)
            joueur=action_energie(x,y,joueur,coordonnees_energie)
        elif tmp=="P":
            fin_jeu_paradis()
        tmp_coordonnees=copy.deepcopy([x,y])
        
        
### INITIALISATION DU JEU ###

def FantomeEscape():
    chateau,coordonnees_monstres,coordonnees_energie,xlen,ylen = definir_chateau()   # on définit le chateau et toutes ses salles, et on place les pintes d'énergie et les mosntres
    
    joueur=fantome(3)       # on initialise le joueur

    chateau=init_jeu(chateau)
    affiche_chateau(chateau)
    jeu(chateau,joueur,coordonnees_monstres,coordonnees_energie,xlen,ylen) 


##### MAIN #####
FantomeEscape()

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
def ajout_salle(grille,coor,valeur):
    for c in coor :
        grille[c[1]][c[0]]=valeur
    return grille


## définir toutes les salles et couloirs du chateau avec leur coordonées
def definir_chateau():    
    xlen=15
    ylen=11
    
    chateau=cree_chateau(xlen,ylen)     # on crée le chateau
    
    coor_vide=[]                        # on vide les cases hors du chateau
    for x in [0,xlen-1]:
        for y in range(ylen):
            coor_vide.append([x,y])
    for x in range(xlen):
        for y in [0,ylen-1]:
            coor_vide.append([x,y])
    for x in [1,2,8,9,10,12,13]:
        for y in [1,2,8,9]:
            coor_vide.append([x,y])
    for x in [2,4,5,6,8,9,10,12]:
        for y in [2,4,6,8]:
            coor_vide.append([x,y])
    for y in [8,9]:
        coor_vide.append([11,y])
    chateau=ajout_salle(chateau,coor_vide," ")

    coor_salles=[]                      # on définit les cases salles et on les place dans le chateau 
    for x in [1,5,9,13]:
        for y in [3,5,7]:
            coor_salles.append([x,y])
    chateau=ajout_salle(chateau,coor_salles,"S")
    
    coor_paradis=[[11,1]]               # on définit la case paradis et on les place dans le chateau
    chateau=ajout_salle(chateau,coor_paradis,"P")

    coor_reception=[[5,9]]              # on définit la case réception et on les place dans le chateau 
    chateau=ajout_salle(chateau,coor_reception,"R")

    monstres=["maitre_chateau","savant_fou","bibbendum_chamallow1","bibbendum_chamallow2","bibbendum_chamallow3"]   # on définit les monstres présents dans le chateau

    energie=[]                           # on définit les pintes d'énergie présentes dans les salles
    for pinte in range(5):
        energie.append("pinte"+str(pinte+1))
    
    coor_monstres,coor_energie=place_objet(chateau,monstres,energie)        # on place les pintes d'énergie et les monstres dans le chateau

    return chateau,coor_monstres,coor_energie,xlen,ylen 
    

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

def trouve_coor(grille,element):
    coor=[]
    for ligne in range(len(grille)):
        for colonne in range(len(grille[ligne])):
            if grille[ligne][colonne]==element:
                coor.append([colonne,ligne])
    return coor


### LE FANTOME ###
def fantome(energie):
    fantome={}
    fantome["energie"]=energie
    return fantome


### L'ENERGIE ###

## mettre en place les pintes d'énergie
def action_energie(x,y,joueur,coor_energie):
    pintes=0
    for pos_pinte in coor_energie.items():
        if [x,y] == pos_pinte[1] :
            joueur["energie"]+=1
            pintes+=1
            del coor_energie[pos_pinte[0]]            
    if pintes != 0 :
        print "Vous avez trouvé",pintes,"pintes d'énergie ! Gasper a maintenant",joueur["energie"],"points d'énergie"
    return joueur


### LES MECHANTS ###

## définir l'action du maitre du chateau
def action_maitre(grille,x,y):
    print "Oh non ! Vous êtes nez à nez avec le maître du chateau !\nIl vous a renvoyé dans la case réception"
    grille[y][x]="S"
    coor=trouve_coor(grille,"R")
    x,y=coor[0]
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
    coor_vide=trouve_coor(grille," ")
    coor_paradis=trouve_coor(grille,"P")
    while ([x,y] in coor_vide) or ([x,y] in coor_paradis):
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
    coor=trouve_coor(grille,"S")
    coor_monstres={}
    for monstre in monstres:
        coor_monstres[monstre]=random.choice(coor)
        coor.remove(coor_monstres[monstre])
    coor_energie={}
    while pintes!=[]:
        if len(pintes) > 3:
            nb_pintes=random.randrange(3)+1
        else:
            nb_pintes=random.randrange(len(pintes))+1
        tmp=random.choice(coor)
        coor.remove(tmp)
        for pinte in range(nb_pintes):
            coor_energie[pintes[pinte]]=tmp
        pintes=pintes[nb_pintes:]
    return coor_monstres,coor_energie

## appeler les méchants
def action_monstre(x,y,joueur,grille,coor_monstres,xlen,ylen,tmp):
    if [x,y] in coor_monstres.values():
        if [x,y] == coor_monstres["maitre_chateau"] :
            x,y,tmp=action_maitre(grille,x,y)
        elif [x,y] == coor_monstres["savant_fou"]:
            x,y,joueur,tmp=action_savant(joueur,grille,x,y,xlen,ylen)
        else : 
            joueur=action_bibbendum(joueur)
    return x,y,joueur,tmp

## définir les cordonnées sur lesquels apparaissent les avertissements
def coor_avertissement(coor_monstres):
    coor={"maitre_chateau":[],"savant_fou":[],"bibbendum_chamallow1":[],"bibbendum_chamallow2":[],"bibbendum_chamallow3":[]}
    for ind in coor_monstres.keys():
        pos1=copy.deepcopy(coor_monstres[ind])
        pos1[0]-=1
        coor[ind].append(pos1)
        pos2=copy.deepcopy(coor_monstres[ind])
        pos2[0]+=1
        coor[ind].append(pos2)
        pos3=copy.deepcopy(coor_monstres[ind])
        pos3[1]-=1
        coor[ind].append(pos3)
        pos4=copy.deepcopy(coor_monstres[ind])
        pos4[1]+=1
        coor[ind].append(pos4)
    return coor

## définir les cris d'avertissement
def cri(coor_avert,x,y):
    maitre=coor_avert["maitre_chateau"]
    savant=coor_avert["savant_fou"]
    bibbendum=["bibbendum_chamallow1","bibbendum_chamallow2","bibbendum_chamallow3"]
    bc=[]
    for b in bibbendum :
        for coor in coor_avert[b]:
            bc.append(coor)
    if [x,y] in maitre:
        print "Qu'est-ce qu'on entend ? On dirait le son de clés..."
    if [x,y] in savant:
        print "Ha ha ha ha !!"
    if [x,y] in bc:
        print "Ca sent le chamallow fraise..."


### JEU ###

## affiche le menu de jeu
def affiche_menu():
    raw_input("COMMANDES\n4: gauche\n8: haut\n6: droit\n2: bas\n0: quitter\n<tapez sur une touche pour commencer>")
    
## début du jeu
def init_jeu(grille):
    print("Gasper, le gentil fantôme d’un chateau, aimerait pouvoir retourner dans le monde des fantômes où il fait toujours beau et où tous ses amis l’attendent. \nMais il est perdu dans un labyrinthe de pièces dont il ne trouve plus la sortie... Voulez-vous l'aider à braver tous les dangers ?")
    affiche_menu()
    coor=trouve_coor(grille,"R")
    grille=ajout_salle(grille,coor,"X")
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
def jeu(grille,joueur,coor_monstres,coor_energie,xlen,ylen):
    option=10
    x,y=position_joueur(grille)
    tmp="R"
    tmp_coor=copy.deepcopy([x,y])
    coor_avert=coor_avertissement(coor_monstres)
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
        grille[tmp_coor[1]][tmp_coor[0]]=tmp
        tmp=copy.deepcopy(grille[y][x])
        grille[y][x]="X"
        affiche_chateau(grille)
        if tmp=="*":
            cri(coor_avert,x,y)
        elif tmp=="S":
            x,y,joueur,tmp=action_monstre(x,y,joueur,grille,coor_monstres,xlen,ylen,tmp)
            joueur=action_energie(x,y,joueur,coor_energie)
        elif tmp=="P":
            fin_jeu_paradis()
        tmp_coor=copy.deepcopy([x,y])
        
        
### INITIALISATION DU JEU ###

def FantomeEscape():
    chateau,coor_monstres,coor_energie,xlen,ylen = definir_chateau()   # on définit le chateau et toutes ses salles, et on place les pintes d'énergie et les mosntres
    
    joueur=fantome(3)       # on initialise le joueur

    chateau=init_jeu(chateau)
    affiche_chateau(chateau)
    jeu(chateau,joueur,coor_monstres,coor_energie,xlen,ylen)  


##### MAIN #####
FantomeEscape()

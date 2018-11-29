#!/bin/Python
#coding=utf-8
import copy
import random
import sys
from Tkinter import *
from tkinter.messagebox import *


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
def salle(grille,coor,valeur):
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
    chateau=salle(chateau,coor_vide," ")

    coor_salles=[]                      # on définit les cases salles et on les place dans le chateau 
    for x in [1,5,9,13]:
        for y in [3,5,7]:
            coor_salles.append([x,y])
    chateau=salle(chateau,coor_salles,"S")
    
    coor_paradis=[[11,1]]               # on définit la case paradis et on les place dans le chateau
    chateau=salle(chateau,coor_paradis,"P")

    coor_reception=[[5,9]]              # on définit la case réception et on les place dans le chateau 
    chateau=salle(chateau,coor_reception,"R")

    monstres=["maitre_chateau","savant_fou","bibbendum_chamallow1","bibbendum_chamallow2","bibbendum_chamallow3"]   # on définit les monstres présents dans le chateau

    energie=[]                           # on définit les pintes d'énergie présentes dans les salles
    for pinte in range(5):
        energie.append("pinte"+str(pinte+1))
    
    coor_monstres,coor_energie=place_item(coor_salles,monstres,energie)        # on place les pintes d'énergie et les monstres dans le chateau

    return chateau,coor_vide,coor_salles,coor_paradis,coor_reception,coor_monstres,coor_energie,xlen,ylen 
    

## afficher le chateau
def affiche_chateau(grille,grille_init,joueur,fenetre):
    xlen = len(grille[0])
    ylen = len(grille)
    x,y = position(grille)
    for ligne in range(ylen):
        for colonne in range(xlen):
            if grille_init[ligne][colonne] == " ":
                Canvas(fenetre, width=800 / xlen, height=700 / ylen, bg="black").grid(column=colonne,row=ligne)
            elif grille_init[ligne][colonne] == "S":
                if [x,y]==[colonne,ligne]:
                    color="red"
                Canvas(fenetre, width=800 / xlen, height=700 / ylen, bg="red").grid(column=colonne, row=ligne)
            elif grille_init[ligne][colonne] == "P":
                if [x,y]==[colonne,ligne]:
                    color="green"
                Canvas(fenetre, width=800 / xlen, height=700 / ylen, bg="green").grid(column=colonne, row=ligne)
            elif grille_init[ligne][colonne] == "R":
                if [x,y]==[colonne,ligne]:
                    color="violet"
                Canvas(fenetre, width=800 / xlen, height=700 / ylen, bg="violet").grid(column=colonne, row=ligne)
            else :
                if [x,y]==[colonne,ligne]:
                    color="blue"
                Canvas(fenetre, width=800 / xlen, height=700 / ylen, bg="blue").grid(column=colonne, row=ligne)
    Label(text="X", font="Arial 25 bold", fg="white", bg=color).grid(row=y, column=x)
    Label(fenetre, text="Gasper a encore "+str(joueur["energie"])+" vies").grid(row=ylen+1, columnspan=xlen+5)
    
## trouver la position du joueur à tout moment dans le chateau
def position(grille):
    for y in range(len(grille)):
        for x in range(len(grille[y])):
            if grille[y][x]=="X":
                idx=x
                idy=y
    return idx,idy


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
        showinfo("Energie","Vous avez trouvé "+str(pintes)+" pintes d'énergie ! Gasper a maintenant "+str(joueur["energie"])+" points d'énergie")
    return joueur


### LES MECHANTS ###

## définir l'action du maitre du chateau
def action_maitre(coor,grille,grille_init,x,y,joueur,fenetre):
    showinfo("Maitre", "Oh non ! Vous êtes nez à nez avec le maître du chateau !\nIl vous a renvoyé dans la case réception")
    grille[y][x]="S"
    x,y=coor[0]
    grille[y][x]="X"
    affiche_chateau(grille,grille_init,joueur,fenetre)
    return x,y

## définir l'action du savant fou
def action_savant(joueur,grille,grille_init,x,y,coor_vide,coor_paradis,xlen,ylen,fenetre):
    showinfo("Savant","Oh non ! Le savant vous attaque !\nVous perdez 1 pinte de vie et vous êtes envoyé dans une autre salle")
    joueur["energie"]=joueur["energie"]-1
    if joueur["energie"]<=0:
        fin_jeu_energie()
    grille[y][x]="S"
    x=0
    y=0
    while ([x,y] in coor_vide) or ([x,y] in coor_paradis):
        x=random.randrange(xlen)
        y=random.randrange(ylen)
    grille[y][x]="X"
    affiche_chateau(grille,grille_init,joueur,fenetre)
    showinfo("Savant","Gasper a maintenant "+str(joueur["energie"])+" points d'énergie")
    return x,y,joueur

## définir l'action du Bibbendum Chamallow
def action_bibbendum(joueur):
    showinfo("Bibbendum","Oh non ! Bibbendum Chamallow vous a paralysé avec sa mousse ! \nVous perdez 2 pintes d'énergies\n\nGasper a maintenant "+str(joueur["energie"])+" points d'énergie")
    joueur["energie"]=joueur["energie"]-2
    if joueur["energie"]<=0:
        fin_jeu_energie()
    return joueur

## mettre en place les méchants et les pintes d'énergie
def place_item(coordonnees,monstres,pintes):
    coor=copy.deepcopy(coordonnees)
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
def monster(x,y,joueur,grille,grille_init,coor_monstres,coor_reception,coor_vide,coor_paradis,xlen,ylen,fenetre):
    if [x,y] in coor_monstres.values():
        if [x,y] == coor_monstres["maitre_chateau"] :
            x,y=action_maitre(coor_reception,grille,grille_init,x,y,joueur,fenetre)
        elif [x,y] == coor_monstres["savant_fou"]:
            x,y,joueur=action_savant(joueur,grille,grille_init,x,y,coor_vide,coor_paradis,xlen,ylen,fenetre)
        else :
            joueur=action_bibbendum(joueur)
    return x,y,joueur

## définir les cordonnées sur lesquels apparaissent les avertissements
def avert(coor_monstres):
    coor_advert={"maitre_chateau":[],"savant_fou":[],"bibbendum_chamallow1":[],"bibbendum_chamallow2":[],"bibbendum_chamallow3":[]}
    for ind in coor_monstres.keys():
        pos1=copy.deepcopy(coor_monstres[ind])
        pos1[0]-=1
        coor_advert[ind].append(pos1)
        pos2=copy.deepcopy(coor_monstres[ind])
        pos2[0]+=1
        coor_advert[ind].append(pos2)
        pos3=copy.deepcopy(coor_monstres[ind])
        pos3[1]-=1
        coor_advert[ind].append(pos3)
        pos4=copy.deepcopy(coor_monstres[ind])
        pos4[1]+=1
        coor_advert[ind].append(pos4)
    return coor_advert

## définir les cris d'avertissement
def cri(coor_advert,x,y,fenetre):
    maitre=coor_advert["maitre_chateau"]
    savant=coor_advert["savant_fou"]
    bibbendum=["bibbendum_chamallow1","bibbendum_chamallow2","bibbendum_chamallow3"]
    bc=[]
    for b in bibbendum :
        for coor in coor_advert[b]:
            bc.append(coor)
    if ([x,y] in maitre) or ([x,y] in savant) or ([x,y] in bc) :
        if [x,y] in maitre:
            showinfo("Alerte","Qu'est-ce qu'on entend ? On dirait le son de clés...")
        elif [x,y] in savant:
            showinfo("Alerte","Ha ha ha ha !!")
        elif [x,y] in bc:
            showinfo("Alert","Ca sent le chamallow fraise...")
        

### JEU ###

## début du jeu
def init_jeu(grille,coor,fenetre,xlen,ylen):
    for ligne in range(ylen):
        for colonne in range(xlen):
            Canvas(fenetre, width=800 / xlen, height=700 / ylen, bg="black").grid(column=colonne,row=ligne)
    Label(fenetre,text="Gasper, le gentil fantôme d’un chateau, aimerait pouvoir retourner dans le monde des fantômes \noù il fait toujours beau et où tous ses amis l’attendent. Mais il est perdu dans un labyrinthe de pièces dont il ne trouve plus la sortie... \nVoulez-vous l'aider à braver tous les dangers ?").grid(row=ylen,columnspan=xlen)
    Label(fenetre, text="Où voulez-vous aller ? Utilisez les fléches directionnelles du clavier").grid(row=ylen+2, columnspan=xlen+5)
    Button(fenetre, text="Quitter", command=fenetre.quit).grid(row=ylen + 2, column=xlen + 1)
    grille=salle(grille,coor,"X")
    return grille

## fin du jeu : manque d'énergie
def fin_jeu_energie():
    showinfo("End","Gasper n'a plus d'énergie ! \nVous avez perdu")
    sys.exit()

## fin du jeu : arrivée au paradis
def fin_jeu_paradis():
    showinfo("End","Gasper le gentil fantôme a atteint le paradis. Bravo ! grâce à vous il a retrouvé tous ses amis ! \nVous avez gagné")
    sys.exit()

## gestion des déplacements
def jeu(event,grille,grille_init,joueur,coor_vide,coor_salles,coor_paradis,coor_reception,coor_monstres,coor_energie,xlen,ylen,fenetre):
    coor_advert=avert(coor_monstres)
    x,y=position(grille)
    tmp=grille_init[y][x]
    tmp_coor=copy.deepcopy([x,y])
    option=event.keysym
    while option not in ["Left","Right","Up","Down","Escape","Enter"]:
        showinfo("Attention","Pas une option de déplacement")
        break
    if (option=="Left") and (grille[y][x-1] != " "):
        x-=1
    elif (option=="Right") and (grille[y][x+1] != " "):
        x+=1
    elif (option=="Up") and (grille[y-1][x] != " "):
        y-=1
    elif (option=="Down") and (grille[y+1][x] != " "):
        y+=1
    elif option=="Escape" :
        sys.exit()
    else:
        showinfo("Attention","C'est un mur")
    grille[tmp_coor[1]][tmp_coor[0]]=tmp
    tmp=grille_init[y][x]
    grille[y][x]="X"
    affiche_chateau(grille,grille_init,joueur,fenetre)
    if tmp=="*":
        cri(coor_advert,x,y,fenetre)
    elif tmp=="S":
        x,y,joueur=monster(x,y,joueur,grille,grille_init,coor_monstres,coor_reception,coor_vide,coor_paradis,xlen,ylen,fenetre)
        joueur=action_energie(x,y,joueur,coor_energie)
    elif tmp=="P":
        fin_jeu_paradis()
    

### INITIALISATION DU JEU ###
    
def FantomeEscape():
    chateau,coor_vide,coor_salles,coor_paradis,coor_reception,coor_monstres,coor_energie,xlen,ylen = definir_chateau()   # on définit le chateau et toutes ses salles, et on place les pintes d'énergie et les mosntres
    joueur=fantome(3)       # on initialise le joueur

    fenetre = Tk()

    chateau_init=copy.deepcopy(chateau)
    chateau=init_jeu(chateau,coor_reception,fenetre,xlen,ylen)
    affiche_chateau(chateau,chateau_init,joueur,fenetre)
    fenetre.focus_set()
    def Game(event,grille=chateau,grille_init=chateau_init,joueur=joueur,coor_vide=coor_vide,coor_salles=coor_salles,coor_paradis=coor_paradis,coor_reception=coor_reception,coor_monstres=coor_monstres,coor_energie=coor_energie,xlen=xlen,ylen=ylen,fenetre=fenetre):
        return jeu(event,grille,grille_init,joueur,coor_vide,coor_salles,coor_paradis,coor_reception,coor_monstres,coor_energie,xlen,ylen,fenetre)
    fenetre.bind("<KeyPress>", Game)

    fenetre.mainloop()

##### MAIN #####

FantomeEscape()

"""

Projet Programmation FantomeEscape
code avec interface graphique
Jean-Clément GALLARDO - Amélie GRUEL
Novembre 2018

"""

#!/bin/Python
#coding=utf-8
import copy
import random
import sys
from Tkinter import *
from tkinter.messagebox import *


### LE CHATEAU ###

def cree_chateau(x0,y0):
    ly=[]
    for y in range(y0):
        lx=[]
        for x in range(x0):
            lx.append("*")
        ly.append(lx)
    return ly

def ajout_salle(grille,coordonnees,valeur):
    for c in coordonnees :
        grille[c[1]][c[0]]=valeur
    return grille


def definir_chateau():    
    xlen=15                             # la matrice a 15 colonnes
    ylen=11                             # la matrice a 11 lignes
    chateau=cree_chateau(xlen,ylen)     
    
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
def affiche_chateau(grille,grille_init,joueur,fenetre):
    xlen = len(grille[0])
    ylen = len(grille)
    x,y = position_joueur(grille)
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

def action_energie(x,y,joueur,coordonnees_energie):
    pintes=0
    for pos_pinte in coordonnees_energie.items():
        if [x,y] == pos_pinte[1] :
            joueur["energie"]+=1
            pintes+=1
            del coordonnees_energie[pos_pinte[0]]
    if pintes != 0 :
        showinfo("Energie","Vous avez trouvé "+str(pintes)+" pintes d'énergie ! Gasper a maintenant "+str(joueur["energie"])+" points d'énergie")
    return joueur


### LES MECHANTS ###

def action_maitre(grille,grille_init,x,y,joueur,fenetre):
    showinfo("Maitre", "Oh non ! Vous êtes nez à nez avec le maître du chateau !\nIl vous a renvoyé dans la case réception")
    grille[y][x]="S"
    coordonnees=trouve_coordonnees(grille,"R")
    x,y=coordonnees[0]
    grille[y][x]="X"
    affiche_chateau(grille,grille_init,joueur,fenetre)
    return x,y

def action_savant(joueur,grille,grille_init,x,y,xlen,ylen,fenetre):
    showinfo("Savant","Oh non ! Le savant vous attaque !\nVous perdez 1 pinte de vie et vous êtes envoyé dans une autre salle")
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
    grille[y][x]="X"
    affiche_chateau(grille,grille_init,joueur,fenetre)
    showinfo("Savant","Gasper a maintenant "+str(joueur["energie"])+" points d'énergie")
    return x,y,joueur

def action_bibbendum(joueur):
    showinfo("Bibbendum","Oh non ! Bibbendum Chamallow vous a paralysé avec sa mousse ! \nVous perdez 2 pintes d'énergies\n\nGasper a maintenant "+str(joueur["energie"])+" points d'énergie")
    joueur["energie"]=joueur["energie"]-2
    if joueur["energie"]<=0:
        fin_jeu_energie()
    return joueur

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
        for pinte in range(nb_pintes):
            coordonnees_energie[pintes[pinte]]=tmp
        pintes=pintes[nb_pintes:]
    return coordonnees_monstres,coordonnees_energie

def action_monstre(x,y,joueur,grille,grille_init,coordonnees_monstres,xlen,ylen,fenetre):
    if [x,y] in coordonnees_monstres.values():
        if [x,y] == coordonnees_monstres["maitre_chateau"] :
            x,y=action_maitre(grille,grille_init,x,y,joueur,fenetre)
        elif [x,y] == coordonnees_monstres["savant_fou"]:
            x,y,joueur=action_savant(joueur,grille,grille_init,x,y,xlen,ylen,fenetre)
        else :
            joueur=action_bibbendum(joueur)
    return x,y,joueur

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

def cri(coordonnees,x,y,fenetre):
    maitre=coordonnees["maitre_chateau"]
    savant=coordonnees["savant_fou"]
    bibbendum=["bibbendum_chamallow1","bibbendum_chamallow2","bibbendum_chamallow3"]
    bc=[]
    for b in bibbendum :
        for coordonnee in coordonnees[b]:
            bc.append(coordonnee)
    if [x,y] in maitre:
        showinfo("Alerte","Qu'est-ce qu'on entend ? On dirait le son de clés...")
    elif [x,y] in savant:
        showinfo("Alerte","Ha ha ha ha !!")
    elif [x,y] in bc:
        showinfo("Alert","Ca sent le chamallow fraise...")
        

### JEU ###

def init_jeu(grille,fenetre,xlen,ylen):
    for ligne in range(ylen):
        for colonne in range(xlen):
            Canvas(fenetre, width=800 / xlen, height=700 / ylen, bg="black").grid(column=colonne,row=ligne)
    Label(fenetre,text="Gasper, le gentil fantôme d’un chateau, aimerait pouvoir retourner dans le monde des fantômes \noù il fait toujours beau et où tous ses amis l’attendent. Mais il est perdu dans un labyrinthe de pièces dont il ne trouve plus la sortie... \nVoulez-vous l'aider à braver tous les dangers ?").grid(row=ylen,columnspan=xlen)
    Label(fenetre, text="Où voulez-vous aller ? Utilisez les fléches directionnelles du clavier").grid(row=ylen+2, columnspan=xlen+5)
    Button(fenetre, text="Quitter", command=fenetre.quit).grid(row=ylen + 2, column=xlen-2,columnspan=2)
    coordonnees=trouve_coordonnees(grille,"R")
    grille=ajout_salle(grille,coordonnees,"X")
    return grille

## fin du jeu : manque d'énergie
def fin_jeu_energie():
    showinfo("End","Gasper n'a plus d'énergie ! \nVous avez perdu")
    sys.exit()

def fin_jeu_paradis():
    showinfo("End","Gasper le gentil fantôme a atteint le paradis. Bravo ! grâce à vous il a retrouvé tous ses amis ! \nVous avez gagné")
    sys.exit()

def jeu(event,grille,grille_init,joueur,coordonnees_monstres,coordonnees_energie,xlen,ylen,fenetre):
    avertissement=coordonnees_avertissement(coordonnees_monstres)
    x,y=position_joueur(grille)
    tmp=grille_init[y][x]
    tmp_coordonnees=copy.deepcopy([x,y])
    option=event.keysym
    if option not in ["Left","Right","Up","Down"]:
        showinfo("Attention","Pas une option de déplacement")
    elif (option=="Left") and (grille[y][x-1] != " "):
        x-=1
    elif (option=="Right") and (grille[y][x+1] != " "):
        x+=1
    elif (option=="Up") and (grille[y-1][x] != " "):
        y-=1
    elif (option=="Down") and (grille[y+1][x] != " "):
        y+=1
    else :
        showinfo("Attention","C'est un mur")
    grille[tmp_coordonnees[1]][tmp_coordonnees[0]]=tmp
    tmp=grille_init[y][x]
    grille[y][x]="X"
    affiche_chateau(grille,grille_init,joueur,fenetre)
    if tmp=="*":
        cri(avertissement,x,y,fenetre)
    elif tmp=="S":
        x,y,joueur=action_monstre(x,y,joueur,grille,grille_init,coordonnees_monstres,xlen,ylen,fenetre)
        joueur=action_energie(x,y,joueur,coordonnees_energie)
    elif tmp=="P":
        fin_jeu_paradis()
    

### INITIALISATION DU JEU ###
    
def FantomeEscape():
    chateau,coordonnees_monstres,coordonnees_energie,xlen,ylen = definir_chateau()   # on définit le chateau et toutes ses salles, et on place les pintes d'énergie et les mosntres
    joueur=fantome(3)       # on initialise le joueur

    fenetre = Tk()

    chateau_init=copy.deepcopy(chateau)
    chateau=init_jeu(chateau,fenetre,xlen,ylen)
    affiche_chateau(chateau,chateau_init,joueur,fenetre)
    fenetre.focus_set()
    def Game(event,grille=chateau,grille_init=chateau_init,joueur=joueur,coordonnees_monstres=coordonnees_monstres,coordonnees_energie=coordonnees_energie,xlen=xlen,ylen=ylen,fenetre=fenetre):
        return jeu(event,grille,grille_init,joueur,coordonnees_monstres,coordonnees_energie,xlen,ylen,fenetre)
    fenetre.bind("<KeyPress>", Game)

    fenetre.mainloop()

##### MAIN #####

FantomeEscape()

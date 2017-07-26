# Créé par ISN_2016 , le 25/04/2016 en Python 3.2
#-*- coding: utf-8 -*-


from tkinter import *
from random import randint
import winsound


""" Touches Mouvements : Haut
                         Bas
                         Droite
                         Gauche

    Touches Attaque :    Espace
"""


#################################
""" Définition des fonctions """
#################################




# Ajout d'une touche à la liste
def enfoncee(evt) :
    if evt.keysym not in touches :
        touches.append(evt.keysym)




# Suppression d'une touche de la liste
def relachee(evt) :
    if evt.keysym in touches :
        touches.remove(evt.keysym)

"""_______________________________________________________"""

###############################
# Animations des Personnages :
###############################

def animation() :
    global Xp, Yp, Anim, num, dialogue, Xt1, Yt1, Xt2, Yt2, Xa, Ya, money, end
    Xpav, Ypav = Xp, Yp
    if "Up" in touches :
        if Decors[(Yp-16)//64][(Xp)//64]  in (' ','-','O','P','i', 'm', 'c', 'w', 'v','n','!','b','W','a','f','s','o','k','u') :
            Yp = Yp - 8
            NomFichier = 'PERSOH'
        if "space" in touches :
            NomFichier = 'PERSOAH'

    if "Down" in touches :
        if Decors[(Yp+32)//64][(Xp)//64]  in (' ','-','O','P','i', 'm', 'c', 'w', 'v','n','!','b','W','a','f','s','o','k','u') :
            Yp = Yp + 8
            NomFichier = 'PERSOB'
        if "space" in touches :
            NomFichier = 'PERSOAB'

    if "Left" in touches :
        if Decors[(Yp)//64][(Xp-32)//64]  in (' ','-','O','P','i', 'm', 'c', 'w', 'v','n','!','b','W','a','f','s','o','k','u') :
            Xp = Xp - 8
            NomFichier = 'PERSOG'
        if "space" in touches :
            NomFichier = 'PERSOAG'

    if "Right" in touches :
        if Decors[(Yp)//64][(Xp+32)//64]  in (' ','-','O','P','i', 'm', 'c', 'w', 'v','n','!','b','W','a','f','s','o','k','u') :
            Xp = Xp + 8
            NomFichier = 'PERSOD'
        if "space" in touches :
            NomFichier = 'PERSOAD'

    if Decors[(Yp)//64][(Xp+32)//64]  in '0' :
        Xpav, Ypav = Xp, Yp


    # Combats
    if Xt1-50 < Xp < Xt1+50 and Yt1-50 < Yp < Yt1+50 :
        if "space" in touches :
            winsound.PlaySound("sons/zombie.wav", winsound.SND_ASYNC)
            boite.delete('trolln1')
            Xt1, Yt1 = -32, -32
        if "space" not in touches :
            boite.itemconfigure(sprite, image=PERSOM)

    if Xt2-50 < Xp < Xt2+50 and Yt2-50 < Yp < Yt2+50 :
        if "space" in touches :
            winsound.PlaySound("sons/zombie.wav", winsound.SND_ASYNC)
            boite.delete('trolln2')
            Xt2, Yt2 = -32, -32
        if "space" not in touches :
            boite.itemconfigure(sprite, image=PERSOM)

    if Xa-50 < Xp < Xa+50 and Ya-50 < Yp < Ya+50 :
        if "space" in touches :
            winsound.PlaySound("sons/criscorpionquimeurt.wav", winsound.SND_ALIAS)
            boite.delete('boss')
            Xa, Ya = -32, -32
            dialogue=2
        if "space" not in touches :
            boite.itemconfigure(sprite, image=PERSOM)


    # Changement de tableau
    if num!=103 and num!=104:
        if Decors[(Yp)//64][(Xp)//64]  in ('b') :
            num +=1
            fenetre.destroy()

    #tableaux speciaux(15-100-101)
    if Decors[(Yp)//64][(Xp)//64]  in ('W') :
        num =15
        fenetre.destroy()

    if Decors[(Yp)//64][(Xp)//64]  in ('u') :
        if num==7 :
            num= 100
            fenetre.destroy()
        if num==8 :
            num= 101
            fenetre.destroy()

    if Decors[(Yp)//64][(Xp)//64]  in ('s') :
        if num==101:
            num=104
            fenetre.destroy()
        if num==100:
            num= 103
            fenetre.destroy()

    if num==103:
        if Decors[(Yp)//64][(Xp)//64]  in ('b') :
            num=8
            fenetre.destroy()

    if num==104:
        if Decors[(Yp)//64][(Xp)//64]  in ('b') :
            num=9
            fenetre.destroy()



    # Dialogues
    if num==1 :
        if Decors[(Yp)//64][(Xp)//64]  in (' ') :
            if dialogue==0 :
                boite.create_image(0, 0, image=jack, anchor=NW, tags='bulle')
                winsound.PlaySound("sons/dialogue.wav", winsound.SND_ASYNC)
                dialogue=1

    if num==3 :
        if Decors[(Yp)//64][(Xp)//64]  in ('o') :
            if dialogue==0 :
                boite.create_image(0, 0, image=tatidou, anchor=NW, tags='bulle')
                winsound.PlaySound("sons/dialogue.wav", winsound.SND_ASYNC)
                dialogue=1

        if Decors[(Yp)//64][(Xp)//64]  in (' ') :
            if dialogue==1 :
                boite.delete('bulle')
                boite.create_image(0, 0, image=epee, anchor=NW, tags='bulle')
                winsound.PlaySound("sons/item.wav", winsound.SND_ASYNC)
                dialogue=2


    if num==15 :
        if Decors[(Yp)//64][(Xp)//64]  in (' ') :
            if dialogue==0 :
                boite.create_image(0, 0, image=theargoste, anchor=NW, tags='bulle')
                winsound.PlaySound("sons/dialogue.wav", winsound.SND_ALIAS)
                winsound.PlaySound("sons/boss.wav", winsound.SND_ASYNC)
                dialogue=1

        if dialogue==2 :
            boite.create_image(0, 0, image=tatidou_fin, anchor=NW, tags='bulle')
            boite.create_image(Xp+64, Yp, image=PNJ1, anchor=NW)
            winsound.PlaySound("sons/dialogue.wav", winsound.SND_ALIAS)
            winsound.PlaySound("sons/fete.wav", winsound.SND_ASYNC)
            dialogue=3
            end=1



    if 'Return' in touches :
        if end==0 :
            boite.delete('bulle')
        if end==1 :
            num=16
            fenetre.destroy()

    if Decors[(Yp)//64][(Xp)//64]  in ('k') :
        if money==0 :
            winsound.PlaySound("sons/geme.wav", winsound.SND_ASYNC)
            boite.delete('geme')
            money=1




    # Animation
    if (Xpav, Ypav) != (Xp, Yp) :
        Anim = 1 - Anim
        boite.itemconfigure(sprite, image=eval(NomFichier+str(Anim)))


    boite.coords(sprite, Xp, Yp)
    fenetre.after(90,animation)




def troll1() :
    global Xt1, Yt1, AnimM1
    Xt1av, Yt1av = Xt1, Yt1

    if Decors[(Yt1)//64][(Xt1)//64]  in ('i', 'm') :
        Yt1 = Yt1 - 8
        NomFichier = 'MONSTREH'


    if Decors[(Yt1)//64][(Xt1)//64]  in ('c') :
        Yt1 = Yt1 + 8
        NomFichier = 'MONSTREB'

    if Decors[(Yt1)//64][(Xt1)//64]  in ('w','n') :
        Xt1 = Xt1 - 8
        NomFichier = 'MONSTREG'

    if Decors[(Yt1)//64][(Xt1)//64]  in ('v') :
        Xt1 = Xt1 + 8
        NomFichier = 'MONSTRED'

    if (Xt1av, Yt1av) != (Xt1, Yt1) :
        AnimM1 = 1 - AnimM1
        boite.itemconfigure(monstre1, image=eval(NomFichier+str(AnimM1)))


    boite.coords(monstre1, Xt1, Yt1)
    fenetre.after(70,troll1)





def troll2() :
    global Xt2, Yt2, AnimM2
    Xt2av, Yt2av = Xt2, Yt2

    if Decors[(Yt2)//64][(Xt2)//64]  in ('i','m') :
        Yt2 = Yt2 - 8
        NomFichier = 'MONSTREH'


    if Decors[(Yt2)//64][(Xt2)//64]  in ('c') :
        Yt2 = Yt2 + 8
        NomFichier = 'MONSTREB'

    if Decors[(Yt2)//64][(Xt2)//64]  in ('w', 'n') :
        Xt2 = Xt2 - 8
        NomFichier = 'MONSTREG'

    if Decors[(Yt2)//64][(Xt2)//64]  in ('v') :
        Xt2 = Xt2 + 8
        NomFichier = 'MONSTRED'

    if (Xt2av, Yt2av) != (Xt2, Yt2) :
        AnimM2 = 1 - AnimM2
        boite.itemconfigure(monstre2, image=eval(NomFichier+str(AnimM2)))


    boite.coords(monstre2, Xt2, Yt2)
    fenetre.after(70,troll2)




def PNJ() :
    global Yj, Xj, AnimJ

    if Decors[(Yj)//64][(Xj)//64]  in ('j') :
        NomFichier = 'PNJ'
        AnimJ = 1 - AnimJ
        boite.itemconfigure(pnj, image=eval(NomFichier+str(AnimJ)))
    fenetre.after(1000,PNJ)




def argoste() :
    global Ya, Xa, AnimA
    NomFichier = 'ARGOSTE'

    if Decors[(Ya)//64][(Xa)//64]  in ('a',' ','P') :
        Xa = Xa + randint(-100,100)
        Ya = Ya + randint(-100,100)

    if IndexError  :
        Xa = randint(64,1216)
        Ya = randint(64,768)

    if Decors[(Ya)//64][(Xa)//64]  in ('1','2','3','4','5','6','7','8','9','d','f','g','h')  :
        Xa = randint(64,1216)
        Ya = randint(64,768)

    AnimA = 1 - AnimA
    boite.itemconfigure(largoste, image=eval(NomFichier+str(AnimA)))
    boite.coords(largoste, Xa, Ya)
    fenetre.after(2000,argoste)


# PNJs de la dernière salle (16)

def Machin() :
    global Ymachin, Xmachin, AnimJ

    if Decors[(Ymachin)//64][(Xmachin)//64]  in ('e') :
        NomFichier = 'MACHIN'
        AnimJ = 1 - AnimJ # Tempo
        boite.itemconfigure(machin, image=eval(NomFichier+str(AnimJ)))
    fenetre.after(200,Machin)

def Fille() :
    global Yfille, Xfille, AnimJ

    if Decors[(Yfille)//64][(Xfille)//64]  in ('x') :
        NomFichier = 'FILLE'
        boite.itemconfigure(fille, image=eval(NomFichier+str(AnimJ)))
    fenetre.after(200,Fille)

def Mario() :
    global Ymario, Xmario, AnimJ

    if Decors[(Ymario)//64][(Xmario)//64]  in ('y') :
        NomFichier = 'MARIO'
        boite.itemconfigure(mario, image=eval(NomFichier+str(AnimJ)))
    fenetre.after(200,Mario)

def Luigi() :
    global Yluigi, Xluigi, AnimJ

    if Decors[(Yluigi)//64][(Xluigi)//64]  in ('l') :
        NomFichier = 'LUIGI'
        boite.itemconfigure(luigi, image=eval(NomFichier+str(AnimJ)))
    fenetre.after(200,Luigi)

def Binoclare() :
    global Ybinoclare, Xbinoclare, AnimJ

    if Decors[(Ybinoclare)//64][(Xbinoclare)//64]  in ('$') :
        NomFichier = 'BINOCLARE'
        boite.itemconfigure(binoclare, image=eval(NomFichier+str(AnimJ)))
    fenetre.after(200,Binoclare)

def Chelou() :
    global Ychelou, Xchelou, AnimJ

    if Decors[(Ychelou)//64][(Xchelou)//64]  in ('€') :
        NomFichier = 'CHELOU'
        boite.itemconfigure(chelou, image=eval(NomFichier+str(AnimJ)))
    fenetre.after(200,Chelou)


"""______________________________________________"""



# Lecture du fichier contenant la boite

def charge_boite(nom) :
    fichier = open(nom + ".txt", "r")
    data = fichier.readlines()
    fichier.close()
    return data



# Dessin de l'interface graphique

def dessine():
    global Xp, Yp, Xt1, Yt1, Xt2, Yt2, Xj, Yj, Xa, Ya, X0, Y0, Xmachin, Ymachin, Xfille, Yfille
    global  Xmario, Ymario, Xluigi, Yluigi, Xbinoclare, Ybinoclare, Xchelou, Ychelou, t1, t2, b,num

    # Textures Environnement
    ligne, colonne = 0, 0
    while ligne < 13 :
        if Decors[ligne][colonne] == 'X' :
            boite.create_image(colonne*64, ligne*64, image=X, anchor=NW)
        if Decors[ligne][colonne] == 'A' :
            boite.create_image(colonne*64, ligne*64, image=A, anchor=NW)
        if Decors[ligne][colonne] == 'H' :
            boite.create_image(colonne*64, ligne*64, image=H, anchor=NW)
        if Decors[ligne][colonne] == ' ' :
            boite.create_image(colonne*64, ligne*64, image=R, anchor=NW)
        if Decors[ligne][colonne] == 'B' :
            boite.create_image(colonne*64, ligne*64, image=B, anchor=NW)
        if Decors[ligne][colonne] == 'V' :
            boite.create_image(colonne*64, ligne*64, image=V, anchor=NW)
        if Decors[ligne][colonne] == 'N' :
            boite.create_image(colonne*64, ligne*64, image=N, anchor=NW)
        if Decors[ligne][colonne] == 'M' :
            boite.create_image(colonne*64, ligne*64, image=M, anchor=NW)
        if Decors[ligne][colonne] == 'K' :
            boite.create_image(colonne*64, ligne*64, image=K, anchor=NW)
        if Decors[ligne][colonne] == 'E' :
            boite.create_image(colonne*64, ligne*64, image=E, anchor=NW)
        if Decors[ligne][colonne] == 'I' :
            boite.create_image(colonne*64, ligne*64, image=I, anchor=NW)
        if Decors[ligne][colonne] == 'L' :
            boite.create_image(colonne*64, ligne*64, image=L, anchor=NW)
        if Decors[ligne][colonne] == 'T' :
            boite.create_image(colonne*64, ligne*64, image=T, anchor=NW)
        if Decors[ligne][colonne] == 'G' :
            boite.create_image(colonne*64, ligne*64, image=G, anchor=NW)
        if Decors[ligne][colonne] == 'Q' :
            boite.create_image(colonne*64, ligne*64, image=Q, anchor=NW)
        if Decors[ligne][colonne] == 'U' :
            boite.create_image(colonne*64, ligne*64, image=U, anchor=NW)
        if Decors[ligne][colonne] == 'C' :
            boite.create_image(colonne*64, ligne*64, image=C, anchor=NW)
        if Decors[ligne][colonne] == 'J' :
            boite.create_image(colonne*64, ligne*64, image=J, anchor=NW)
        if Decors[ligne][colonne] == 'O' :
            boite.create_image(colonne*64, ligne*64, image=O, anchor=NW)
        if Decors[ligne][colonne] == '-' :
            boite.create_image(colonne*64, ligne*64, image=Y, anchor=NW)
        if Decors[ligne][colonne] == 'W' :
            boite.create_image(colonne*64, ligne*64, image=W, anchor=NW)
        if Decors[ligne][colonne] == 'F' :
            boite.create_image(colonne*64, ligne*64, image=F, anchor=NW)
        if Decors[ligne][colonne] == 'D' :
            boite.create_image(colonne*64, ligne*64, image=D, anchor=NW)
        if Decors[ligne][colonne] == 'S' :
            boite.create_image(colonne*64, ligne*64, image=S, anchor=NW)
        if Decors[ligne][colonne] == 'Z' :
            boite.create_image(colonne*64, ligne*64, image=Z, anchor=NW)
        if Decors[ligne][colonne] == 'z' :
            boite.create_image(colonne*64, ligne*64, image=z, anchor=NW)
        if Decors[ligne][colonne] == '!' :
            boite.create_image(colonne*64, ligne*64, image=q, anchor=NW)
        if Decors[ligne][colonne] == '1' :
            boite.create_image(colonne*64, ligne*64, image=mur11, anchor=NW)
        if Decors[ligne][colonne] == '2' :
            boite.create_image(colonne*64, ligne*64, image=mur12, anchor=NW)
        if Decors[ligne][colonne] == '3' :
            boite.create_image(colonne*64, ligne*64, image=mur21, anchor=NW)
        if Decors[ligne][colonne] == '4' :
            boite.create_image(colonne*64, ligne*64, image=mur22, anchor=NW)
        if Decors[ligne][colonne] == '5' :
            boite.create_image(colonne*64, ligne*64, image=mur31, anchor=NW)
        if Decors[ligne][colonne] == '6' :
            boite.create_image(colonne*64, ligne*64, image=mur32, anchor=NW)
        if Decors[ligne][colonne] == '7' :
            boite.create_image(colonne*64, ligne*64, image=mur41, anchor=NW)
        if Decors[ligne][colonne] == '8' :
            boite.create_image(colonne*64, ligne*64, image=mur42, anchor=NW)
        if Decors[ligne][colonne] == 'h' :
            boite.create_image(colonne*64, ligne*64, image=mur1, anchor=NW)
        if Decors[ligne][colonne] == 'd' :
            boite.create_image(colonne*64, ligne*64, image=mur2, anchor=NW)
        if Decors[ligne][colonne] == 'f' :
            boite.create_image(colonne*64, ligne*64, image=mur3, anchor=NW)
        if Decors[ligne][colonne] == 'g' :
            boite.create_image(colonne*64, ligne*64, image=mur4, anchor=NW)
        if Decors[ligne][colonne] == 'r' :
            boite.create_image(colonne*64, ligne*64, image=porte1, anchor=NW)
        if Decors[ligne][colonne] == 't' :
            boite.create_image(colonne*64, ligne*64, image=porte2, anchor=NW)

        if Decors[ligne][colonne] == 'k' :
            boite.create_image(colonne*64, ligne*64, image=geme, anchor=NW, tags='geme')



        # Textures Perso

        if Decors[ligne][colonne] == 'P' :
            Xp, Yp = X0+colonne*64+32, Y0+ligne*64+32

        if Decors[ligne][colonne] == 'm' :
            Xt1, Yt1 = X0+colonne*64+32, Y0+ligne*64+32
            t1=1

        if Decors[ligne][colonne] != 'm' and t1==0:
            Xt1, Yt1 = -32, -32

        if Decors[ligne][colonne] == 'n' :
            Xt2, Yt2 = X0+colonne*64+32, Y0+ligne*64+32
            t2=1

        if Decors[ligne][colonne] != 'n' and t2==0 :
            Xt2, Yt2 = -32, -32

        if Decors[ligne][colonne] == 'j' :
            Xj, Yj = colonne*64+32, ligne*64+32

        if Decors[ligne][colonne] == 'a' :
            Xa, Ya = X0+colonne*64, Y0+ligne*64
            b=1

        if Decors[ligne][colonne] != 'a' and b==0 :
            Xa, Ya = -32, -32

        if Decors[ligne][colonne] == 'e' :
            Xmachin, Ymachin = colonne*64+32, ligne*64+32

        if Decors[ligne][colonne] == 'x' :
            Xfille, Yfille = colonne*64+32, ligne*64+32

        if Decors[ligne][colonne] == 'y' :
            Xmario, Ymario = colonne*64+32, ligne*64+32

        if Decors[ligne][colonne] == 'l' :
            Xluigi, Yluigi = colonne*64+32, ligne*64+32

        if Decors[ligne][colonne] == '$' :
            Xbinoclare, Ybinoclare = colonne*64+32, ligne*64+32

        if Decors[ligne][colonne] == '€' :
            Xchelou, Ychelou = colonne*64+32, ligne*64+32







        colonne=colonne+1
        if colonne == 20 :
            colonne = 0
            ligne = ligne + 1




def textures():
        global A,Z,E,R,T,Y,U,I,O,P,Q,S,D,F,G,H,J,K,L,M,W,X,C,V,B,N,z,q,geme,mur1,mur11,mur12,mur2
        global mur21,mur22,mur3,mur31,mur32,mur4,mur41,mur42,porte1,porte2,PNJ0,PNJ1,PERSOAB0
        global PERSOAB1,PERSOAD0,PERSOAD1,PERSOAG0,PERSOAG1,PERSOAH0,PERSOAH1,PERSOB0
        global PERSOB1,PERSOD0,PERSOD1,PERSOG0,PERSOG1,PERSOH0,PERSOH1,PERSOM,MONSTREB0
        global MONSTREB1,MONSTRED0,MONSTRED1,MONSTREG0,MONSTREG1,MONSTREH0,MONSTREH1,ARGOSTE0,ARGOSTE1
        #Chargement des fichiers :
        #Roches
        X=PhotoImage(file = "images/cailloux_bas_milieu.gif")
        H=PhotoImage(file = "images/cailloux_haut_milieu.gif")
        V=PhotoImage(file = "images/cailloux_bas_gauche.gif")
        N=PhotoImage(file = "images/cailloux_bas_droite.gif")
        M=PhotoImage(file = "images/cailloux_haut_gauche.gif")
        K=PhotoImage(file = "images/cailloux_haut_droite.gif")

        #Random
        A=PhotoImage(file = "images/arbre.gif")
        R=PhotoImage(file = "images/sol1.gif")
        Y=PhotoImage(file = "images/sol2.gif")
        B=PhotoImage(file = "images/buisson.gif")
        F=PhotoImage(file = "images/tombe.gif")
        W=PhotoImage(file = "images/escalier.gif")
        O=PhotoImage(file = "images/pont.gif")
        D=PhotoImage(file = "images/garde.gif")
        S=PhotoImage(file = "images/maison1.gif")
        Z=PhotoImage(file = "images/maison2.gif")
        z=PhotoImage(file = "images/maison3.gif")
        q=PhotoImage(file = "images/quest.gif")
        geme=PhotoImage(file = "images/geme.gif")


        #Eau
        E=PhotoImage(file = "images/eau.gif")
        I=PhotoImage(file = "images/eau_milieu_gauche.gif")
        L=PhotoImage(file = "images/eau_milieu_droite.gif")
        T=PhotoImage(file = "images/eau_haut_milieu.gif")
        G=PhotoImage(file = "images/eau_haut_gauche.gif")
        Q=PhotoImage(file = "images/eau_haut_droite.gif")
        U=PhotoImage(file = "images/eau_bas_milieu.gif")
        C=PhotoImage(file = "images/eau_bas_gauche.gif")
        J=PhotoImage(file = "images/eau_bas_droite.gif")

        # Donjon
        mur1=PhotoImage(file = "images/donjon/mur_haut_gauche.gif")
        mur2=PhotoImage(file = "images/donjon/mur_haut_droite.gif")
        mur3=PhotoImage(file = "images/donjon/mur_bas_droite.gif")
        mur4=PhotoImage(file = "images/donjon/mur_bas_gauche.gif")

        mur11=PhotoImage(file = "images/donjon/mur_haut_3.gif")
        mur12=PhotoImage(file = "images/donjon/mur_haut_6.gif")
        mur21=PhotoImage(file = "images/donjon/mur_droite_3.gif")
        mur22=PhotoImage(file = "images/donjon/mur_droite_6.gif")
        mur31=PhotoImage(file = "images/donjon/mur_bas_3.gif")
        mur32=PhotoImage(file = "images/donjon/mur_bas_6.gif")
        mur41=PhotoImage(file = "images/donjon/mur_gauche_3.gif")
        mur42=PhotoImage(file = "images/donjon/mur_gauche_6.gif")

        porte1=PhotoImage(file = "images/donjon/mur_porte_1.gif")
        porte2=PhotoImage(file = "images/donjon/mur_porte_2.gif")




        # Information sur le perso :
        PERSOG0=PhotoImage(file="images/sprites/perso1.gif")
        PERSOD0=PhotoImage(file="images/sprites/perso8.gif")
        PERSOG1=PhotoImage(file="images/sprites/perso2.gif")
        PERSOD1=PhotoImage(file="images/sprites/perso7.gif")
        PERSOH0=PhotoImage(file="images/sprites/perso5.gif")
        PERSOH1=PhotoImage(file="images/sprites/perso6.gif")
        PERSOB0=PhotoImage(file="images/sprites/perso3.gif")
        PERSOB1=PhotoImage(file="images/sprites/perso4.gif")
        PERSOAD0=PhotoImage(file="images/sprites/persoattaquedroite.gif")
        PERSOAD1=PhotoImage(file="images/sprites/persoattaquedroite.gif")
        PERSOAG0=PhotoImage(file="images/sprites/persoattaquegauche.gif")
        PERSOAG1=PhotoImage(file="images/sprites/persoattaquegauche.gif")
        PERSOAD1=PhotoImage(file="images/sprites/persoattaquedroite.gif")
        PERSOAB0=PhotoImage(file="images/sprites/persoattaquebas.gif")
        PERSOAB1=PhotoImage(file="images/sprites/persoattaquebas.gif")
        PERSOAH0=PhotoImage(file="images/sprites/persoattaquehaut.gif")
        PERSOAH1=PhotoImage(file="images/sprites/persoattaquehaut.gif")
        PERSOM=PhotoImage(file="images/sprites/persomort.gif")


        # Information sur le monstre :
        MONSTREG0=PhotoImage(file="images/sprites/monstre1gauche.gif")
        MONSTREG1=PhotoImage(file="images/sprites/monstre2gauche.gif")
        MONSTRED0=PhotoImage(file="images/sprites/monstre1droite.gif")
        MONSTRED1=PhotoImage(file="images/sprites/monstre2droite.gif")
        MONSTREH0=PhotoImage(file="images/sprites/monstre1haut.gif")
        MONSTREH1=PhotoImage(file="images/sprites/monstre2haut.gif")
        MONSTREB0=PhotoImage(file="images/sprites/monstre1bas.gif")
        MONSTREB1=PhotoImage(file="images/sprites/monstre2bas.gif")

        PNJ0=PhotoImage(file="images/sprites/PNJ1.gif")
        PNJ1=PhotoImage(file="images/sprites/PNJ2.gif")

        ARGOSTE0=PhotoImage(file="images/sprites/argoste0.gif")
        ARGOSTE1=PhotoImage(file="images/sprites/argoste1.gif")



def play():
    winsound.PlaySound("sons/blanc.wav", winsound.SND_ASYNC)
    frame.destroy()



"""___________________________________________________________"""



###########################################
""" Initialisation du programme chroma """
###########################################




num = 1 # numéro du niveau


touches=[]



while True :
    if num == 1 :

        fenetre=Tk()
        fenetre.resizable(width=False, height=False)
        winsound.PlaySound("sons/quest.wav", winsound.SND_ASYNC | winsound.SND_LOOP)


        fenetre.title("chroma")
        fenetre.iconbitmap("@arbre.xbm")
        fenetre.geometry("1280x832+0+0")
        fenetre.lift()

        MENU0=PhotoImage(file="images/menu.gif")
        jack=PhotoImage(file="images/dialogues/bulle_jack.gif")

        # Dessin de l'interface
        boite = Canvas(fenetre,width=1280,height=832, bg="#dedede")
        boite.place(x=0,y=0)


        # Menu
        frame = Canvas(fenetre,width=1280,height=832, bg="#dedede")
        mon_menu = frame.create_image(0, 0, image=MENU0, anchor=NW)
        frame.pack(fill=BOTH, expand= 1)

        play = Button(frame,text="Play",width=10,height=2,font='bold',command=play)
        play.place(x=615,y=700)


        # Jeu
        X0, Y0 = 0, 0 # Positions
        Xj, Yj = -32, -32
        Xmachin, Ymachin = -32, -32
        Xfille, Yfille = -32, -32
        Xmario, Ymario = -32, -32
        Xluigi, Yluigi = -32, -32
        Xbinoclare, Ybinoclare = -32, -32
        Xchelou, Ychelou = -32, -32



        fenetre.bind_all("<KeyPress>",enfoncee)
        fenetre.bind_all("<KeyRelease>",relachee)


        Anim = 0 # Variables d'animation
        AnimM1 = 0
        AnimM2 = 0
        AnimJ = 0

        dialogue=0  # Variable Dialogues
        end=0 # Variable suppression bulle


        t1=0 # Variables Position
        t2=0
        b=0

        # Chargement du tableau

        box = 'boites/boite'+str(num)
        Decors = charge_boite(box)

        textures()
        dessine()

        pnj = boite.create_image(Xj, Yj, image=PNJ1)  #Sprites Perso
        sprite = boite.create_image(Xp, Yp, image=PERSOB1)
        monstre1 = boite.create_image(Xt1, Yt1, image=MONSTREH0, tags='trolln1')
        monstre2 = boite.create_image(Xt2, Yt2, image=MONSTREH0, tags='trolln2')

        animation()  #Animations Perso
        troll1()
        troll2()
        PNJ()


        fenetre.mainloop()




    if num >= 2 :

        fenetre=Tk()
        fenetre.resizable(width=False, height=False)

        fenetre.title("chroma")
        fenetre.iconbitmap("@arbre.xbm")
        fenetre.geometry("1280x832+0+0")
        fenetre.focus_force()



        # Dessin de l'interface
        boite = Canvas(fenetre,width=1280,height=832, bg="#dedede")
        boite.place(x=0,y=0)


        epee=PhotoImage(file="images/dialogues/bulle_epee.gif")
        tatidou=PhotoImage(file="images/dialogues/bulle_tatidou.gif")


        # Jeu
        X0, Y0 = 0, 0 # Positions
        Xj, Yj = -32, -32
        Xmachin, Ymachin = -32, -32
        Xfille, Yfille = -32, -32
        Xmario, Ymario = -32, -32
        Xluigi, Yluigi = -32, -32
        Xbinoclare, Ybinoclare = -32, -32
        Xchelou, Ychelou = -32, -32

        fenetre.bind_all("<KeyPress>",enfoncee)
        fenetre.bind_all("<KeyRelease>",relachee)


        Anim = 0 # Variables d'animation
        AnimM1 = 0
        AnimM2 = 0
        AnimJ = 0

        dialogue=0 # Variable Dialogues
        money=0 # Variable geme
        end=0 # Variable suppression bulle

        t1=0 # Variables Position
        t2=0
        b=0



        # Chargement du tableau

        box = 'boites/boite'+str(num)
        Decors = charge_boite(box)


        textures()
        dessine()

        pnj = boite.create_image(Xj, Yj, image=PNJ1)  #Sprite Perso
        sprite = boite.create_image(Xp, Yp, image=PERSOB1)
        monstre1 = boite.create_image(Xt1, Yt1, image=MONSTREH0, tags='trolln1')
        monstre2 = boite.create_image(Xt2, Yt2, image=MONSTREH0, tags='trolln2')

        animation()  #Animation Perso
        troll1()
        troll2()
        PNJ()


        fenetre.mainloop()





    if num == 15 :

        fenetre=Tk()
        fenetre.resizable(width=False, height=False)

        fenetre.title("chroma")
        fenetre.iconbitmap("@arbre.xbm")
        fenetre.geometry("1280x832+0+0")
        fenetre.focus_force()


        # Dessin de l'interface
        boite = Canvas(fenetre,width=1280,height=832, bg="#dedede")
        boite.place(x=0,y=0)

        tatidou_fin=PhotoImage(file="images/dialogues/bulle_tatidou_fin.gif")
        theargoste=PhotoImage(file="images/dialogues/bulle_argoste.gif")

        # Jeu
        X0, Y0 = 0, 0 # Positions
        Xj, Yj = -32, -32
        Xmachin, Ymachin = -32, -32
        Xfille, Yfille = -32, -32
        Xmario, Ymario = -32, -32
        Xluigi, Yluigi = -32, -32
        Xbinoclare, Ybinoclare = -32, -32
        Xchelou, Ychelou = -32, -32


        fenetre.bind_all("<KeyPress>",enfoncee)
        fenetre.bind_all("<KeyRelease>",relachee)


        Anim = 0 # Variables d'animation
        AnimM1 = 0
        AnimM2 = 0
        AnimJ = 0
        AnimA = 0

        dialogue=0 # Variable Dialogues
        end=0 # Variable suppression bulle

        t1=0 # Variables Position
        t2=0
        b=0


        # Chargement du tableau

        box = 'boites/boite'+str(num)
        Decors = charge_boite(box)


        textures()
        dessine()

        pnj = boite.create_image(Xj, Yj, image=PNJ1)  #Sprites Perso
        sprite = boite.create_image(Xp, Yp, image=PERSOB1)
        monstre1 = boite.create_image(Xt1, Yt1, image=MONSTREH0, tags='trolln1')
        monstre2 = boite.create_image(Xt2, Yt2, image=MONSTREH0, tags='trolln2')
        largoste = boite.create_image(Xa, Ya, image=ARGOSTE0, tags='boss')


        animation()  #Animations Perso
        troll1()
        troll2()
        PNJ()
        argoste()

        fenetre.mainloop()



    if num == 16:

        fenetre=Tk()
        fenetre.resizable(width=False, height=False)

        fenetre.title("chroma")
        fenetre.iconbitmap("@arbre.xbm")
        fenetre.geometry("1280x832+0+0")
        fenetre.focus_force()

        # Dessin de l'interface
        boite = Canvas(fenetre,width=1280,height=832, bg="#bddba8")
        boite.place(x=0,y=0)

        #Jeu
        X0, Y0 = 0, 0 # Positions
        Xj, Yj = -32, -32
        Xmachin, Ymachin = -32, -32
        Xfille, Yfille = -32, -32
        Xmario, Ymario = -32, -32
        Xluigi, Yluigi = -32, -32
        Xbinoclare, Ybinoclare = -32, -32
        Xchelou, Ychelou = -32, -32

        fenetre.bind_all("<KeyPress>",enfoncee)
        fenetre.bind_all("<KeyRelease>",relachee)

        Anim = 0 # Variables d'animation
        AnimJ = 0


        dialogue=0 # Variable Dialogues
        end=0 # Variable suppression bulle

        t1=0 # Variables Position
        t2=0
        b=0


        # Chargement du tableau

        box = 'boites/boite'+str(num)
        Decors = charge_boite(box)


        # Chargement des sprites spéciaux (colorés)
        PERSOG0=PhotoImage(file="images/couleur/perso1.gif")
        PERSOD0=PhotoImage(file="images/couleur/perso8.gif")
        PERSOG1=PhotoImage(file="images/couleur/perso2.gif")
        PERSOD1=PhotoImage(file="images/couleur/perso7.gif")
        PERSOH0=PhotoImage(file="images/couleur/perso5.gif")
        PERSOH1=PhotoImage(file="images/couleur/perso6.gif")
        PERSOB0=PhotoImage(file="images/couleur/perso3.gif")
        PERSOB1=PhotoImage(file="images/couleur/perso4.gif")
        PERSOAD0=PhotoImage(file="images/couleur/persoattaquedroite.gif")
        PERSOAD1=PhotoImage(file="images/couleur/persoattaquedroite.gif")
        PERSOAG0=PhotoImage(file="images/couleur/persoattaquegauche.gif")
        PERSOAG1=PhotoImage(file="images/couleur/persoattaquegauche.gif")
        PERSOAD1=PhotoImage(file="images/couleur/persoattaquedroite.gif")
        PERSOAB0=PhotoImage(file="images/couleur/persoattaquebas.gif")
        PERSOAB1=PhotoImage(file="images/couleur/persoattaquebas.gif")
        PERSOAH0=PhotoImage(file="images/couleur/persoattaquehaut.gif")
        PERSOAH1=PhotoImage(file="images/couleur/persoattaquehaut.gif")


        A=PhotoImage(file = "images/couleur/arbre.gif")
        R=PhotoImage(file = "images/couleur/sol.gif")
        S=PhotoImage(file = "images/couleur/maison1.gif")
        Z=PhotoImage(file = "images/couleur/maison2.gif")
        z=PhotoImage(file = "images/couleur/maison3.gif")

        #Eau(Optionel)
        E=PhotoImage(file = "images/couleur/eau.gif")
        I=PhotoImage(file = "images/couleur/eau_milieu_gauche.gif")
        L=PhotoImage(file = "images/couleur/eau_milieu_droite.gif")
        T=PhotoImage(file = "images/couleur/eau_haut_milieu.gif")
        G=PhotoImage(file = "images/couleur/eau_haut_gauche.gif")
        Q=PhotoImage(file = "images/couleur/eau_haut_droite.gif")
        U=PhotoImage(file = "images/couleur/eau_bas_milieu.gif")
        C=PhotoImage(file = "images/couleur/eau_bas_gauche.gif")
        J=PhotoImage(file = "images/couleur/eau_bas_droite.gif")

        MACHIN0=PhotoImage(file="images/npc/machin1.gif")
        MACHIN1=PhotoImage(file="images/npc/machin2.gif")

        FILLE0=PhotoImage(file="images/npc/fille1.gif")
        FILLE1=PhotoImage(file="images/npc/fille2.gif")

        MARIO0=PhotoImage(file="images/npc/mario1.gif")
        MARIO1=PhotoImage(file="images/npc/mario2.gif")

        LUIGI0=PhotoImage(file="images/npc/luigi1.gif")
        LUIGI1=PhotoImage(file="images/npc/luigi2.gif")

        BINOCLARE0=PhotoImage(file="images/npc/binoclare1.gif")
        BINOCLARE1=PhotoImage(file="images/npc/binoclare2.gif")

        CHELOU0=PhotoImage(file="images/npc/chelou1.gif")
        CHELOU1=PhotoImage(file="images/npc/chelou2.gif")


        dessine()


        #Sprites Perso
        machin = boite.create_image(Xmachin, Ymachin, image=MACHIN1)
        fille = boite.create_image(Xfille, Yfille, image=FILLE1)
        mario = boite.create_image(Xmario, Ymario, image=MARIO1)
        luigi = boite.create_image(Xluigi, Yluigi, image=LUIGI1)
        binoclare = boite.create_image(Xbinoclare, Ybinoclare, image=BINOCLARE1)
        chelou = boite.create_image(Xchelou, Ychelou, image=CHELOU1)

        sprite = boite.create_image(Xp, Yp, image=PERSOB1)


        animation()
        Machin()
        Fille()
        Mario()
        Luigi()
        Binoclare()
        Chelou()


        fenetre.mainloop()
        winsound.PlaySound("sons/blanc.wav", winsound.SND_ASYNC)
        break

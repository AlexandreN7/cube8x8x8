# script carre.py
from tkinter import *

matrice_leds = [[0] * 8 for i in range(2)]

# Taille d'un pixel
pix_size=50

def Clic(event):
    """ Gestion de l'événement Clic gauche sur la zone graphique """

    # position du pointeur de la souris
    for i in range(8) :
    	if i*pix_size<event.x<=(i+1)*pix_size : 
            index = i  	
            X = pix_size*i

    for i in range(2) :    				
    	if i*pix_size<event.y<=(i+1)*pix_size :
            couleur=i
            Y = pix_size*i
            
    matrice_leds[couleur][index]=1

    if Y==0 :
        color = 'red'
    else :
        color = 'blue'

    # on dessine un carré
    cote = pix_size
    Canevas.create_rectangle(X, Y, X+cote, Y+cote, outline='black',fill=color)

def Envoyer():

    print (matrice_leds)


def Effacer():
    """ Efface la zone graphique """
    Canevas.delete(ALL)
    """ RAZ de la matrice """ 
    for i in range(2) :
        for j in range(8) : 
            matrice_leds [i][j]=0

# Création de la fenêtre principale
Mafenetre = Tk()
Mafenetre.title('Carrés')

# Création d'un widget Canvas
Largeur = 8*pix_size
Hauteur = 2*pix_size
Canevas = Canvas(Mafenetre, width = Largeur, height =Hauteur, bg ='white')
# La méthode bind() permet de lier un événement avec une fonction :
# un clic gauche sur la zone graphique provoquera l'appel de la fonction utilisateur Clic()
Canevas.bind('<Button-1>', Clic)
Canevas.pack(padx =5, pady =5)

# Création d'un widget Button (bouton Envoyer)
Button(Mafenetre, text ='Envoyer', fg="purple", command = Envoyer).pack(side=LEFT,padx = 5,pady = 5)

# Création d'un widget Button (bouton Effacer)
Button(Mafenetre, text ='Effacer', command = Effacer).pack(side=LEFT,padx = 5,pady = 5)

# Création d'un widget Button (bouton Quitter)
Button(Mafenetre, text ='Quitter', command = Mafenetre.destroy).pack(side=RIGHT,padx=5,pady=5)

Mafenetre.mainloop()
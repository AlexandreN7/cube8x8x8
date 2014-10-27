"""
script interface_souris_ftdi_PCtoPIC.py
  ______  _____      _           _
 |___   /| ___ \    | |         | |
     / / | |_/ /___ | |__   ___ | |_
    / /  |    // _ \| '_ \ / _ \|  _|
   / /   | |\ \ (_) | |_) | (_) | |_
  /_/    |_| \_\___/|____/ \___/ \__|
                            7robot.fr
Cube8x8x8
                            
Created by Robin Beilvert
"""

from tkinter import *

# Matrice pour envoyer les infos de l'interface graphique au ftdi
matrice_leds = [[0] * 8 for i in range(2)]

# Taille d'un pixel
pix_size=50

def Clic(event):
    """ Gestion de l'événement Clic gauche sur la zone graphique """

    # position du pointeur de la souris
    for i in range(8) :
    	if i*pix_size<event.x<=(i+1)*pix_size : 
            # index pour matrice_leds
            index = i
            # position horizontale du carré              	
            X = pix_size*i

    for i in range(2) :    				
    	if i*pix_size<event.y<=(i+1)*pix_size :
            # couleur pour matrice_leds            
            couleur=i
            # position verticale du carré             
            Y = pix_size*i
            
    matrice_leds[couleur][index]=1

    # couleur du carré en fonction de sa position
    if Y==0 :
        color = 'red'
    else :
        color = 'blue'

    # on dessine le carré
    cote = pix_size
    Canevas.create_rectangle(X, Y, X+cote-1, Y+cote-1, outline=color, fill=color)

def Envoyer():
    # afficher la matrice dans le terminal
    print (matrice_leds)


def Effacer():
    # effacement de la zone graphique
    Canevas.delete(ALL)
    # RAZ de la matrice
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
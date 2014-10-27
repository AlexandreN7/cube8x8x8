#!/usr/bin/python2.6
# -*-coding:Latin-1 -*
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

# Bibliothèques pour ftdi, calculs et gestion du temps
import sys, math
from pylibftdi import Device
from time import sleep

# Bibliothèque pour interface graphique
#from tkinter import *
#from Tkinter import * pour python2.6


try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *


# Matrice pour envoyer les infos de l'interface graphique au ftdi
matrice_leds = [[False] * 8 for i in range(2)]

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
            
    matrice_leds[couleur][index]= not matrice_leds[couleur][index]

    # couleur du carré en fonction de sa position
    if Y==0 :
        color = 'red'
    else :
        color = 'blue'

    # on dessine le carré
    if matrice_leds[couleur][index]==True :
        Canevas.create_rectangle(X, Y, X+pix_size-1, Y+pix_size-1, outline=color, fill=color)
    else :
        Canevas.create_rectangle(X, Y, X+pix_size-1, Y+pix_size-1, outline='white', fill='white')        

def Envoyer():
    # Afficher la matrice dans le terminal
    print (matrice_leds)

    # Formation des octets à envoyer à partir de la matrice
    octet_rouge=0
    octet_bleu=0

    for i in range(8) :
        octet_rouge = octet_rouge+matrice_leds[0][i]*(2**i) 
    for i in range(8) :
        octet_bleu = octet_bleu+matrice_leds[1][i]*(2**i)

    print ("Octet rouge = %s" % bin(octet_rouge))
    print ("Octet bleu = %s" % bin(octet_bleu))

    # On envoie la sauce !
    with Device (mode = 't') as dev:
        dev.baudrate = 19200

        i=0
        while i<64 :
            dev.write(chr(octet_bleu))
            dev.write(chr(octet_rouge))                                
            i=i+1



def Effacer():
    # effacement de la zone graphique
    Canevas.delete(ALL)
    # RAZ de la matrice
    for i in range(2) :
        for j in range(8) : 
            matrice_leds [i][j]=False

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

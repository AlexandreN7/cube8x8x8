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

Created by Robin Beilvert and Alexandre Proux
"""

# Bibliothèques pour ftdi, calculs et gestion du temps
import sys, math
from pylibftdi import Device
from time import sleep

# Bibliothèque pour interface graphique
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

# Une ligne correspond à un PIC
lignes = 8
# Une colonne correspond à une diode pour un PIC
colonnes = 8

# Matrice pour envoyer les infos de l'interface graphique au ftdi
matrice_leds = []
for i in range(lignes):
    matrice_leds.append([0] * colonnes)


# Taille d'un pixel du GUI
pix_size=50


def Clic(event):
    """ Gestion de l'événement Clic gauche sur la zone graphique """

    # Incrémentation de la matrice en fonction de la position du pointeur de la souris
    for i in range(8) : 
    	for j in range(8) :    				
		    if (i*pix_size<event.x<=(i+1)*pix_size) and (j*pix_size<event.y<=(j+1)*pix_size) :
		        matrice_leds[j][i] = matrice_leds[j][i]+1 

    # Dessin du carré en fonction de la position et du nombre de clics (couleur)
    for i in range(8) :
    		for j in range(8) :    	

		    	if  matrice_leds[i][j]%4 == 1:
		    		Canevas.create_rectangle(j*pix_size, i*pix_size, j*pix_size+pix_size-1,  i*pix_size+pix_size-1, outline='red', fill='red')
		    	elif matrice_leds[i][j]%4 == 2:
		    		Canevas.create_rectangle(j*pix_size, i*pix_size, j*pix_size+pix_size-1,  i*pix_size+pix_size-1, outline='blue', fill='blue')
		    	elif matrice_leds[i][j]%4 == 3:
		    		Canevas.create_rectangle(j*pix_size, i*pix_size, j*pix_size+pix_size-1,  i*pix_size+pix_size-1, outline='purple', fill='purple')
		    	else :
		    		Canevas.create_rectangle(j*pix_size, i*pix_size, j*pix_size+pix_size-1,  i*pix_size+pix_size-1, outline='white', fill='white')

def Envoyer():
    # Formation des octets à envoyer à partir de la matrice
    # Les 8 indices des octets correspondent aux 8 PICs
    octets_rouges=[0,0,0,0,0,0,0,0]
    octets_bleus=[0,0,0,0,0,0,0,0]

    # Indice pour chaque PIC
    for i in range(8) :
        # Indice pour chaque diode d'une ligne (= d'un PIC)
        for j in range(8) :

            if  matrice_leds[i][j]%4 == 1:
                octets_rouges[i] = octets_rouges[i]+2**j

            elif matrice_leds[i][j]%4 == 2:                
                octets_bleus[i] = octets_bleus[i]+2**j

            elif matrice_leds[i][j]%4 == 3:
                octets_rouges[i] = octets_rouges[i]+2**j
                octets_bleus[i] = octets_bleus[i]+2**j

    print ("On verifie les octets envoyes aux deux premiers PICs :")
    print ("Premier octet rouge = %s" % bin(octets_rouges[0]))
    print ("Premier octet bleu = %s" % bin(octets_bleus[0]))
    print ("Second octet rouge = %s" % bin(octets_rouges[1]))
    print ("Second octet bleu = %s" % bin(octets_bleus[1]))

    # On envoie la sauce !
    with Device (mode = 't') as dev:
        dev.baudrate = 19200

        # 8 étages
        for k in range(8) :
            # 8 PICs = 8 lignes bicolores
            for i in range (8) :
                dev.write(chr(octets_bleus[i]))
                dev.write(chr(octets_rouges[i]))



def Effacer():
    # Effacement de la zone graphique
    Canevas.delete(ALL)
    # RAZ de la matrice
    for i in range(8) :
        for j in range(8) : 
            matrice_leds [i][j]=0

# Création de la fenêtre principale
Mafenetre = Tk()
Mafenetre.title('Carrés')

# Création d'un widget Canvas
Largeur = colonnes*pix_size
Hauteur = lignes*pix_size
Canevas = Canvas(Mafenetre, width = Largeur, height =Hauteur, bg ='white')
# La méthode bind() permet de lier un événement avec une fonction :
# un clic gauche sur la zone graphique provoquera l'appel de la fonction utilisateur Clic()
Canevas.bind('<Button-1>', Clic)
Canevas.pack(padx = 5, pady = 5)

# Création d'un widget Button (bouton Envoyer)
Button(Mafenetre, text ='Envoyer', fg="purple", command = Envoyer).pack(side=LEFT, padx = 5, pady = 5)

# Création d'un widget Button (bouton Effacer)
Button(Mafenetre, text ='Effacer', command = Effacer).pack(side=LEFT, padx = 5, pady = 5)

# Création d'un widget Button (bouton Quitter)
Button(Mafenetre, text ='Quitter', command = Mafenetre.destroy).pack(side=RIGHT, padx = 5, pady = 5)

Mafenetre.mainloop()

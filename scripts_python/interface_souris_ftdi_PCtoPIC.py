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

def Change_couleur(i,j):
	# Incrémentation de la matrice				
	matrice_leds[i][j] = matrice_leds[i][j]+1 
	# Changement de couleur du carré  	
	if  matrice_leds[i][j]%4 == 1 :
		Canevas.itemconfigure(carre[i][j],fill='red')
	elif matrice_leds[i][j]%4 == 2 :
		Canevas.itemconfigure(carre[i][j],fill='blue')
	elif matrice_leds[i][j]%4 == 3 :
		Canevas.itemconfigure(carre[i][j],fill='purple')
	else :
		Canevas.itemconfigure(carre[i][j],fill='white')


def Clic(event):
	""" Gestion de l'événement Clic gauche sur la zone graphique """
	for i in range(lignes):
		for j in range (colonnes):
			if (j*pix_size<event.x<=(j+1)*pix_size) and (i*pix_size<event.y<=(i+1)*pix_size) :
				Change_couleur(i,j) 	


def Touche(event):

	print (section.get())
	# Gestion de l'événement Appui sur une touche du clavier
	touche = event.keysym
	touche_list=['ampersand','eacute','quotedbl','apostrophe',\
			     'a','z','e','r',\
			     'q','s','d','f',\
			     'w','x','c','v']     
	for index in range (16):
		if touche == touche_list[index]:
			Change_couleur(index//4+4*(section.get()//2),index%4+4*(section.get()%2)) 
		

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

		
def Init():
	# Effacement de la zone graphique
	Canevas.delete(ALL)
	global carre
	carre = []
	for i in range(lignes):
		carre.append(\
		[Canevas.create_rectangle(0*pix_size, i*pix_size, 0*pix_size+pix_size-1,  i*pix_size+pix_size-1, outline='white', fill='white')]+\
		[Canevas.create_rectangle(1*pix_size, i*pix_size, 1*pix_size+pix_size-1,  i*pix_size+pix_size-1, outline='white', fill='white')]+\
		[Canevas.create_rectangle(2*pix_size, i*pix_size, 2*pix_size+pix_size-1,  i*pix_size+pix_size-1, outline='white', fill='white')]+\
		[Canevas.create_rectangle(3*pix_size, i*pix_size, 3*pix_size+pix_size-1,  i*pix_size+pix_size-1, outline='white', fill='white')]+\
		[Canevas.create_rectangle(4*pix_size, i*pix_size, 4*pix_size+pix_size-1,  i*pix_size+pix_size-1, outline='white', fill='white')]+\
		[Canevas.create_rectangle(5*pix_size, i*pix_size, 5*pix_size+pix_size-1,  i*pix_size+pix_size-1, outline='white', fill='white')]+\
		[Canevas.create_rectangle(6*pix_size, i*pix_size, 6*pix_size+pix_size-1,  i*pix_size+pix_size-1, outline='white', fill='white')]+\
		[Canevas.create_rectangle(7*pix_size, i*pix_size, 7*pix_size+pix_size-1,  i*pix_size+pix_size-1, outline='white', fill='white')])
	
	# RAZ de la matrice
	for i in range(lignes) :
		for j in range(colonnes) : 
			matrice_leds [i][j]=0

# Création de la fenêtre principale
Mafenetre = Tk()
Mafenetre.title('Carrés')

# un appui sur une touche du clavier provoquera l'appel de la fonction utilisateur Touche()
Mafenetre.bind('<Key>', Touche)

# Création d'un widget Canvas
Largeur = colonnes*pix_size
Hauteur = lignes*pix_size
Canevas = Canvas(Mafenetre, width = Largeur, height =Hauteur, bg ='white')
# La méthode bind() permet de lier un événement avec une fonction :
# un clic gauche sur la zone graphique provoquera l'appel de la fonction utilisateur Clic()
Canevas.bind('<Button-1>', Clic)

Canevas.pack(padx = 5, pady = 5)

Init()

Boutons = Canvas(Mafenetre, width = 100, height =100)
section=IntVar()
section.set(0)
bouton1=Radiobutton(Boutons, text="Haut gauche", variable=section, value=0, indicatoron=0, height=3, width=15)
bouton2=Radiobutton(Boutons, text="Haut droite", variable=section, value=1, indicatoron=0, height=3, width=15)
bouton3=Radiobutton(Boutons, text="Bas gauche", variable=section, value=2, indicatoron=0, height=3, width=15)
bouton4=Radiobutton(Boutons, text="Bas droite", variable=section, value=3, indicatoron=0, height=3, width=15)
bouton1.grid(row=0, column=0)
bouton2.grid(row=0, column=1)
bouton3.grid(row=1, column=0)
bouton4.grid(row=1, column=1)

Boutons.pack(padx = 5, pady = 5)

# Création d'un widget Button (bouton Envoyer)
Button(Mafenetre, text ='Envoyer', fg="purple", command = Envoyer).pack(side=LEFT, padx = 5, pady = 5)

# Création d'un widget Button (bouton Effacer)
Button(Mafenetre, text ='Effacer', command = Init).pack(side=LEFT, padx = 5, pady = 5)

# Création d'un widget Button (bouton Quitter)
Button(Mafenetre, text ='Quitter', command = Mafenetre.destroy).pack(side=RIGHT, padx = 5, pady = 5)

Mafenetre.mainloop()

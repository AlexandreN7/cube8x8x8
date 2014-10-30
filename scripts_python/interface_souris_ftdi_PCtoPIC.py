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

logs = open("logs_8x8x8.txt", "w")

# Une ligne correspond à un PIC
lignes = 8
# Une colonne correspond à une diode pour un PIC donné
colonnes = 8
# 8 étages
etages = 8

# Etage affiché dans le canevas principal
Etage_courant = 0

# Matrice pour envoyer les infos de l'interface graphique au ftdi
matrice_leds = []
for i in range(lignes):
	matrice_leds.append([0] * colonnes)


# Taille d'un pixel du canevas principal
pix_size=50


def Change_couleur(i,j):

	canv=Canevas
	# Incrémentation de la matrice				
	matrice_leds[i][j] = matrice_leds[i][j]+1 
	# Changement de couleur du carré  	
	if  matrice_leds[i][j]%4 == 1 :
		canv.itemconfigure(carre[i][j],fill='red')
	elif matrice_leds[i][j]%4 == 2 :
		canv.itemconfigure(carre[i][j],fill='blue')
	elif matrice_leds[i][j]%4 == 3 :
		canv.itemconfigure(carre[i][j],fill='purple')
	else :
		canv.itemconfigure(carre[i][j],fill='white')

	global octets_rouges
	global octets_bleus
	octets_rouges=[0,0,0,0,0,0,0,0]				
	octets_bleus=[0,0,0,0,0,0,0,0]

	# Indice pour chaque PIC
	for i in range(lignes) :
		# Indice pour chaque diode d'une ligne (= d'un PIC)
		for j in range(colonnes) :

			if  matrice_leds[i][j]%4 == 1:
				octets_rouges[i] = octets_rouges[i]+2**j

			elif matrice_leds[i][j]%4 == 2:                
				octets_bleus[i] = octets_bleus[i]+2**j

			elif matrice_leds[i][j]%4 == 3:
				octets_rouges[i] = octets_rouges[i]+2**j
				octets_bleus[i] = octets_bleus[i]+2**j


def Clic(event):
	""" Gestion de l'événement Clic gauche sur la zone graphique """
	for i in range(lignes):
		for j in range (colonnes):
			if (j*pix_size<event.x<=(j+1)*pix_size) and (i*pix_size<event.y<=(i+1)*pix_size) :
				Change_couleur(i,j) 	


def Touche(event):
	# Gestion de l'événement Appui sur une touche du clavier
	touche = event.keysym
	#print(touche)
	# Touches sensibles pour les pixels
	sensPix_list=['ampersand','eacute','quotedbl','apostrophe','parenleft','minus','egrave','underscore',\
				 'a','z','e','r','t','y','u','i',\
				 'q','s','d','f','g','h','j','k',\
				 'w','x','c','v','b','n','comma','semicolon'] 
	# Touches sensibles changement d'étage
	sensEtage_list=['Left','Right']

	for index in range (len(sensPix_list)):
		if touche == sensPix_list[index]:
			Change_couleur(index//8+4*section.get(),index%8) 

	for index in range (len(sensEtage_list)):
		if touche == sensEtage_list[index]:
			ChangeEtage(index)

def Envoyer():

	print ("On verifie les octets envoyes aux deux premiers PICs :")
	print ("Premier octet rouge = %s" % bin(octets_rouges[0]))
	print ("Premier octet bleu = %s" % bin(octets_bleus[0]))
	print ("Second octet rouge = %s" % bin(octets_rouges[1]))
	print ("Second octet bleu = %s" % bin(octets_bleus[1]))

	# On envoie la sauce !
	with Device (mode = 't') as dev:
		dev.baudrate = 19200	

		# 8 étages
		for k in range(etages) :
			# 8 PICs = 8 lignes bicolores
			for i in range (lignes) :
				dev.write(chr(octets_bleus[i]))
				dev.write(chr(octets_rouges[i]))

		
def Init():
	# Effacement de la zone graphique
	Canevas.delete(ALL)
	global carre
	carre = []
	# Initialisation des carrés ligne par ligne
	for i in range(lignes):
		# On créé une ligne
		sommelist=[]
		for j in range (8):
			sommelist=sommelist+\
			[Canevas.create_rectangle(j*pix_size, i*pix_size, j*pix_size+pix_size-1,  i*pix_size+pix_size-1, outline='white', fill='white')]
		# On ajoute la ligne	
		carre.append(sommelist)
	
	# RAZ de la matrice
	for i in range(lignes) :
		for j in range(colonnes) : 
			matrice_leds [i][j]=0
	
def ChangeEtage(event):

	# Touche est pour un évenement au clavier, event.widget gère les interventions à la souris
	touche = event.keysym
	if touche=='Left' or event.widget==Fleche_gauche :

		#if Etage_courant != 0 :
			print ('pouet a gauche')
			#Etage_courant = Etage_courant-1

	else:
		#if Etage_courant != 7 :
			print ('pouet a droite')
			#Etage_courant = Etage_courant+1


def Save():
	# Sauvegarde des logs
	logs.write('Envoi \n')
	for k in range(etages) :		
		for i in range (lignes) :
			logs.write("(%s,%s) " %(octets_bleus[i],octets_rouges[i]))
		logs.write('\n')


# Création de la fenêtre principale
Mafenetre = Tk()
Mafenetre.title('Carrés')


# La méthode bind() permet de lier un événement avec une fonction :
# un appui sur une touche du clavier provoquera l'appel de la fonction utilisateur Touche()
Mafenetre.bind('<Key>', Touche)

Mafenetre.bind('<Left>', ChangeEtage)
Mafenetre.bind('<Right>', ChangeEtage)

Boutons = Canvas(Mafenetre, width = 100, height =100)


# Création d'un widget Canvas (matrice colorée)
Hauteur = lignes*pix_size
Largeur = colonnes*pix_size
Canevas = Canvas(Mafenetre, width = Largeur, height =Hauteur, bg ='white')

# La méthode bind() permet de lier un événement avec une fonction :
# un clic gauche sur la zone graphique provoquera l'appel de la fonction utilisateur Clic()
Canevas.bind('<Button-1>', Clic)

Etages = Canvas(Mafenetre)

Fleche_gauche = Canvas(Etages, width=48, height=48)
Fleche_gauche.grid(row=0, column=0)
photo_flechegauche = PhotoImage(file="fleche_gauche.png")
Fleche_gauche.create_image(0, 0, image=photo_flechegauche, anchor=NW)

etage=[]
for i in range(etages):
	etage.append(Canvas(Etages, width = 48, height = 48, bg ='white'))
	etage[i].grid(row=0, column=i+1)

Fleche_droite = Canvas(Etages, width=48, height=48)
Fleche_droite.grid(row=0, column=etages+1)
photo_flechedroite = PhotoImage(file="fleche_droite.png")
Fleche_droite.create_image(0, 0, image=photo_flechedroite, anchor=NW)

Etages.pack(padx = 5, pady = 5)

Canevas.pack(padx = 5, pady = 5)

Fleche_gauche.bind('<Button-1>', ChangeEtage)
Fleche_droite.bind('<Button-1>', ChangeEtage)

# On remplit le canevas principal de carrés blancs
Init()

# Boutons de sélection de la zone concernée par les entrées au clavier
# et image du clavier
Boutons = Canvas(Mafenetre, width = 100, height =100)

ImgClavier = Canvas(Boutons, width=329, height=146)
ImgClavier.grid(column=0, rowspan=2)
photo = PhotoImage(file="clavier.png")
ImgClavier.create_image(0, 0, image=photo, anchor=NW)

section=IntVar()
section.set(0)
bouton1=Radiobutton(Boutons, text="En haut", variable=section, value=0, indicatoron=0, height=3, width=15)
bouton2=Radiobutton(Boutons, text="En bas", variable=section, value=1, indicatoron=0, height=3, width=15)
bouton1.grid(row=0, column=1)
bouton2.grid(row=1, column=1)

Boutons.pack(side=TOP, padx = 10, pady = 5) 

# Bouton Envoyer
Button(Mafenetre, text ='Envoyer', fg="purple", command = Envoyer).pack(side=LEFT, padx = 5, pady = 5)

# Bouton Effacer
Button(Mafenetre, text ='Effacer', command = Init).pack(side=LEFT, padx = 5, pady = 5)

# Bouton Save
Button(Mafenetre, text ='Save', command = Save).pack(side=LEFT, padx = 5, pady = 5)

# Bouton Quitter
Button(Mafenetre, text ='Quitter', command = Mafenetre.destroy).pack(side=RIGHT, padx = 5, pady = 5)

Mafenetre.mainloop()

logs.close()
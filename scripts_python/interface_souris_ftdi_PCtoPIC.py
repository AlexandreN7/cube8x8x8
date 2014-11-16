#!/usr/bin/env python # -*- coding: utf8 -*-

"""
script interface_souris_ftdi_PCtoPIC.py
 ______  _____      _           _
|___   || ___ \    | |         | |
	/ / | |_/ /___ | |__   ___ | |_
   / /  |    // _ \|  _ \ / _ \|  _|
  / /   | |\ \ (_) | |_) | (_) | |_
 /_/    |_| \_\___/|____/ \___/ \__|
						7robot.fr

Cube8x8x8

Created by Robin Beilvert, 3 lines written by Alexandre Proux and Felix is watching
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

# Gestionnaire de threads
from threading import Thread

import os

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
for i in range(lignes*etages):
	matrice_leds.append([0] * colonnes)


# Taille d'un pixel des étages
etage_pix_size=6

# Taille d'un pixel du canevas principal
pix_size=50

# Variable logique d'envoi des trames (en cours ou pas)
envoiState=FALSE;

###################################### Thread d'envoi de trame ######################################

class Envoi_Trame(Thread):
	''' Envoi des trames dans un thread séparé. '''
	def __init__(self):
		Thread.__init__(self)
		self._arret = False

	def run(self):

		numPattern=0

		while not self._arret:	
			filename = liste_trame.get(2*numPattern)
			print(filename)
			logs = open("Patterns//%s.txt" %filename,"r")
			for k in range(etages):	
				for i in range(lignes):
					for j in range(colonnes):
						for couleur_pixel in range(5):
							# L'appel à logs.read(1) fait avancer la lecture d'un caractère :
							# On se remet à la bonne position avec logs.seek()
							logs.seek(8*i+j+64*k,0)
							if logs.read(1) == "%s" %couleur_pixel :
								matrice_leds[i+8*k][j]=couleur_pixel
			
			numPattern+=1
			if numPattern==liste_trame.size()//2:
				numPattern=0


			Envoyer()

			# On attend le bon délai entre deux patterns
			delaistring=liste_trame.get(2*(numPattern//2)+1)
			sleep(int(delaistring[1:len(delaistring)-4])/1000)

		print ("Terminé !")

	def stop(self):
		self._arret = True

#####################################################################################################

def Envoyer_Trame():

	if 	liste_trame.size()!=0 :
		global envoiState
		envoiState=~envoiState

		if(envoiState):
			Bouton_EnvoiTrames.config(text="Arrêter\nl'envoi",fg='brown')
			global envoiTrame
			envoiTrame = Envoi_Trame()
			envoiTrame.start()  # On démarre l'envoi
		else:
			Bouton_EnvoiTrames.config(text='Envoyer\nla trame !',fg='purple')
			envoiTrame.stop() 	# On arrête l'envoi
	else :
		print('Trame vide...')


def Change_couleur(i,j):

	# Incrémentation de la matrice				
	matrice_leds[i+8*Etage_courant][j] = (matrice_leds[i+8*Etage_courant][j]+1)%4

	# Changement de couleur des carrés
	if  matrice_leds[i+8*Etage_courant][j] == 1 :

		Canevas.itemconfigure(carre[i][j],fill='red')
		Etages.itemconfigure(carres_etages[i+8*Etage_courant][j],fill='red')

	elif matrice_leds[i+8*Etage_courant][j] == 2 :

		Canevas.itemconfigure(carre[i][j],fill='blue')
		Etages.itemconfigure(carres_etages[i+8*Etage_courant][j],fill='blue')

	elif matrice_leds[i+8*Etage_courant][j] == 3 :

		Canevas.itemconfigure(carre[i][j],fill='purple')
		Etages.itemconfigure(carres_etages[i+8*Etage_courant][j],fill='purple')

	else :
		Canevas.itemconfigure(carre[i][j],fill='white')
		Etages.itemconfigure(carres_etages[i+8*Etage_courant][j],fill='white')


def Clic(event):
	""" Gestion de l'événement Clic gauche sur la zone graphique """
	for i in range(lignes):
		for j in range (colonnes):
			if (j*pix_size<event.x<=(j+1)*pix_size) and (i*pix_size<event.y<=(i+1)*pix_size) :
				Change_couleur(i,j) 	


def Touche(event):
	# Gestion de l'événement Appui sur une touche du clavier
	touche = event.keysym
	#print(liste_trame.size())

	if touche=='Escape':
		Mafenetre.destroy()

	if touche=='asterisk':
		Init()

	if touche=='parenright':
		Open()

	if touche=='equal':
		Save_Popup()				

	if touche=='Return':
		Envoyer()

	if touche=='Up':
		section.set(0)
	if touche=='Down':
		section.set(1)		

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
	octets_rouges=[]				
	octets_bleus=[]
	for k in range(etages):
		octets_rouges.append([0] * lignes)
		octets_bleus.append([0] * lignes)		

	for k in range(etages):	
		# Indice pour chaque PIC
		for i in range(lignes) :
			# Indice pour chaque diode d'une ligne (= d'un PIC)
			for j in range(colonnes) :

				if  matrice_leds[i+8*k][j] == 1:
					octets_rouges[k][i] = octets_rouges[k][i]+2**j

				elif matrice_leds[i+8*k][j] == 2:                
					octets_bleus[k][i] = octets_bleus[k][i]+2**j

				elif matrice_leds[i+8*k][j] == 3:
					octets_rouges[k][i] = octets_rouges[k][i]+2**j
					octets_bleus[k][i] = octets_bleus[k][i]+2**j


	#print ("On verifie les octets envoyés aux PICs :")
	#print ("Premier octet bleu = %s" % bin(octets_bleus[0][0]))	
	#print ("Premier octet rouge = %s" % bin(octets_rouges[0][0]))
	#print ("Second octet bleu = %s" % bin(octets_bleus[0][1]))	
	#print ("Second octet rouge = %s" % bin(octets_rouges[0][1]))

	try:
		# On envoie la sauce !
		with Device (mode = 't') as dev:
			dev.baudrate = 115200

			# 8 étages
			for k in range(etages) :
				# 8 PICs = 8 lignes bicolores
				for i in range (lignes) :
					dev.write(chr(octets_bleus[k][i]))
					dev.write(chr(octets_rouges[k][i]))
	except Exception:	
		#if envoiState:
		#	Envoyer_Trame()
		print('FTDI non détecté')
	


def Init():

	##################################### Initialisation des étages #####################################

	# Contours des étages		
	Etages.delete(ALL)
	global etage
	etage=[]
	for i in range(etages):
		etage=etage+[Etages.create_rectangle(48*i+3*(i+1), 2, 48*(i+1)+3*(i+1), 50, width=2 ,outline='grey')]
	Etages.itemconfigure(etage[Etage_courant], outline='yellow')	

	# Contenu des étages
	global carres_etages
	carres_etages = []
	# Initialisation des carrés étage par étage et ligne par ligne
	for i in range(lignes*etages):
		# On créé une ligne
		sommelist=[]
		for j in range (8):
			sommelist=sommelist+\
			[Etages.create_rectangle(j*etage_pix_size+3+51*(i//8), (i%8)*etage_pix_size+2,\
			j*etage_pix_size+etage_pix_size+2+51*(i//8), (i%8)*etage_pix_size+etage_pix_size+1,\
			outline='white', fill='white')]
		# On ajoute la ligne	
		carres_etages.append(sommelist)

	#####################################################################################################


	################################ Initialisation du canevas principal ################################

	Canevas.delete(ALL)
	global carre
	carre = []
	# Initialisation des carrés ligne par ligne
	for i in range(lignes):
		# On créé une ligne
		sommelist=[]
		for j in range (8):
			sommelist=sommelist+\
			[Canevas.create_rectangle(j*pix_size+2, i*pix_size+2, j*pix_size+pix_size+1,  i*pix_size+pix_size+1,\
			 outline='white', fill='white')]
		# On ajoute la ligne	
		carre.append(sommelist)

	# RAZ de la matrice
	for k in range(etages) :
		for i in range(lignes) :
			for j in range(colonnes) : 
				matrice_leds [i+8*k][j]=0

	####################################################################################################


def ChangeEtage(event):

	global Etage_courant
	# Touche est pour un évenement au clavier, event.widget gère les interventions à la souris
	touche = event.keysym
	
	Etages.itemconfigure(etage[Etage_courant], outline='grey')

	if touche=='Left' or event.widget==Fleche_gauche :
		if Etage_courant != 0 :
			Etage_courant = Etage_courant-1
	else:
		if Etage_courant != 7 :
			Etage_courant = Etage_courant+1

	Etages.itemconfigure(etage[Etage_courant], outline='yellow')

	MAJ_Couleurs(0)


def MAJ_Couleurs(petitscarres):
	if petitscarres == 1 :
		for k in range(etages) :
			for i in range (lignes):
				for j in range(etages):
					if  matrice_leds[i+8*k][j] == 1 :
						Etages.itemconfigure(carres_etages[i+8*k][j],fill='red')
					elif matrice_leds[i+8*k][j] == 2 :					
						Etages.itemconfigure(carres_etages[i+8*k][j],fill='blue')
					elif matrice_leds[i+8*k][j] == 3 :
						Etages.itemconfigure(carres_etages[i+8*k][j],fill='purple')
					else :
						Etages.itemconfigure(carres_etages[i+8*k][j],fill='white')
	else :
		for i in range (lignes):
			for j in range(etages):
				if  matrice_leds[i+8*Etage_courant][j] == 1 :
					Canevas.itemconfigure(carre[i][j],fill='red')
				elif matrice_leds[i+8*Etage_courant][j] == 2 :
					Canevas.itemconfigure(carre[i][j],fill='blue')
				elif matrice_leds[i+8*Etage_courant][j] == 3 :
					Canevas.itemconfigure(carre[i][j],fill='purple')
				else :
					Canevas.itemconfigure(carre[i][j],fill='white')


def Open():

	if liste_save.curselection() != ():
		filename = liste_save.get(liste_save.curselection())
		logs = open("Patterns//%s.txt" %filename,"r")
		for k in range(etages):	
			for i in range(lignes):
				for j in range(colonnes):
					for couleur_pixel in range(5):
						# L'appel à logs.read(1) fait avancer la lecture d'un caractère :
						# On se remet à la bonne position avec logs.seek()
						logs.seek(8*i+j+64*k,0)
						if logs.read(1) == "%s" %couleur_pixel :
							matrice_leds[i+8*k][j]=couleur_pixel


		logs.close()
		MAJ_Couleurs(0)
		MAJ_Couleurs(1)

def Actualiser_patterns():
	# Actualisation de la liste des patterns enregistrés
	liste_save.delete(0, END)		
	savedPatterns = os.listdir('Patterns')
	for i in range(len(savedPatterns)):
		liste_save.insert(END, "%s" %(savedPatterns[i][:len(savedPatterns[i])-4]))

def Save_Popup():

	def Save(event):
		if savefield.get() == '':
			# Nom de sauvegarde par défaut
			savename='default'
		else :
			savename=savefield.get()

		logs = open("Patterns//%s.txt" %savename,"w")
		for k in range(etages):	
			for i in range(lignes):
				for j in range(colonnes):
					logs.write("%s" %matrice_leds[i+8*k][j])
		logs.close()

		Actualiser_patterns()

		Save_Screen.destroy()

	# Création de la fenêtre de sauvegarde
	Save_Screen = Tk()
	Save_Screen.title('Save')	

	BlablaSave = Label(Save_Screen, text="Nom du pattern (default par defaut):").grid()
	
	global savefield
	savefield= Entry(Save_Screen)
	savefield.focus_force()
	savefield.grid()

	# Bouton Save
	saveBouton=Button(Save_Screen, text ='Save')
	saveBouton.bind("<Button-1>", Save)
	Save_Screen.bind("<Return>", Save)
	saveBouton.grid()

def Supprimer_Pattern():
	print("%s" %delai_field.get())
	os.remove("Patterns//%s.txt" %liste_save.get(liste_save.curselection()))
	Actualiser_patterns()

def Ajouter_Pattern():
	if liste_save.curselection() != ():
		liste_trame.insert(END, liste_save.get(liste_save.curselection()))

		if delai_field.get()=='' or int(delai_field.get()) in range(26):
			liste_trame.insert(END, "(25 ms)")
		elif int(delai_field.get()) in range(10000):	
			liste_trame.insert(END, "(%s ms)" %delai_field.get())
		else:
			liste_trame.insert(END, "(10000 ms)")	

		
def Enlever_Pattern():
	if liste_trame.curselection() != ():
		n=liste_trame.curselection()[0]
		liste_trame.delete(2*(n//2),2*(n//2)+1)

def Modif_Delai():
	if liste_trame.curselection() != ():
		n=liste_trame.curselection()[0]
		liste_trame.delete(2*(n//2)+1)
		liste_trame.insert(2*(n//2)+1, "(%s ms)" %delai_field.get())		


#####################################################################################################
#####################################################################################################
#####################################################################################################
#####################################################################################################



# Création de la fenêtre principale
Mafenetre = Tk()
Mafenetre.title('Interface Cube8x8x8')

# La méthode bind() permet de lier un événement avec une fonction :
# un appui sur une touche du clavier provoquera l'appel de la fonction utilisateur Touche()
Mafenetre.bind('<Key>', Touche)

Mafenetre.bind('<Left>', ChangeEtage)
Mafenetre.bind('<Right>', ChangeEtage)

Boutons = Canvas(Mafenetre, width = 100, height =100)




#####################################################################################################
######################## Création de la ligne avec les étages et les flèches ########################
#####################################################################################################
Etages = Canvas(Mafenetre, width = 8*51, height=50)

Fleche_gauche = Canvas(Mafenetre, width=48, height=48)
Fleche_gauche.grid(row=0, column=0)
photo_flechegauche = PhotoImage(file="fleche_gauche.png")
Fleche_gauche.create_image(0, 0, image=photo_flechegauche, anchor=NW)


Fleche_droite = Canvas(Mafenetre, width=48, height=48)
Fleche_droite.grid(row=0, column=6)
photo_flechedroite = PhotoImage(file="fleche_droite.png")
Fleche_droite.create_image(0, 0, image=photo_flechedroite, anchor=NW)

Etages.grid(row=0, column=1, columnspan=5, pady=5)
#####################################################################################################

# On lie les flèches du clavier aux flèches de sélection des étages
Fleche_gauche.bind('<Button-1>', ChangeEtage)
Fleche_droite.bind('<Button-1>', ChangeEtage)

#####################################################################################################
######################### Création du canevas principal (matrice colorée) ###########################
#####################################################################################################
Hauteur = lignes*pix_size
Largeur = colonnes*pix_size
Canevas = Canvas(Mafenetre, width = Largeur+2, height =Hauteur+2)

# La méthode bind() permet de lier un événement avec une fonction :
# un clic gauche sur la zone graphique provoquera l'appel de la fonction utilisateur Clic()
Canevas.bind('<Button-1>', Clic)
# On affiche le canevas principal
Canevas.grid(row=1, column=1, columnspan=5)
#####################################################################################################


#####################################################################################################
###### Boutons de sélection de la zone concernée par les entrées au clavier et image du clavier #####
#####################################################################################################
Boutons = Canvas(Mafenetre, width = 100, height =100, highlightthickness=0)

ImgClavier = Canvas(Boutons, width=329, height=146)
ImgClavier.grid(column=0, rowspan=2)
photo = PhotoImage(file="clavier.png")
ImgClavier.create_image(0, 0, image=photo, anchor=NW)

section=IntVar()
section.set(0)
bouton1=Radiobutton(Boutons, text="En haut", variable=section, value=0, indicatoron=0, height=4, width=11)
bouton2=Radiobutton(Boutons, text="En bas", variable=section, value=1, indicatoron=0, height=4, width=11)
bouton1.grid(row=0, column=1)
bouton2.grid(row=1, column=1)

Boutons.grid(row=2, column=1, columnspan=5, pady=5) 
#####################################################################################################


#####################################################################################################
################################## Gestion des trames de patterns ###################################
#####################################################################################################
Gestion_Trames = Canvas(Mafenetre, highlightthickness=0)
Gestion_Trames.grid(row=0, column=7, rowspan=3, padx=10)


Button(Gestion_Trames, text ='Supprimer pattern \n /!\\ Suppression définitive /!\\', fg="red",\
							width=21, command = Supprimer_Pattern).grid(row=0, column=0, columnspan=2, pady=5)
Label(Gestion_Trames, text="Patterns disponibles :").grid(row=1, column=0, columnspan=2)
liste_save = Listbox(Gestion_Trames, width=24, height=5)
liste_save.grid(row=2, column=0, columnspan=2, rowspan=2)
Actualiser_patterns()

Fleche_haut = Canvas(Gestion_Trames, width=24, height=24)
Fleche_haut.grid(row=2, column=2)
photo_flechehaut = PhotoImage(file="fleche_haut.png")
Fleche_haut.create_image(0, 0, image=photo_flechehaut, anchor=NW)

Fleche_bas = Canvas(Gestion_Trames, width=24, height=24)
Fleche_bas.grid(row=3, column=2)
photo_flechebas = PhotoImage(file="fleche_bas.png")
Fleche_bas.create_image(0, 0, image=photo_flechebas, anchor=NW)

Button(Gestion_Trames, text ='Delai :', command = Modif_Delai, width=7).grid(row=4, column=0, pady=5)
delai_field= Entry(Gestion_Trames, width=9)
delai_field.grid(row=4, column=1, pady=5)

Label(Gestion_Trames, text="Trame envoyée").grid(row=5, column=0, columnspan=2)
liste_trame = Listbox(Gestion_Trames, width=24, height=15)
liste_trame.grid(row=6, column=0, columnspan=2)

Button(Gestion_Trames, text ='Ajouter', command = Ajouter_Pattern, width=8).grid(row=7, column=0, pady=5)
Button(Gestion_Trames, text ='Enlever', command = Enlever_Pattern, width=8).grid(row=7, column=1, pady=5)

Bouton_EnvoiTrames=Button(Gestion_Trames, text ='Envoyer\nla trame !', command = Envoyer_Trame,\
													height=4, width=20, fg='purple',cursor='hand1')
Bouton_EnvoiTrames.grid(row=8, column=0, columnspan=2, pady=10)
#####################################################################################################

# On remplit le canevas principal et les étages de carrés blancs
Init()

# Bouton Envoyer
Button(Mafenetre, text ='Envoyer', fg="purple", command = Envoyer).grid(row=3, column=1, pady=5)

# Bouton Effacer
Button(Mafenetre, text ='Effacer', command = Init).grid(row=3, column=2, pady=5)

# Bouton Open
Button(Mafenetre, text ='Open', command = Open).grid(row=3, column=3, pady=5)

# Bouton Save
Button(Mafenetre, text ='Save', command = Save_Popup).grid(row=3, column=4, pady=5)

# Bouton Quitter
Button(Mafenetre, text ='Quitter', command = Mafenetre.destroy).grid(row=3, column=5, pady=5)

Mafenetre.mainloop()

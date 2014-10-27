#!/usr/bin/env python3

import sys, math
from pylibftdi import Device
from tkinter import *
from time import sleep

class Interface(Frame):
    
    """Notre fenêtre principale.
    Tous les widgets sont stockés comme attributs de cette fenêtre."""
    
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        self.pack(fill=BOTH)
        
        # Création de nos widgets
        self.var_choix = StringVar()

        self.choix_rouge = Radiobutton(fenetre, text="Rouge", variable=self.var_choix, value="rouge")
        self.choix_bleu = Radiobutton(fenetre, text="Bleu", variable=self.var_choix, value="bleu")
        self.choix_off = Radiobutton(fenetre, text="Off", variable=self.var_choix, value="off")

        self.choix_rouge.pack()
        self.choix_bleu.pack()      
        self.choix_off.pack()
                
        self.bouton_send = Button(self, text="Send", fg="red", command=self.choix)
        self.bouton_send.pack(side="left")       
    
        self.bouton_quitter = Button(self, text="Quitter", command=self.quit)
        self.bouton_quitter.pack(side="right")

    def choix(self):
        with Device (mode = 't') as dev:
            dev.baudrate = 19200


            i=0

            if self.var_choix.get()=='rouge' :

                while i<64 :
                    dev.write(chr(0x00))
                    dev.write(chr(0xFF))                                
                    i=i+1

            elif self.var_choix.get()=='bleu' :

                while i<64 :
                    dev.write(chr(0xFF))
                    dev.write(chr(0x00))                                
                    i=i+1

            elif self.var_choix.get()=='off' :

                while i<128 :
                    dev.write(chr(0x00))                                
                    i=i+1                        

            else :
                while i<128 :
                    dev.write(chr(0x00))                            
                    i=i+1


fenetre = Tk()
interface = Interface(fenetre)

interface.mainloop()
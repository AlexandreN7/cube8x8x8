     ______  _____      _           _
    |___   /| ___ \    | |         | |
        / / | |_/ /___ | |__   ___ | |_
       / /  |    // _ \| '_ \ / _ \|  _|
      / /   | |\ \ (_) | |_) | (_) | |_
     /_/    |_| \_\___/|____/ \___/ \__|
                              7robot.fr

Projet cube8x8x8
================

Organisation des trames :

pc => pic maitre 

pic maitre => pic esclave : 128 octets
| 16 octets pour le pic 1 | 16 octets pour le pic 2 | ...

Par pic esclave :
| octet étage 1 Bleu | octet étage 1 Rouge |.|.|octets pour les autres PICs (ignorés)|.|.| octet étage 2 Bleu | octet étage 2 Rouge | ...

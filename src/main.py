# -*- coding: utf-8 -*-

from sys import argv

from bnavale import *

lancerJeu = True
if len(argv) == 4:
    try:
        n = int(argv[1])
        m = int(argv[2])
    except:
        print ('n et m doivent être des entiers !')
        lancerJeu = False
    
    flotte = argv[3]
    descriptionFlotte = lireDescription(flotte)
    if descriptionFlotte == None:
        print('Le chemin pour le fichier de description des bateau ou le fichier en lui-même est invalide.')
        lancerJeu = False
    if lancerJeu:
        dicoJoueur1 = initialiserGrille(n, m, descriptionFlotte, 1)
        dicoJoueur2 = initialiserGrille(n, m, descriptionFlotte, 2)
        bateauxTouches2, bateauxTouches1 = [], []
    joueur = 0
        

elif len(argv) == 2:
    n, m, dicoJoueur1, dicoJoueur2, joueur, bateauxTouches1, bateauxTouches2 = restaurer(argv[1])
    if n == None:
        print('Le chemin pour le fichier a charger ou le fichier en lui-même est invalide.')
        lancerJeu = False

else:
    print ('Nombre invalide d\'argument, veuillez relancer le programme.')
    lancerJeu = False

if lancerJeu:
    gagnant = finPartie(dicoJoueur1, dicoJoueur2)
    action = None
    while gagnant == False and action != 1:
        print('Joueur '+str(joueur+1)+', choisissez une action :')
        print('(1) Arr�ter et sauvegarder la partie.\n(2) Attaquer.\n(3) Afficher votre grille.')
        action = raw_input('Votre choix : ')
        while action != '1' and action != '2' and action != '3':
            action = raw_input('Votre choix : ')
        action = int(action)
        if action == 1:
            sauvegarde = raw_input('Dans quel fichier ? ')
            erreur = sauvegarder(sauvegarde, n, m, dicoJoueur1, dicoJoueur2, joueur,bateauxTouches1, bateauxTouches2)
            if erreur:
                print ('Chemin invalide pour le fichier de sauvegarde.')
                joueur -=1
                action = None

        elif action == 2:
            erreur = 1
            while erreur == 1:
                erreur = 0
                try:
                    yAttaque = raw_input('Ligne : ')
                    if not yAttaque.isdigit():
                        raise ValueError('La valeur entré doit être un entier !')
                    if int(yAttaque) < 0 or int(yAttaque) >= m:
                        raise ValueError('La valeur entré doit etre comprise entre 0 et '+str(m-1)+' !')
                except ValueError as textErreur:
                    print (textErreur)
                    erreur = 1
            yAttaque = int(yAttaque)

            erreur = 1
            while erreur == 1:
                erreur = 0
                try:
                    xAttaque = raw_input('Colonne : ')
                    if not xAttaque.isdigit():
                        raise ValueError('La valeur entré doit etre un entier !')
                    if int(xAttaque) < 0 or int(xAttaque) >= n:
                        raise ValueError('La valeur entré doit etre comprise entre 0 et '+str(n-1)+' !')
                except ValueError as textErreur:
                    print (textErreur)
                    erreur = 1
            xAttaque = int(xAttaque)

            if joueur == 0:
                dicoJoueur2, bateauxTouches2 = tour(xAttaque, yAttaque, dicoJoueur2, bateauxTouches2)
            else:
                dicoJoueur1, bateauxTouches1 = tour(xAttaque, yAttaque, dicoJoueur1, bateauxTouches1)

        elif action == 3:
            if joueur == 0:
                afficherGrille(n, m, dicoJoueur1, bateauxTouches1)
            else:
                afficherGrille(n, m, dicoJoueur2, bateauxTouches2)
            joueur -= 1

        joueur += 1
        joueur = joueur%2
        gagnant = finPartie(dicoJoueur1, dicoJoueur2)

    if gagnant == False:
        print 'Votre partie a bien été sauvegardé.'
    else:
        print 'F�licitation joueur '+gagnant+' ! Vous remportez la partie !'
    print 'Le programme va maintenant s\'arreter.'

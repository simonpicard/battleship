# -*- coding: utf-8 -*-

from os import system


def lireDescription(flotte):
    """Prends en paramètre un fichier texte descrivant une flotte.
    Le fichier doit être ordonné de cette fa�on :
    'nombre de case que prends le bateau' 'nom du bateau', un bateau par ligne.
    La fonction renvoie alors un dictionnaire avec comme clef le nom du bateau et sa taille en valeur."""
    try:
        descriptionFlotte = open(flotte, 'r')
        descriptionFlotteLignes = descriptionFlotte.readlines()
        descriptionBateau = {}
        for i in range(len(descriptionFlotteLignes)):
            bateau = descriptionFlotteLignes[i].strip('\n').split(' ')
            descriptionBateau[bateau[1]] = int(bateau[0])
        descriptionFlotte.close()
    except:
        descriptionBateau = None
    return descriptionBateau

def initialiserGrille(n, m, flotte, joueur):
    '''Permet de créer un dictionnaire représentant une grille de bataille navale.
    La clef du dictionnaire représente la case du bateau et sa valeur le nom du bateau.
    L'utilisateur choisit où il place ses bateaux.
    Une fois tout les bateaux placé, la fonction retourne le dictionnaire.'''
    recommencer = True
    bateauPlace = 0
    dicoJoueur = {}
    while bateauPlace != len(flotte):
        nomBateau = flotte.keys()[bateauPlace]
        mauvaisPlacement = True
        while mauvaisPlacement:
            print ('Joueur '+str(joueur)+', veuillez placer votre vaisseau "'+nomBateau+'", sa taille est de '+str(flotte[nomBateau])+'.')
            erreur = 1
            while erreur == 1:
                erreur = 0
                try:
                    yBateau = raw_input('Ligne (0-'+str(m-1)+') : ')
                    if not yBateau.isdigit():
                        raise ValueError('La valeur entré doit être un entier !')
                    if int(yBateau) < 0 or int(yBateau) >= m:
                        raise ValueError('La valeur entré doit être comprise entre 0 et '+str(m-1)+' !')
                except ValueError as textErreur:
                    print (textErreur)
                    erreur = 1
            yBateau = int(yBateau)

            erreur = 1
            while erreur == 1:
                erreur = 0
                try:
                    xBateau = raw_input('Colonne (0-'+str(n-1)+') : ')
                    if not xBateau.isdigit():
                        raise ValueError('La valeur entré doit être un entier !')
                    if int(xBateau) < 0 or int(xBateau) >= n:
                        raise ValueError('La valeur entré doit être comprise entre 0 et '+str(n-1)+' !')
                except ValueError as textErreur:
                    print (textErreur)
                    erreur = 1
            xBateau = int(xBateau)

            orientationBateau = raw_input('Orientation (H/V) : ')
            while orientationBateau != 'H' and orientationBateau != 'V':
                print ('Veullez entrer soit "H" pour un placement horizontal (de gauche à droite) soit "V" pour un placement vertical (de haut en bas).')
                orientationBateau = raw_input('Orientation (H/V) : ')

            mauvaisPlacement = verifPlacement(orientationBateau, flotte, nomBateau, dicoJoueur, xBateau, yBateau, n, m)
            if not mauvaisPlacement:
                print('Placement OK.')
                for tailleBateau in range(flotte[nomBateau]):
                    dicoJoueur[xBateau, yBateau] = nomBateau
                    if orientationBateau == 'H':
                        xBateau += 1
                    else:
                        yBateau += 1
                bateauPlace += 1

            choixRecommencer = raw_input('Continuer (c) ou tout recommencer (r) ? ')
            while choixRecommencer != 'r' and choixRecommencer != 'c':
                print ('Veuillez entrer soit "r" soit "c".')
                choixRecommencer = raw_input('Continuer (c) ou tout recommencer (r) ? ')
            if choixRecommencer == 'r':
                mauvaisPlacement = False
                bateauPlace = 0
                dicoJoueur = {}
    system('cls')
    print ('Tout vos bateaux ont �t� plac�s !')
    return dicoJoueur

def verifPlacement(orientationBateau, flotte, nomBateau, dicoJoueur, xBateau, yBateau, n, m):
    '''Vérifie que le placement d'un bateau � une certaine coordonné dans une grille est possible.'''
    mauvaisPlacement = False
    if orientationBateau == 'H':
        if xBateau + flotte[nomBateau] > n:
            mauvaisPlacement = True
            print('Placement invalide : bateau trop grand pour pour ce placement, veuillez recommencer le placement de ce bateau.')
    else:
        if yBateau + flotte[nomBateau] > m:
            mauvaisPlacement = True
            print('Placement invalide : bateau trop grand pour pour ce placement, veuillez recommencer le placement de ce bateau.')
    indice = 0
    xBateauTest, yBateauTest = xBateau, yBateau
    while indice < flotte[nomBateau] and not mauvaisPlacement:
        #if verifCollision(dicoJoueur,xBateauTest, yBateauTest):
        if (xBateauTest, yBateauTest) in dicoJoueur:
            mauvaisPlacement = True
            print('Placement invalide : un bateau se trouve déjà là, veuillez recommencer le placement de ce bateau.')
        if orientationBateau == 'H':
            xBateauTest += 1
        else:
            yBateauTest += 1
        indice += 1
    return mauvaisPlacement

def afficherGrille(n,m,dico,bateauxTouches):
    '''Cette fonction affiche une grille de bataille navale
    � partir du dictionnaire créer par la fonction initialiserGrille.'''
    print ' ',
    for x in range (n):
        print x,
        print (2-len(str(x)))*' ',
    print '\n',
    print '  ' + n*'-   '
    for y in range(m):
        print '|',
        for x in range(n):
            if (x, y) in dico:
                print 'O',
            elif (x, y) in bateauxTouches :
                print 'X',
            else:
                print ' ',
            print '|',
        print y
        print '  ' + n*'-   '
    print('O = bateau intacte\nX = bateau touché\nCase vide = mer')
    effacer = raw_input('Appuyez sur enter pour effacer la grille')
    while effacer != '':
        effacer = raw_input('Appuyez sur enter pour effacer la grille')
    system('cls')

def verifCollision(dico,i,j):
    '''Vérifie si un bateau se trouve à la position (i, j) dans
    la grille repr�sent�e par le dictionnaire.'''
    res = False
    if (i, j) in dico:
        res = True
    return res

def tour(i,j,dicoJeu, bateauxTouches):
    '''En fonction du résultat de verifCollision, la fonction affiche le résultat de l'attaque,
    modifie le dictionnaire et la liste des bateaux touché si besoin puis les retourne.'''
    if not verifCollision(dicoJeu,i,j):
        print 'Raté !'
    else:
        bateauTouche = dicoJeu.pop((i,j))
        if bateauTouche not in dicoJeu.values():
            print 'Coulé !'
        else:
            print 'Touché !'
        bateauxTouches.append((i,j))
    return dicoJeu, bateauxTouches

def finPartie(dicoJoueur1, dicoJoueur2):
    '''Vérifie si la partie est termin�, si oui retourne le numéro du joueur gagnant,
    retourne False sinon.'''
    if dicoJoueur1 == {}:
        res = '2'
    elif dicoJoueur2 == {}:
        res = '1'
    else:
        res = False
    return res

def sauvegarder(fichier, n, m, grille1, grille2,joueur,bateauxTouches1, bateauxTouches2):
    '''Sauvegarde la partie dans un fichier'''
    try:
        save = open(fichier, 'w')
        save.write(str(n) +'\n'+ str(m) +'\n'+ str(joueur) +'\n'+ str(grille1) +'\n'+ str(grille2)+'\n'+str(bateauxTouches1)+'\n'+str(bateauxTouches2))
        save.close()
        res = False
    except:
        res = True
    return res

def restaurer(fichier):
    '''Charge une partie à partir d'un fichier'''
    try:
        load = open(fichier, 'r')
        loadLignes = load.readlines()
        for i in range(len(loadLignes)):
            loadLignes[i] = loadLignes[i].strip('\n')
        n = int(loadLignes[0])
        m = int(loadLignes[1])
        joueur = int(loadLignes[2])
        grille1 = eval(loadLignes[3])
        grille2 = eval(loadLignes[4])
        bateauxTouches1 = eval(loadLignes[5])
        bateauxTouches2 = eval(loadLignes[6])
        load.close()
    except:
        n, m, grille1, grille2, joueur, bateauxTouches1, bateauxTouches2 = None, None, None, None, None, None, None
    return n, m, grille1, grille2, joueur, bateauxTouches1, bateauxTouches2

    

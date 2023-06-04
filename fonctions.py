# coding: utf8
"""module fonctions contenant les fonctions utiles au programme principal py.py"""
import pickle
import os
from carte import Carte
DEBUG = False

def charge_cartes(parties_en_cours):
    """Cette fonction charge les cartes existantes, pour chaque carte on instancie un objet de classe Carte et on 
    l'ajoute à la liste     cartes[]"""
    cartes = []     # Liste d'objets de classe Carte. Chaque élément de la liste sera un objet de classe Carte qui 
                    # contient un attribut labyrinthe (de type dictionnaire) qui représente le labyrinthe. 
                    # Cf la docstring de la classe Carte
    for nom_fichier in os.listdir("cartes"):
        if nom_fichier.endswith(".txt"):
            chemin = os.path.join("cartes", nom_fichier)
            nom_carte = nom_fichier[:-3].lower()    # On retire le txt à la fin
            with open(chemin, "r") as fichier:
                contenu = fichier.read()
                fichier.close()
                # Pour chaque fichier carte, on crée une instance de la classe Carte, avec des attributs:
                #  -le nom de la carte
                #  -le labyrinthe, sous forme d'un dictionnaire avec clé = (x, y) et valeur = "O" ou " " ou "." ou U" ou "X"
                #  -la position du robot, détectée par la présence d'un X dans la carte
                carte_courante = Carte(nom_carte[:-1], contenu)    # On retire le . à la fin
                # Si il y avait une partie en cours pour cette carte, on efface le X du labyrinthe de la carte originale
                # et on met un X à la position sauvegardée du robot:
                if carte_courante.nom in parties_en_cours:
                    carte_courante.labyrinthe[carte_courante.robot] = " "        # On efface le X qui était dans la carte d'origine
                    carte_courante.robot = parties_en_cours[carte_courante.nom]  # On met à jour attribut robot avec la position sauvegardée
                # Cet objet de type Carte est ajouté à la liste des cartes:
                cartes.append(carte_courante)
    return(cartes)

def ecrire_partie_en_cours(parties_en_cours):
    """Cette fonction va ouvrir le fichier parties_en_cours et écrire (dump) le dictionnaire parties_en_cours dedans"""

    try:
        with open('parties_en_cours', 'wb') as fichier:
            mon_pickler = pickle.Pickler(fichier)
            mon_pickler.dump(parties_en_cours)
            fichier.close()
    except IOError:
        print('Erreur d\'écriture dans le fichier parties_en_cours')

def lire_partie_en_cours():
    """Cette fonction va essayer d'ouvrir le fichier parties_en_cours, et s'il existe lire son contenu dans un dictionnaire
    et renvoyer le dictionnaire.
    Si le fichier n'existe pas, elle renvoie un dictionnaire vide"""

    try:
        with open('parties_en_cours', 'rb') as fichier:
            mon_depickler = pickle.Unpickler(fichier)
            parties_en_cours = mon_depickler.load()
    except IOError:    # Si le fichier n'existe pas, on renvoie un dictionnaire vide
        parties_en_cours = {}
    return parties_en_cours

def frappe_clavier(touches_permises, message_erreur):
    """Cette fonction récupère une lettre saisie par le joueur et vérifie qu'elle fait bien partie des lettres permises.
    Si ce n'est pas la cas elle affiche un message d'erreur (passé en paramètre à la fonction"""
    
    touche = input("")
    touche = touche.lower()
    
    touche_ok = True
    if len(touche) == 2:        # Cas d'une direction suivie d'un facteur de répétiiton, ex: E2
        if touche[0] not in "qneso" or touche[1] not in "123456789":
            touche_ok = False
    elif len(touche) == 1:      # Cas d'une direction simple (E, S, O, N)
        if touche not in touches_permises:
            touche_ok = False
    else:
        touche_ok = False
    
    if not touche.isalnum() or not touche_ok:     # En cas d'erreur 
        print(message_erreur)
        # On appelle de nouveau la fonction pour avoir une autre touche
        return frappe_clavier(touches_permises, message_erreur)
    else:
        return touche
    
def nouvelle_position(robot, touche, labyrinthe):
    """La fonction nouvelle_position(robot) se charge des tests et renvoie la nouvelle position du robot en prenant en compte 
    les contraintes (mur)"""
    
    # Acquisition du facteur de répétition optionnel
    if len(touche) == 2: 
        repetition = int(touche[1])
    else:
        repetition = 1
    
    # Traitement des commandes
    if touche[0] == "n":                                # Nord => on décrémente y
        for i in range(repetition):                     # Autant de fois que le facteur de répétition
            nouvelle_position = (robot[0], robot[1]-1)
            # La nouvelle position pourrait sortir du labyrinthe (si on fait N et que le robot était tout en haut)
            # on vérifie donc que le nouveau tuple de position fait bien partie des tuples du labyrinthe, et s'il
            # n'en fait plus partie on ne change pas sa position
            if nouvelle_position not in labyrinthe: nouvelle_position = (robot[0], robot[1])
            # Validation de la nouvelle position
            if labyrinthe[nouvelle_position] == "O":    # On frappe un mur en allant au Nord
                return robot                            # On renvoie la position du robot inchangée
            elif (labyrinthe[nouvelle_position] == "U"):# On atteint la sortie en allant au Nord
                robot = nouvelle_position
                return robot
                break                                   # On sort de la boucle, anyway on a gagné !
            else:                                       # Soit case vide soit "." soit U
                robot = nouvelle_position
        return robot
    elif touche[0] == "e":                              # Est => on incrémente x
        for i in range(repetition):                     # Autant de fois que le facteur de répétition
            nouvelle_position = (robot[0]+1, robot[1])
            # La nouvelle position pourrait sortir du labyrinthe (si on fait E et que le robot était tout à droite)
            # on vérifie donc que le nouveau tuple de position fait bien partie des tuples du labyrinthe, et s'il
            # n'en fait plus partie on ne change pas sa position
            if nouvelle_position not in labyrinthe: nouvelle_position = (robot[0], robot[1])
            # Validation de la nouvelle position
            if (labyrinthe[nouvelle_position] == "O"):  # On frappe un mur en allant à l'Est
                return robot                            # On renvoie la position du robot inchangée
            elif (labyrinthe[nouvelle_position] == "U"):# On atteint la sortie en allant à l'Est
                robot = nouvelle_position
                return robot
                break                                   # On sort de la boucle, anyway on a gagné !
            else:                                       # Soit case vide soit "." soit U
                robot = nouvelle_position
        return robot
    elif touche[0] == "s":                              # Sud => on incrémente y
        for i in range(repetition):                     # Autant de fois que le facteur de répétition
            nouvelle_position = (robot[0], robot[1]+1)
            # La nouvelle position pourrait sortir du labyrinthe (si on fait S et que le robot était tout en bas)
            # on vérifie donc que le nouveau tuple de position fait bien partie des tuples du labyrinthe, et s'il
            # n'en fait plus partie on ne change pas sa position
            if nouvelle_position not in labyrinthe: nouvelle_position = (robot[0], robot[1])
            # Validation de la nouvelle position
            if labyrinthe[nouvelle_position] == "O":    # On frappe un mur en allant au Sud
                return robot                            # On renvoie la position du robot inchangée
            elif (labyrinthe[nouvelle_position] == "U"):# On atteint la sortie en allant au Sud
                robot = nouvelle_position
                return robot
                break                                   # On sort de la boucle, anyway on a gagné !
            else:                                       # Soit case vide soit "." soit U
                robot = nouvelle_position
        return robot
    elif touche[0] == "o":                              # Ouest => on décrémente x
        for i in range(repetition):                     # Autant de fois que le facteur de répétition
            nouvelle_position = (robot[0]-1, robot[1])
            # La nouvelle position pourrait sortir du labyrinthe (si on fait O et que le robot était tout à gauche)
            # on vérifie donc que le nouveau tuple de position fait bien partie des tuples du labyrinthe, et s'il
            # n'en fait plus partie on ne change pas sa position
            if nouvelle_position not in labyrinthe: nouvelle_position = (robot[0], robot[1])
            # Validation de la nouvelle position
            if labyrinthe[nouvelle_position] == "O":    # On frappe un mur en allant à l'Ouest
                return robot                            # On renvoie la position du robot inchangée
            elif (labyrinthe[nouvelle_position] == "U"):# On atteint la sortie en allant à l'Ouest
                robot = nouvelle_position
                return robot
                break                                   # On sort de la boucle, anyway on a gagné !
            else:                                       # Soit case vide soit "." soit U
                robot = nouvelle_position
        return robot
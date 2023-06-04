# -*-coding:Utf-8 -*

"""py un jeu de robot dans un labyrithe qui se joue au claivier de la console."""

import fonctions
from carte import Carte
DEBUG = False
# On charge les infos sur les parties en cours : elle sont dans un dictionnaire parties_en_cours sauvegardé (pickler):
# Ce dictionnaire a comme clé le nom de la carte et comme valeur un tuple représentant la position du robot
# -dans le répertoire courant vérifier la présense du fichier partie_en_cours
# -s'il existe, le lire (unpickle) dans un dico 
# -s'il n'existe pas (encore), on crée un dico vide
parties_en_cours = fonctions.lire_partie_en_cours()

# On charge les cartes existantes, pour chaque carte on instancie un objet de classe Carte et on l'ajoute à la liste 
# cartes[]
cartes = fonctions.charge_cartes(parties_en_cours)

# On affiche les cartes existantes, avec une indication pour les parties en cours
print("Labyrinthes existants :")
for i, carte in enumerate(cartes):
    # Si partie en cours pour cette carte, l'afficher
    # Le texte "(partie en cours)" sea ajouté à la suite du nom de la carte si besoin
    try:
        # Si la partie a été sauvée, position_robot contiendra un tuple qui représente la dernièr position du robo (x, y)
        position_robot = parties_en_cours[carte.nom]
        partie_en_cours_texte = "(partie en cours)"
    except KeyError:    # Si le dico ne contient pas cette carte (pas de partie en cours sauvée pour cettte carte)
        partie_en_cours_texte = ""
    print("  {0} - {1}. {2}".format(i + 1, carte.nom, partie_en_cours_texte))

touches_permises = ""   
for i in range(len(cartes)):    # On construit une chaine représentant les touches permises, c.à.d. les index de la liste cartes
    touches_permises += str(i+1)
print("")
print("Entrez un numéro de labyrinthe pour commencer à jouer : ", end="")
touche = fonctions.frappe_clavier(touches_permises, "Choisissez un des labyrinthes proposés: [" + touches_permises + "]")
print("")

# On affiche le labyrinthe choisi par le joueur et on chargle l'objet carte_en_cours
carte_en_cours = cartes[int(touche) - 1]
robot = carte_en_cours.robot
###fonctions.afficher_labyrinthe(carte_en_cours)
carte_en_cours.afficher_labyrinthe()

# Boucle principale: tant que le joueur ne quitte pas (Q) on gère son déplacement du robot, en vérifiant à chaque fois
# que le déplacement demandé est possible. Le jeu est terminé quand la prochaine position du robot correspond à la sortie (U)
continuer_partie = 'o'
while continuer_partie != 'n':
    # Note: le joueur peut faire suivre son ordre de direction par un nombre, que l'on limite à 9 au maximum. Il peut donc
    # entrer jusqu'à 2 caractères
    touche = fonctions.frappe_clavier("qneso123456789", "Les touches suivantes sont permises: Q (quitter), N (Nord), E (Est), S (Sud), O (Ouest), suivies d'un chiffre (optionnel) de 1 à 9, par exemple: s8")
    if touche == "q":   # Le joueusr quitte la partie
        # On sauve dans un fichier le dico des parties en cours
        fonctions.ecrire_partie_en_cours(parties_en_cours)
        continuer_partie = 'n'
        print("\nAu revoir")
        continue
    else:
        # On calcule la prochaine position du robot en fonction de l'ordre donné. La fonction nouvelle_position(robot) se
        # charge des test et renvoie la nouvelle position du robot en prenant en compte les contraintes
        # (mur, ne pas sortir de l'espace de la carte)
        if DEBUG: print("DEBUG: ancienne position = ", carte_en_cours.robot)
        nouvelle_position = fonctions.nouvelle_position(carte_en_cours.robot, touche, carte_en_cours.labyrinthe)
        carte_en_cours.robot = nouvelle_position                    # On met à jour l'attribut robot
        if DEBUG: print("DEBUG: nouvelle position = ", carte_en_cours.robot)
        parties_en_cours[carte_en_cours.nom] = carte_en_cours.robot # On sauve la position du robot dans le dictionnaire des
                                                                    # parties en cours
        # On teste si le robot n'a pas trouvé la sortie !
        if carte_en_cours.labyrinthe[carte_en_cours.robot] == "U":  # YES !
            ###fonctions.afficher_labyrinthe(carte_en_cours)
            carte_en_cours.afficher_labyrinthe()
            print("", "Félicitations ! Vous avez gagné !", "")
            # Dire que la partie n'est plus en cours, del de l'élément carte.nom dans le dico partiues_en cours
            del parties_en_cours[carte_en_cours.nom]
            # On sauve dans un fichier le dico des parties en cours
            fonctions.ecrire_partie_en_cours(parties_en_cours)
            continuer_partie = 'n'
            continue
        ###fonctions.afficher_labyrinthe(carte_en_cours)
        carte_en_cours.afficher_labyrinthe()
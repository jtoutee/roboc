# -*-coding:Utf-8 -*

"""Ce module contient la classe Carte."""
DEBUG = False

class Carte:

    """Objet qui contient le nom de la carte, la carte sous forme de dictionnaire (la clé étant un tuple (x, y),
    la valeur étant le contenu d'une case) et la position courante du robot (x, y).
    L'objet contient aussi un attribut tuple robot qui repésente la position du robot.
    L'objet contient aussi une méthode qui permet de lire le fichier carte et de le transformer
    en dictionnaire."""

    def __init__(self, nom, chaine):
        self.nom = nom
        self.nb_colonnes = 0    # Attribut pour mémoriser le nombre de colonnes (pour affichage ultérieur)
        self.nb_lignes = 0      # Attribut pour mémoriser le nombre de lignes (pour affichage ultérieur)
        self.robot = (0, 0)     # Positiondu robot en (x, y)
        self.labyrinthe = self.creer_labyrinthe_depuis_chaine(chaine)

    def creer_labyrinthe_depuis_chaine(self, chaine):
        """ Lire la chaine (contenu) ligne par ligne puis caractère par caractère, et créer un dictionnaire
        qui représente le labyrinthe sous forme d'un dictionnaire avec clé = (x, y) et valeur = "O" ou " " ou "."
         ou U" ou "X"
        L'origine (x, y) = (0, 0) est le coin en haut et à gauche de la carte"""

        x = 0   # x = numéro de colonne
        y = 0   # y = numéro de ligne
        labyrinthe = {}

        # Vérifier qu'il y a bien un X dans la carte. S'il a été oublié, on le met arbitrairement à la place du
        # premier espace rencontré:
        if "X" not in chaine:
            chaine = chaine.replace(" ", "X", 1)
        
        liste = chaine.split(sep="\n")   # On tokenise la chaine en une liste, avec une ligne par élément
        self.nb_colonnes = len(liste[0]) # Le 1er élément contient autant de caractères que de colonnes (le lbyrinthe est rectangulaire  
        for ligne in liste:
            x = 0   # Nouvelle ligne, on remet donc le numéro de colone à 0
            for char in ligne:
                labyrinthe[(x, y)] = char
                if char == "X":     # Si on tombe sur le robot, on met à jour l'attribut robot
                    self.robot = (x, y)
                    labyrinthe[(x, y)] = " "    # Et on efface le X de la carte, car dorénavant la position du robot est dand l'attribut robot
                x += 1  # Caractère suivant
            y += 1  # Ligne suivante
            self.nb_lignes += 1
        return labyrinthe

    def afficher_labyrinthe(self):
        """Cette fonction affiche le labyrinthe (attribut de l'objet passé en paramètre)
        Note: si on passe par la position d'une porte, telle que mémorisée dans l'attribut portes de l'objet carte,
        on affiche la porte. En effet la porte peut avoir été 'effacée' par le déplacement du robot."""
        if DEBUG: print("DEBUG: Entrée de la fonction aficher_labyrinthe: robot = ", self.robot)
        for ligne in range(self.nb_lignes):
            for colonne in range(self.nb_colonnes):
                ###print("DEBUG: Colonne = {}, Ligne = {}, Char = {}".format(colonne, ligne, carte.labyrinthe[(colonne, ligne)]))
                ###print("DEBUG: colonne, ligne - robot",colonne, ligne, carte.robot)
                if (colonne, ligne) == self.robot:
                    print("X", end='')
                else:
                    print(self.labyrinthe[(colonne, ligne)], end='')
            print("")   # Ligne suivante

    def __repr__(self):
        return "<Carte {}>".format(self.nom)

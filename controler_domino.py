from beans_domino import *
from random import randint, sample


class Partie:
    """
    2 joueurs chacun prend 7 dominos, à 3 et 4 joueurs chacun prend 6 dominos, à 5 et 6 joueurs chacun prend 4 dominos.
    """
    regles = { 2: 7,
               3: 6,
               4: 6,
               5: 4,
               6: 4
              }
    
    def jeux_complet():
        """Génère une boite de domino complète

        Returns:
            [List]: List de dominos
        """
        jeux_complet = []

        for i in range(0, 7):
            j = 0
            for j in range (0, i):
                jeux_complet.append(Domino(j, i))
            jeux_complet.append(Domino(i, i))
        return jeux_complet
    
    def __init__(self, partie_name=""):
        self._joueurs = []
        self._pioche = None
        self._plateau = []
        self.partie_name = partie_name
        self._joueur_courant_position = 0

    def ajouter_joueur(self, joueur):
        if len(self._joueurs) < 7 :
            if isinstance(joueur, str):
                self._joueurs.append(Joueur(joueur))
            elif isinstance(joueur, Joueur):
                 self._joueurs.append(joueur)
            else : 
                raise Exception ('La création de joueur doit être de type str ou obj !')
        else :
            raise Exception("Il ne peut pas y avoir plus de 6 joueurs")

    def distribue_dominos(self):
        """
        Distribus les dominos de manière aléatoire aux joueurs
        """
        # Initialisation de la pioche
        self._pioche = Partie.jeux_complet()

        # nombre de joueurs
        nb_joueurs = len(self._joueurs)
        if nb_joueurs < 1:
            raise Exception("Aucun joueur n'a été ajouté")
        elif nb_joueurs == 1:
            self.ajouter_joueur("Ordinateur")
            nb_joueurs = len(self._joueurs)

        # nombre de dominos à distribuer en fonction du nombre de joueurs
        nb_dominos = Partie.regles[nb_joueurs]

        for joueur in self._joueurs:
            # on tire au sort les dominos
            main = sample(self._pioche, nb_dominos)
            # on affecte les dominos au joeur
            joueur.dominos_en_main = main
            # on suprrime les dominos déjà distribués de la pioche
            for domino in main:
                self._pioche.remove(domino)
    
    def pioche(self):
        domino = None
        if len(self._pioche) > 0:
            domino = sample(self._pioche, 1)
            self._pioche.remove(domino)
        return domino

    def affiche_plateau(self):
        for domino in self._plateau:
            print(domino, end="")
        print("")
    
    def affiche_joueurs_mains(self):
        for joueur in self._joueurs:
            print(joueur)

    def affiche_pioche(self):
        print(f"Pioche:{len(self._pioche)}=>{self._pioche}")
    
    def deposer_domino_a_gauche(self, domino):
        """ Ajoute le domino à la chaine
        Args:
            domino (Domino): le domino à ajouter

        Raises:
            Exception: S'il ne s'agit pas d'un Domino

        Returns:
            Boolean: True si le Domino a été déposé, False si le domino ne pouvait pas être déposé (incompatible)
        """
        ajout_success = self._ajouter_domino(domino, "gauche")
        return ajout_success
    
    def deposer_domino_a_droite(self, domino):
        """ Ajoute le domino à la chaine

        Args:
            domino (Domino): le domino à ajouter

        Raises:
            Exception: S'il ne s'agit pas d'un Domino

        Returns:
            Boolean: True si le Domino a été déposé, False si le domino ne pouvait pas être déposé (incompatible)
        """
        ajout_success = self._ajouter_domino(domino, "droite")
        return ajout_success

    def deposer_premier_domino(self, domino):
        """ Ajoute le domino à la chaine

        Args:
            domino (Domino): le domino à ajouter

        Raises:
            Exception: S'il ne s'agit pas d'un Domino

        Returns:
            Boolean: True si le Domino a été déposé, False si le domino ne pouvait pas être déposé (incompatible)
        """
        ajout_success = self._ajouter_domino(domino, "")
        return ajout_success  

    def joueur_courant(self):
        """
        Raises:
            Exception: Si aucun joueur couarnt n'est définit (avant de déterminer le 1er joueur par exemple)

        Returns:
            [Joeur]: Le joueur courant
        """
        if self._joueur_courant_position > -1:
            return self._joueurs[self._joueur_courant_position]
        else :
            raise Exception("Aucun joueur courant définit")
    
    def joueur_suivant(self):
        """
        Raises:
            Exception: Si aucun joueur courant n'est définit, il ne peut pas y avoir de joueur suivant

        Returns:
            [Joueur]: Le joueur suivant
        """
        if self._joueur_courant_position > -1:
            self._joueur_courant_position += 1
            if self._joueur_courant_position >= len(self._joueurs):
                self._joueur_courant_position = 0
            return self._joueurs[self._joueur_courant_position]
        else :
            raise Exception("Aucun joueur courant définit, donc aucun suivant ne peut être définit")

    def premier_joueur(self):
        """Identifie le premier joueur de la partie en suivant les règles suivantes :
            - Le joueur ayant le double le plus élevé commence la partie de dominos et pose son domino au centre de la 
            table (si personne n’a pas le double 6, c’est le double 5 qui commence, etc.… et 
            - si personne n’a de double, c'est le domino 6/5 qui commence ou sinon le 6/4 etc.). 
                  
        Returns:
            [Joueur]: Le joueur qui doit commencer la partie
        """
        double_domino = None 
        valeur_max = None
        premier_joueur = None
        pos = 0
        for joueur in self._joueurs:
            # On vérifie la présence de double pour chaque joueurs, en gardant le plus grand
            if double_domino == None:
                # On défini la valeur de double_domino par la première valeur trouvé
                double_domino = joueur.maxi_double()
                if double_domino is not None:
                    premier_joueur = joueur
                    self._joueur_courant_position = pos
            else :
                # On vérifie maintenant si les nouveaux doubles trouvé sont plus grands que la valeur enregistré
                double_joueur = joueur.maxi_double()
                if double_joueur is not None and double_joueur.score() > double_domino.score() :
                    double_domino = joueur.maxi_double()
                    premier_joueur = joueur
                    self._joueur_courant_position = pos
            pos += 1

        # On applique maintenant la règle dans le cas ou aucun joueurs ne possède de domino double
        # On regarde donc la valeur maximun des dominos présent dans la main de chaque joueurs
        if premier_joueur is None :
            pos = 0
            for joueur in self._joueurs:
                if valeur_max == None:
                    valeur_max = joueur.maxi_domino()
                    premier_joueur = joueur
                    self._joueur_courant_position = pos
                else :
                    if  joueur.maxi_domino() is not None and joueur.maxi_domino() > valeur_max :
                        valeur_max = joueur.maxi_domino()
                        premier_joueur = joueur
                        self._joueur_courant_position = pos
                pos += 1
        return premier_joueur
    
    @property
    def joueurs(self):
        return self._joueurs

    @joueurs.setter
    def joueurs(self, joueurs):
         raise Exception("Impossible de modifier les joueurs en cours de partie !")        

    def _ajouter_domino(self, domino, position):
        """[summary]

        Args:
            domino (Domino): le domino à ajouter
            position (String): emplacement où déposer le domino : 'droite' ou 'gauche'

        Raises:
            Exception: Si l'emplacement indiqué n'existe pas ou s'il ne s'agit pas d'un Domino

        Returns:
            Boolean: True si le Domino a été déposé, False si le domino ne pouvait pas être déposé (incompatible)
        """
        ajout_success = False
        if domino != None and domino.isinstance(Domino):
            # Traitement du cas du premier domino
            if len(self._plateau) == 0 :
                self._plateau = [domino]
            else :
                # Traitement des autres domino
                if position == "droite":
                    # Vérifier que la valeur de gauche du domino = la valeur de droite du dernier domino du plateau
                    domino_plateau = self._plateau[-1]
                    if domino.valeur_a_gauche == domino_plateau.valeur_a_droite:
                        self._plateau.append(domino)
                        ajout_success = True
                elif position == "gauche":
                    domino_plateau = self._plateau[0]
                    if domino.valeur_a_droite == domino_plateau.valeur_a_gauche:
                        self._plateau.insert(0, domino)
                        ajout_success = True
                else:
                    raise Exception("Position non gérée pour l'instant", position)
        else:
            raise Exception("Domino attendu et non", domino)
        return ajout_success
            
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                                              TESTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_partie():
    partie1 = Partie()
    partie1.ajouter_joueur("Vincent")
    partie1.ajouter_joueur("Aurélie")
    partie1.ajouter_joueur("Toto")
    partie1.affiche_joueurs_mains()
    partie1.distribue_dominos()
    partie1.affiche_joueurs_mains()
    partie1.affiche_pioche()
    print( "premier joueur = ", partie1.premier_joueur())

# jeux = Partie.jeux_complet()
# print(len(jeux), jeux)

# test_partie()
   

def test_premier_joueur():
    print("Test sur la définition du premier joueur")
    partie1 = Partie()
    # print( "le premier joueur est : ",partie1.premier_joueur())
    partie1.ajouter_joueur("JoueurUn")
    print( "le premier joueur est : ",partie1.premier_joueur())
    partie1.ajouter_joueur('JoueurDeux')
    j1 = partie1.joueurs[0]
    j2 = partie1.joueurs[1]
    j1.ajouter_domino(Domino(2, 6))
    j1.ajouter_domino(Domino(3, 2))
    j2.ajouter_domino(Domino(6 ,4))
    j2.ajouter_domino(Domino(1 ,5))
    partie1.affiche_joueurs_mains()
    print( "le premier joueur est : ",partie1.premier_joueur())
    assert partie1.premier_joueur() == j2
    j1.ajouter_domino(Domino(6, 6))
    j2.ajouter_domino(Domino(3 ,3))
    print( "le premier joueur est : ",partie1.premier_joueur())
    assert partie1.premier_joueur() == j1
    # assert mon_domino.valeur_a_gauche in range(0, 7)
    # assert mon_domino.valeur_a_droite in range(0, 7)
    # mon_domino = Domino(0, 5)
    # assert mon_domino.valeur_a_gauche == 0
    # assert mon_domino.valeur_a_droite == 5
    # mon_autre_domino = Domino(1, 4)
    # assert mon_autre_domino.__repr__() == '[1:4]'
    # assert mon_domino.__repr__() == '[ :5]'
    # print(mon_domino, mon_autre_domino)


test_premier_joueur()
import random
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
    
    def __init__(self):
        self._joueurs = []
        self._pioche = None
        self._plateau = []

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
    
    def ajouter_domino(self, domino, position):
        ajout_success = False
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
        return ajout_success

    def premier_joueur(self):
        """Le joueur ayant le double le plus élevé commence la partie de dominos et pose son domino au centre de la 
        table (si personne n’a le double 6, c’est le double 5 qui commence, etc.… et si personne n’a de double, c'est le domino 6/5 qui commence ou 
        sinon le 6/4 etc.). Le joueur suivant (à gauche du premier joueur) doit poser l’un de ses dominos dont l’un des côtés est identique à un côté du premier domino. 
        Puis c’est au joueur suivant de jouer et ainsi de suite. 
        Les joueurs peuvent poser leur domino à l’une ou l’autre des extrémités de la chaîne.
        """
        double_domino = None 
        valeur_max = None
        premier_joueur = None
        
        for joueur in self._joueurs:
            # On vérifie la présence de double pour chaque joueurs, en gardant le plus grand
            if double_domino == None:
                # On défini la valeur de double_domino par la première valeur trouvé
                double_domino = joueur.maxi_double()
                if double_domino is not None:
                    premier_joueur = joueur
            else :
                # On vérifie maintenant si les nouveaux doubles trouvé sont plus grands que la valeur enregistré
                double_joueur = joueur.maxi_double()
                if double_joueur is not None and double_joueur.score() > double_domino.score() :
                    double_domino = joueur.maxi_double()
                    premier_joueur = joueur
        # On applique maintenant la règle dans le cas ou aucun joueurs ne possède de domino double
        # On regarde donc la valeur maximun des dominos présent dans la main de chaque joueurs
        if premier_joueur is None :
            for joueur in self._joueurs:
                if valeur_max == None:
                    valeur_max = joueur.maxi_domino()
                    premier_joueur = joueur
                else :
                    if  joueur.maxi_domino() is not None and joueur.maxi_domino() > valeur_max :
                        valeur_max = joueur.maxi_domino()
                        premier_joueur = joueur
        return premier_joueur
    
    @property
    def joueurs(self):
        return self._joueurs

    @joueurs.setter
    def joueurs(self, joueurs):
         raise Exception("Impossible de modifier les joueurs en cours de partie !")        
            


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
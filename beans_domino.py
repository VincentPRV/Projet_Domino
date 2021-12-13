"""
Ce fichier contient toutes les classes utilisées pour ce projet
"""
import random

class Domino:
    """Cette classe représente un Domino
    """
    def __init__(self, valeur_a_gauche=0, valeur_a_droite=0, generate=False):
        """[summary]
            1. On veut pouvoir construire un domino avec des valeurs déterminées
            2. On veut pouvoir construire un domino avec des valeurs tirées au hasard
            3. On veut s'assurer que les valeurs des côtés du domino sont comprises entre 0 et 6
        Args:
            valeur_a_gauche (int, optional): one face value. Defaults to 0.
            b (int, optional): one face value. Defaults to 0.
            random (bool, optional): To generate the domino values. Defaults to False.

        Raises:
            Exception: La valeur doit être entre 0 et 6 (inclus)
        """
        if generate:
            valeur_a_gauche = random.randint(0, 7)
            valeur_a_droite = random.randint(0, 7)
        if valeur_a_gauche > 6 | valeur_a_gauche < 0 | valeur_a_droite > 6 | valeur_a_droite < 0:
            raise Exception("La valeur doit être entre 0 et 6 (inclus)")
        self._valeur_a_gauche = valeur_a_gauche
        self._valeur_a_droite = valeur_a_droite

    def score(self):
        """ The domino's value (sum of 2 values)"""
        return self.valeur_a_gauche + self._valeur_a_droite
    
    def inverse(self):
        temp = self._valeur_a_gauche
        self._valeur_a_gauche = self._valeur_a_droite
        self._valeur_a_droite = temp

    def __repr__(self):
        return str(self)

    def est_compatible(self, valeur):
        """Teste si le domino est compatible avec une valeur passée en paramètre
        c'est-à-dire s'il peut être placée à côté de cette valeur
        """
        return self._valeur_a_droite == valeur or self._valeur_a_gauche == valeur

    @property
    def valeur_a_gauche(self):
        return self._valeur_a_gauche

    @valeur_a_gauche.setter
    def valeur_a_gauche(self, valeur_a_gauche):
        raise Exception("La valeur ne peut pas être modifiée")

    @property
    def valeur_a_droite(self):
        return self._valeur_a_droite

    @valeur_a_droite.setter
    def b(self, valeur_a_droite):
        raise Exception("La valeur ne peut pas être modifiée")

    def __str__(self):
        return f"[{self.valeur_a_gauche}:{self.valeur_a_droite}]"


class Plateau:
    def __init__(self):
        pass


class Joueur:
    def __init__(self, name):
        self._dominos_en_main = {}
        self._name = name

    def addDomino(self, new_domino):
        pass

class Partie:

    def __init__(self, nb_joueurs=2):
        self._nb_joueurs = nb_joueurs
        # TODO : initialiser la pioche dans la partie ou dans le plateau ?
        self._pioche = None
        self._plateau = Plateau()
        self._joueurs = {}
        # TODO : vérifier si le ça prend bien le dernier élément
        for i in range (1, nb_joueurs+1):
            self._joueurs['Joueur'+i] = Joueur('Joueur'+i)
        # TODO : distribuer les dominos

    def distribue_dominos(self):
        """
        2 joueurs chacun prend 7 dominos, à 3 et 4 joueurs chacun prend 6 dominos, à 5 et 6 joueurs chacun prend 4 dominos.
        """
        pass

    def jeux_complet():
        """Génère une boite de domino complète

        Returns:
            [List]: List de dominos
        """
        jeux_complet = []
        for i in range(0, 6):
            j = 0
            for j in range (0, i):
                jeux_complet.append(Domino(j, i))
        return jeux_complet

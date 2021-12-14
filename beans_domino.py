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
        if valeur_a_gauche > 6 or valeur_a_gauche < 0 or valeur_a_droite > 6 or valeur_a_droite < 0:
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

    def est_double(self):
        return self._valeur_a_droite == self._valeur_a_gauche
    
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
    def valeur_a_droite(self, valeur_a_droite):
        raise Exception("La valeur ne peut pas être modifiée")

    def __str__(self):
        return f"[{self.valeur_a_gauche}:{self.valeur_a_droite}]"
    
    def __eq__(self, other):
        
        if type(other) != type(self):
            return False
        
        # On vérifie l'égalité dans les deux sens
        equa = self.valeur_a_droite == other.valeur_a_droite and self.valeur_a_gauche == other.valeur_a_gauche
        equa = equa or (self.valeur_a_droite == other.valeur_a_gauche and self.valeur_a_gauche == other.valeur_a_droite)
        return equa


class Joueur:

    def __init__(self, name, type="humain"):
        self._dominos_en_main = []
        self.name = name
        self._type = type
        
    def ajouter_domino(self, new_domino):
        self._dominos_en_main.append(new_domino)

    def retirer_domino(self, index_domino):
        self._dominos_en_main.pop(index_domino)
        
    def maxi_domino(self):
        max_score= None
        for domino in self._dominos_en_main:
            if max_score == None:
                max_score = domino.score()
            else :
                if max_score is not None and max_score < domino.score() :
                    max_score = domino.score()
        return max_score
              
    def maxi_double(self):
        maxi = None
        for domino in self._dominos_en_main:
            if domino.est_double():
                if maxi is None:
                    maxi = domino
                elif domino.valeur_a_droite > maxi.valeur_a_droite:
                    maxi = domino
        return maxi

    def str_main(self):
        main = ""
        for domino in self._dominos_en_main:
            main += f"{domino},"
        return main[:-1]

    @property
    def dominos_en_main(self):
        return self._dominos_en_main.copy()

    @dominos_en_main.setter
    def dominos_en_main(self, dominos_en_main):
        self._dominos_en_main = dominos_en_main

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        raise Exception("Le type de joueur ne peut pas être modifié")

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.name}: {len(self._dominos_en_main)}=>" + self.str_main()


def test_domino():
    domino = Domino(5, 6)
    print(domino)
    domino.inverse()
    print(domino)

def test_joueur():
    j1 = Joueur("Player1")
    print(j1)
    j1.ajouter_domino(Domino(5, 6))
    j1.ajouter_domino(Domino(3, 4))
    j1.ajouter_domino(Domino(5, 5))
    j1.ajouter_domino(Domino(6, 6))
    j1.ajouter_domino(Domino(3, 2))
    print(j1)
    j1.retirer_domino(1)
    j1_double = j1.maxi_double()
    print("Maxi double:", j1_double)
    print("Domino not equals",j1_double == Domino(5, 5))
    print("Domino equals",j1_double == Domino(6, 6))
    print(j1)
    print('Maxi domino :', j1.maxi_domino())


test_joueur()
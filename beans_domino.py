"""
Ce fichier contient toutes les classes utilisées pour ce projet
"""
from random import randint

class Domino:
    """Cette classe représente un Domino
    """
    def __init__(self, valeur_a_gauche=-1, valeur_a_droite=-1):
        """[summary]
            1. On veut pouvoir construire un domino avec des valeurs déterminées
            2. On veut pouvoir construire un domino avec des valeurs tirées au hasard
            3. On veut s'assurer que les valeurs des côtés du domino sont comprises entre 0 et 6
        Args:
            valeur_a_gauche (int, optional): one face value. Defaults to 0.
            b (int, optional): one face value. Defaults to 0.

        Raises:
            Exception: La valeur doit être entre 0 et 6 (inclus)
        """
        if valeur_a_gauche == -1:
            valeur_a_gauche = randint(0, 6)
        if valeur_a_droite == -1:
            valeur_a_droite = randint(0, 6)

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
        c'est-à-dire s'il peut être placé à côté de cette valeur
        """
        est_comp = self._valeur_a_droite == valeur or self._valeur_a_gauche == valeur
        est_comp = est_comp or self._valeur_a_droite == 0 or self._valeur_a_gauche == 0 or valeur == 0
        return est_comp

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
        return f"[{' ' if self.valeur_a_gauche==0 else self.valeur_a_gauche}:{' ' if self.valeur_a_droite==0 else self.valeur_a_droite}]"
    
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
        for domino in self.dominos_en_main:
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


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                                              TESTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DOMINO
def test_domino_constructeur():
    print("Domino > constucteur et repr")
    mon_domino = Domino()
    assert mon_domino.valeur_a_gauche in range(0, 7)
    assert mon_domino.valeur_a_droite in range(0, 7)
    mon_domino = Domino(0, 5)
    assert mon_domino.valeur_a_gauche == 0
    assert mon_domino.valeur_a_droite == 5
    mon_autre_domino = Domino(1, 4)
    assert mon_autre_domino.__repr__() == '[1:4]'
    assert mon_domino.__repr__() == '[ :5]'
    print(mon_domino, mon_autre_domino)

def test_domino_constructeur_erreur():
    print("Domino > constucteur > exception")
    # Doit lever une exception
    try:
        mon_faux_domino = Domino(7, 7)
        raise AssertionError(f"Une exception aurait dû être levée:{mon_faux_domino}") 
    except:
        assert True
    try:
        mon_faux_domino = Domino(-1, 0)
        raise AssertionError(f"Une exception aurait dû être levée:{mon_faux_domino}") 
    except:
        assert True
    try:
        mon_faux_domino = Domino(1, 7)
        raise AssertionError(f"Une exception aurait dû être levée:{mon_faux_domino}") 
    except:
        assert True

def test_domino_inverse():
    print("Domino > inverse()")
    mon_domino = Domino(0, 5)
    print(mon_domino)
    mon_domino.inverse()
    assert mon_domino.valeur_a_gauche == 5
    assert mon_domino.valeur_a_droite == 0
    print(mon_domino)

def test_domino_score():
    print("Domino > score()")
    mon_autre_domino = Domino(1, 4)
    assert mon_autre_domino.score() == 5

def test_domino_est_compatible():
    print("Domino > est_compatible()")
    mon_domino = Domino(0, 5)
    assert mon_domino.est_compatible(4) == True
    mon_autre_domino = Domino(1, 4)
    assert mon_autre_domino.est_compatible(4) == True
    assert mon_autre_domino.est_compatible(5) == False
    assert mon_autre_domino.est_compatible(0) == True

def test_domino_equals():
    print("Domino > equals()")
    mon_domino = Domino()
    assert mon_domino == mon_domino
    assert mon_domino != Domino(0, 5)

def test_domino():
    print("Domino > START")
    test_domino_constructeur()
    test_domino_constructeur_erreur()
    test_domino_inverse()
    test_domino_score()
    test_domino_est_compatible()
    test_domino_equals()
    print("Domino > END")
    
# test_domino()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# JOUEURS
def test_joueur_constructeur():
    print("Joueur > constucteur")
    # def __init__(self, name, type="humain"):
    j1 = Joueur("Player1")
    assert j1.type == "humain"
    assert j1.name == "Player1"
    j2 = Joueur("Player2", "ordinateur")
    assert j2.name == "Player2"
    assert j2.type == "ordinateur"

def test_joueur_exception():
    print("Joueur > Exceptions")
    j1 = Joueur("Player1")
    try:
        j1.type = "ordinateur"
        raise AssertionError("La modification du type devrait déclencher une erreur")
    except:
        assert True

def test_joueur_ajouter_domino(no_joueur=1):
    print("Joueur > Ajouter Domino")
    j1 = Joueur("Player"+str(no_joueur))
    for i in range (5):
        j1.ajouter_domino(Domino())
    assert len(j1.dominos_en_main) == (i+1)
    print(j1)
    return j1


def test_joueur_retirer_domino(joueur=None):
    print("Joueur > Ajouter Domino")
    if joueur is None:
        joueur = test_joueur_ajouter_domino()
    
    pos = 0
    for i in range(len(joueur.dominos_en_main)):
        domino = joueur.dominos_en_main[pos]
        joueur.retirer_domino(pos)
        if len(joueur.dominos_en_main)> 0:
            assert joueur.dominos_en_main[pos] != domino
        else:
            # Cas où il n'y a plus de domino
            assert True
    # Tester le retrait d'un domino avec index hors liste
    joueur = test_joueur_ajouter_domino()
    pos = len(joueur.dominos_en_main) + 2
    try:
        joueur.retirer_domino(pos)
        raise AssertionError("Le retrait d'un domino d'un index > à la taille de la liste devrait lever une erreur")
    except:
        assert True

def test_joueur_maxi_double():
    print("Joueur > Maxi Double")
    j1 = Joueur("Player")
    for i in range (6):
        j1.ajouter_domino(Domino(i, i))  
        maxi = j1.maxi_double()
        assert maxi.score() == i*2

    j1 = Joueur("Player")
    maxi = j1.maxi_double()
    assert maxi is None

    j1.ajouter_domino(Domino(1,2))
    j1.ajouter_domino(Domino(2,3))
    j1.ajouter_domino(Domino(3,4))
    maxi = j1.maxi_double()
    assert maxi is None

    j1.ajouter_domino(Domino(4,4))
    maxi = j1.maxi_double()
    assert maxi.score() == 8


def test_joueur():
    print("Joueur > START")
    test_joueur_constructeur()
    test_joueur_exception()
    j1 = test_joueur_ajouter_domino()
    test_joueur_retirer_domino()
    test_joueur_maxi_double()
    print("Joueur > END")

# test_joueur()
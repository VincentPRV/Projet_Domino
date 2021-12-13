import beans_domino as beans
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
        for i in range(0, 6):
            j = 0
            for j in range (0, i):
                jeux_complet.append(beans.Domino(j, i))
        return jeux_complet
    

    def __init__(self):
        self._joueurs = []
        self._pioche = None
        self._plateau = []

    def ajouter_joueur(self, joueur):
        if len(self._joueurs) < 7:
            self._joueurs.append(joueur)
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
   

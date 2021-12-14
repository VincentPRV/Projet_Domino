from controler_domino import *
from beans_domino import *

# Gérer la création des joueurs
# Affichage plateau avant jeu
# Gérer les tours

def play():

    reponse = ""
    i = 0
    while reponse != "exit":
        i += 1
        partie = Partie("Partie "+str(i))
        # Ajout des joueurs
        joueur_name = ""
        while joueur_name != "stop":
            joueur_name = input("Saisissez le nom du joueur (ou stop si tous les joueurs sont enregistrés):\n")
            if joueur_name != "stop":
                partie.ajouter_joueur(joueur_name)
        
        if len(partie.joueurs)>0:
            # Initilialisation de la partie
            print(partie.partie_name, ": distribution des dominos")
            partie.distribue_dominos()
            print(partie.partie_name, ": le premier joueur est ", end="")
            joueur = partie.premier_joueur()
            print(joueur.name)
            # La partie est initialisée
            
            # Il faut poser le premier domino
            # il faut récupérer l'indice du premier joueur pour initier les tours

            

        else:
            reponse = input("Vous n'avez saisis aucun joueur, souhaitez-vous quitter le jeux ? o/n\n")
            reponse = "exit"
    



# Si un joueur n’a pas de domino qu’il puisse poser, il pioche un domino (sans le monter aux autres joueurs). S’il peut le poser, il le fait immédiatement, sinon il l’ajoute à ces dominos. Si la pioche est épuisée, le joueur passe son tour.
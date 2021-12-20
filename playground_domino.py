from controler_domino import *
from beans_domino import *

# Gérer la création des joueurs
# Affichage plateau avant jeu
# Gérer les toursV

def tour_joueur(partie, joueur):
    # Boucle des tours pour 1 joueur (erreur de saisie et pioche)
    pioche = False
    continuer_a_jouer = True
    continuer_tour = True
    
    while continuer_tour:
        error = False
        # On affiche le plateau
        partie.affiche_plateau()
        # on affiche les dominos du joueur courant
        joueur.affiche_main_et_positions()
        jeu = input(f"{joueur.name} quel domino voulez-vous déposer ? position OU auto OU aucun OU exit:\n")
        # Le joueur ne peut pas déposer un domino
        # on passe au joueur suivant, donc on sort de la boucle
        if jeu is None or len(jeu) == 0:
            print("Merci de corriger votre saisie")
        else:
            jeu = jeu.lower()
            if jeu == "exit":
                continuer_tour = False
                continuer_a_jouer = False
                break
            elif "auto" in jeu:
                return partie.tour_auto(joueur)
            elif "aucun" in jeu and pioche:
                continuer_tour = False
                break
            elif "aucun" in jeu and not pioche:
                # on pioche automatiquement
                domino = partie.pioche()
                if domino is not None:
                    joueur.ajouter_domino(domino)
                pioche = True
            else:
                
                try:
                    pos = int(jeu)
                    if pos < len(joueur.dominos_en_main):
                        domino = joueur.dominos_en_main[pos]
                        # il faut vérifier que le domino est compatible
                        cote = input(f"{joueur.name} de quel côté voulez-vous deposer votre domino ? (g ou d ou ig ou id)\n")
                        if cote is not None:
                            cote = cote.lower()
                            if "i" in cote :
                                domino.inverse()
                            if "g" in cote:
                                if partie.deposer_domino_a_gauche(joueur, domino):
                                    # On peut passer au joueur suivant
                                    continuer_tour = False
                                    # Si le joueur n'a plus de domino, il a gagné
                                    return len(joueur.dominos_en_main) > 0
                                else:
                                    print(f"Impossible de déposer le domino tel que : {domino} <> {partie.domino_a_gauche()}")
                                    error = True
                            elif "d" in cote:
                                if partie.deposer_domino_a_droite(joueur, domino):
                                    # On peut passer au joueur suivant
                                    continuer_tour = False
                                    # Si le joueur n'a plus de domino, il a gagné
                                    return len(joueur.dominos_en_main) > 0
                                else:
                                    print(f"Impossible de déposer le domino tel que : {partie.domino_a_droite()} <> {domino}")
                                    error = True
                            else:
                                continuer_tour = False
                                return len(joueur.dominos_en_main) > 0
                        else:
                            error = True
                    else:
                        error = True
                except:
                    error = True
        if error : print(f"Merci de vérifier votre saisie (position entre 0 et {len(joueur.dominos_en_main)})")
    return continuer_a_jouer


def play():

    reponse = " "
    i = 0
    while reponse not in "exit":
        i += 1
        partie = Partie("Partie "+str(i))
        # Ajout des joueurs
        joueur_name = "Player"
        while joueur_name not in "stop" and joueur_name not in "exit":
            joueur_name = input("Saisissez le nom du joueur (ou exit ou stop):")
            if joueur_name not in "stop" and joueur_name not in "exit":
                partie.ajouter_joueur(joueur_name)
            else:
                break
        
        if joueur_name in "exit":
            reponse = "exit"
            break
        elif len(partie.joueurs) == 1:
            partie.ajouter_ordinateur()
        
        if len(partie.joueurs)>1:
            # Initilialisation de la partie
            print(partie.partie_name, ": distribution des dominos")
            partie.distribue_dominos()
            print(partie.partie_name, ": le premier joueur est ", end="")
            # Il faut poser le premier domino
            # il faut récupérer l'indice du premier joueur pour initier les tours
            joueur, premier_domino = partie.premier_joueur()
            print(joueur.name)
            # on affiche les dominos du 1er joueur
            print(joueur)
            if partie.deposer_premier_domino(joueur, premier_domino):
                # La partie est initialisée
                continuer_a_jouer = True
                # Boucle des tours joueurs
                while continuer_a_jouer:
                    # Boucle des tours pour 1 joueur (erreur de saisie et pioche)
                    joueur = partie.joueur_suivant()
                    if "ordinateur" in joueur.type:
                        continuer_a_jouer = partie.tour_auto(joueur)
                    else:
                        continuer_a_jouer = tour_joueur(partie, joueur)
                
                print("---------------------- GAME OVER ----------------------")
                partie.affiche_classement()
                print("-------------------------------------------------------")
                reponse = input("Souhaitez-vous jouer une nouvelle partie ?(o/n):\n")
                if "n" in reponse:
                    reponse = "exit"
            else:
                print("Erreur lors de l'ajout du premier Domino, reinitialisation de la partie")
        else:
            reponse = input("Vous n'avez saisis aucun joueur, souhaitez-vous quitter le jeux ? o/n\n")
            if "o" in reponse:
                reponse = "exit"
                break
    

play()
# Si un joueur n’a pas de domino qu’il puisse poser, 
# il pioche un domino (sans le montrer aux autres joueurs). 
# S’il peut le poser, il le fait immédiatement, sinon il l’ajoute à ces dominos. 
# Si la pioche est épuisée, le joueur passe son tour.

# TODO :
# - Corriger le bug de l'ordinateur qui gagne
# - Traiter le cas du jeux bloqué => aucun joueur ne peut poser de domino et pioche vide
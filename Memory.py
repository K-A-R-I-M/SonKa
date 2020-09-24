import os
"""

var pour tout SONKA

"""

dir_audio = "audio"
dir_sauvegarde_playlist = "memoire_playlist"
dos_memoire_touche = "memoire_touche"

fichier_touche_next = "touche_next.ka"
fichier_touche_pause = "touche_play_pause.ka"

trait = "__________________________________________________________"
trait_2 = "----------------------------------------------------------"

chemin_cour = os.path.abspath(os.getcwd())

touches_commande = {}





"""

    default var

"""


default_next = "1"
default_play_pause = "2"

with os.scandir("./"+dos_memoire_touche) as fichiers:
    for fichier in fichiers:

        if fichier.name == fichier_touche_next:
            with open("./"+dos_memoire_touche+"/"+fichier.name, "r") as f:
                i = 0
                for ligne in  f.readlines():
                    if i == 0:
                        default_next = str(ligne[0])

        if fichier.name == fichier_touche_pause:
            with open("./"+dos_memoire_touche+"/"+fichier.name, "r") as f:
                i = 0
                for ligne in f.readlines():
                    if i == 0:
                        default_play_pause = str(ligne[0])

touches_commande["Pause"] = str(default_play_pause)
touches_commande["Next"] = str(default_next)




"""

fonction pour tout SONKA

"""

def sauve_ecrase(chemin, fichier, cont):
    with open(chemin+fichier, "w") as fichier:
        fichier.write(cont)

"""

fonction important

"""
def setDefaultNext(c:str):
    global default_next

    default_next = c
    ch = "./"+dos_memoire_touche+"/"
    sauve_ecrase(ch, fichier_touche_next, c)
    touches_commande["Next"] = str(default_next)

def setDefaultPause(c:str):
    global default_play_pause

    default_play_pause = c
    ch = "./" + dos_memoire_touche + "/"
    sauve_ecrase(ch, fichier_touche_pause, c)
    touches_commande["Pause"] = str(default_play_pause)


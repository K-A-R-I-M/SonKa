from recherche_youtube import RechercheLienYoutube
import os
from os import system
from LecteurAudio import LecteurAudio
from time import sleep
from PlaylistKa import PlaylistKa
from ContPlaylistKa import ContPlaylistKa
from AudioKa import AudioKa

import keyboard

from playlist_youtube import playliste_youtube
import Memory as memory


prog_etat = True
chercheur = RechercheLienYoutube()
conteneur_playlist = None
lecteur = None
dossiers = [PlaylistKa.memoire, LecteurAudio.dos_telechargement, memory.dos_memoire_touche]
detection_commande_th = None
version = "3.0"
titre_fenetre = "SonKa "+version+"____ by K-A-R-I-M"


"""--------fontions utiles-------------"""


def net_titre(txt: str):
	titre = " ".join(txt.split())
	return titre


def aff_encad(txt):
	print(memory.trait)
	print(txt)
	print(memory.trait)

def suppr_a_partir(txt, c):
	tmp = ""
	for caractere in txt:
		if caractere == c:
			return tmp
		tmp += caractere
	return tmp

def clear():
	print('\033c')

"""--------------------------------INITIALISATION------------------------------------"""
"""----------------initialisation de la memoire--------------------"""
def memoire_init():
	# verification et/ou creation des dossiers necessaire au bon fonctionnement du prog
	for dos in dossiers:
		doc_tele_etat = False
		with os.scandir("./") as fichiers:
			for fichier in fichiers:
				if fichier.name == dos:
					doc_tele_etat = True
		if doc_tele_etat == False:
			os.mkdir(dos)
"""----------------initialisation de la memoire--------------------"""
def conteneur_playlist_init():
	global conteneur_playlist
	conteneur_playlist = ContPlaylistKa()

	with os.scandir(dossiers[0]) as fichiers:
		for fichier in fichiers:
			chemin = "./"+dossiers[0]+"/"+fichier.name

			with open(chemin, "r") as f:

				playlist_recup_sauv = PlaylistKa(suppr_a_partir(fichier.name, "."))

				for audio in f.readlines():
					audio = AudioKa.fromJson(audio)
					playlist_recup_sauv.ajout(audio)
			print("playlist recuperer")
			conteneur_playlist.ajout(playlist_recup_sauv)

def detection_commande_th_init():
	global detection_commande_th
	trad_commande()


"""----------------detection et trad touche du clavier--------------------"""
def trad_commande():
	keyboard.add_hotkey(str(memory.default_play_pause), pause_hotkey)
	keyboard.add_hotkey(str(memory.default_next), next_hotkey)
def pause_hotkey():
	global lecteur
	if lecteur != None:
		lecteur.pause()
	else:
		print("action impossible lecteur inexistant")
def next_hotkey():
	global lecteur
	if lecteur != None:
		lecteur.next()
	else:
		print("action impossible lecteur inexistant")

"""----------------main--------------------"""
def main():

	global prog_etat, lecteur, detection_commande_th, titre_fenetre

	#initialisation
	system("title "+titre_fenetre)
	memoire_init()
	conteneur_playlist_init()
	detection_commande_th_init()


	#taille fenetre
	os.system("mode con cols=60 lines=20")

	#presentation
	presentation_demarrage()


	while prog_etat:
		try:

			clear()

			menuPrincipal = memory.trait_2 + "\n"
			menuPrincipal += " 1 - jouer un audio\n"
			menuPrincipal += " 2 - pause/reprendre l'audio\n"
			menuPrincipal += " 3 - next audio\n"
			menuPrincipal += " 4 - afficher le file de lecture\n"
			menuPrincipal += memory.trait_2 + "\n"
			menuPrincipal += " 5 - menu playlist\n"
			menuPrincipal += memory.trait_2 + "\n"
			menuPrincipal += " 6 - arreter/redemarrer le systeme de lecture audio\n"
			menuPrincipal += " 7 - credits \n"
			menuPrincipal += " 8 - parametre\n"
			menuPrincipal += memory.trait_2 + "\n"
			menuPrincipal += " 1234 - sortir \n"
			menuPrincipal += memory.trait_2

			aff_encad(menuPrincipal)

			choix = int(input())
			if (choix == 1):

				titre_rech = input('titre : \n')

				if lecteur == None:
					lecteur = LecteurAudio()
					audio_moment = PlaylistKa(titre_rech, momentaner=True)
					audio_moment.lancer(lecteur)

				else:
					audio_moment = PlaylistKa(titre_rech, momentaner=True)
					audio_moment.lancer(lecteur)

				lecteur.add_launch()

			elif (choix == 2):
				if lecteur != None:
					lecteur.pause()
				else:
					print("pause/resume impossible pas de lecteur\n")


			elif (choix == 3):
				if lecteur != None:
					lecteur.next()
				else:
					print("next impossible pas de lecteur\n")


			elif (choix == 4):
				if lecteur != None:
					print(lecteur)
				else:
					aff_encad(" Depuis le lancement aucun audio n'a été lancer\n cela va etre dificile de vous faire une liste de tout ce qui compose le vide mais bon...\n hummm....\n bah rien en faite\n lol\n ")
				input("Appuyer sur entree pour continuer !!")

			elif (choix == 5):
				menu_playlist()


			elif (choix == 6):
				if lecteur != None:
					lecteur.eteindre()
					lecteur = None
					print(" arret \n")
				else:
					print("arret impossible \n")


			elif (choix == 7):
				credit_SonKa()

			elif (choix == 8):
				parametre()

			elif (choix == 1234):
				if lecteur != None:
					lecteur.eteindre()
					lecteur = None

				print("Au Revoir")
				prog_etat = False

			else:
				aff_encad("Saisie incorrecte")


		except Exception as e:
			print("Erreur : ")
			print(e)
		sleep(1)
"""--------------fonction utile pour le menu de playlist------------------"""
def aff_tout_playlist():
	nb = 0
	if conteneur_playlist != None:
		print(memory.trait)
		for playlist in conteneur_playlist.getListPlaylist():
			print(str(nb)+" - " + str(playlist.getTitre()))
			nb += 1
		print(memory.trait)

	else:
		print("aucune playlist existante")

def choix_playlist():
	try:
		aff_tout_playlist()
		if conteneur_playlist != None:
			choix = int(input())
			if choix < len(conteneur_playlist.getListPlaylist()) and choix >= 0:
				return conteneur_playlist.getPlaylist(choix)
			else:
				print("playlist inexistante")
				return None
		else:
			return None

	except Exception as e:
		print("ERREUR :")
		print(e)
		return None

"""----------------------menu playlist------------------------"""
def menu_playlist():
	global conteneur_playlist, lecteur
	while True:
		try:

			clear()

			aff_encad("			Menu Playlist			")

			msgPresentationChoix = memory.trait_2 + "\n"
			msgPresentationChoix += " 1 - crée une playlist\n"
			msgPresentationChoix += memory.trait_2+"\n"
			msgPresentationChoix += " 2 - afficher tout les playlists existantes\n"
			msgPresentationChoix += " 3 - afficher une playlist\n"
			msgPresentationChoix += memory.trait_2+"\n"
			msgPresentationChoix += " 4 - gerer une playlist\n"
			msgPresentationChoix += " 5 - jouer une playlist\n"
			msgPresentationChoix += " 6 - importer une playliste youtube\n"
			msgPresentationChoix += memory.trait_2+"\n"
			msgPresentationChoix += " 7 - skip la playlist courante\n"
			msgPresentationChoix += memory.trait_2+"\n"
			msgPresentationChoix += " 123 - quitter\n"
			msgPresentationChoix += memory.trait_2

			aff_encad(msgPresentationChoix)

			choix = int(input())


			if(choix == 1):

				titre_nv_playlist = input("Nom nv playlist : ")
				nv_playlist = PlaylistKa(titre_nv_playlist)

				if conteneur_playlist != None:
					conteneur_playlist.ajout(nv_playlist)

				else:
					conteneur_playlist = ContPlaylistKa()
					conteneur_playlist.ajout(nv_playlist)

			elif choix == 2:
				aff_tout_playlist()

			elif choix == 3:
				playlist_aff = choix_playlist()
				if playlist_aff != None:
					aff_encad(playlist_aff)

			elif choix == 4:
				playlist = choix_playlist()
				if playlist != None:
					menu_gestion_playlist(playlist)

			elif choix == 5:
				playlist_joue = choix_playlist()

				if playlist_joue != None:

					if lecteur != None:
						playlist_joue.lancer(lecteur)
					else:
						lecteur = LecteurAudio()
						playlist_joue.lancer(lecteur)

				else:
					print("impossible de jouer cet playlist")

			elif choix == 6:
				titre = input("nom de la playliste : ")
				url = input("url de la playliste : ")
				nv_playlist_yt = playliste_youtube(titre_playlist=titre, url=url)

				if nv_playlist_yt != None:
					if conteneur_playlist != None:
						conteneur_playlist.ajout(nv_playlist_yt)

					else:
						conteneur_playlist = ContPlaylistKa()
						conteneur_playlist.ajout(nv_playlist_yt)
				else:
					print("Lien defectueux")

			elif choix == 7:
				lecteur.next_playlist()

			elif choix == 123:
				break

			else:
				aff_encad("Saisie incorrecte")

		except Exception as e:
			print("Erreur : ")
			print(e)

		sleep(1)
"""--------------------fonction utiles pour menu gestion playlist-----------------------"""
def choix_audio(playlist:PlaylistKa):
	aff_encad(playlist)
	try:
		choix = int(input())
		if choix < len(playlist.getAudios()) and choix >= 0:
			return playlist.getAudios()[choix]
		else:
			return None

	except Exception as e:
		print("Erreur : ")
		print(e)

		return None

"""----------------------menu gestion playlist------------------------"""
def menu_gestion_playlist(playlist:PlaylistKa):
	while True:
		try:

			clear()

			aff_encad("		Menu Gestion d'une Playlist		\n		"+playlist.getTitre())

			msgPresentationChoix = memory.trait_2 + "\n"
			msgPresentationChoix += " 1 - ajouter un audio à la playlist\n"
			msgPresentationChoix += " 2 - supprimer un audio de la playlist\n"
			msgPresentationChoix += memory.trait_2 + "\n"
			msgPresentationChoix += " 3 - afficher la playlist\n"
			msgPresentationChoix += memory.trait_2 + "\n"
			msgPresentationChoix += " 4 - sauvegarder la playlist\n"
			msgPresentationChoix += memory.trait_2 + "\n"
			msgPresentationChoix += " 123 - quitter\n"
			msgPresentationChoix += memory.trait_2

			aff_encad(msgPresentationChoix)

			choix = int(input())

			if(choix == 1):

				playlist_audio_ajt = playlist

				if playlist_audio_ajt != None:
					titre_audio_chercher = input("nom de l'audio : ")
					titre_audio_ajt, url_audio_ajt = chercheur.recherche(titre_audio_chercher)
					titre_audio_ajt = net_titre(titre_audio_ajt)
					audio_ajt = AudioKa(titre_audio_ajt, url_audio_ajt)
					playlist_audio_ajt.ajout(audio_ajt)

			elif(choix == 2):
				playlist_audio_suppr = playlist

				if playlist_audio_suppr != None:
					audio_suppr = choix_audio(playlist_audio_suppr)
					playlist_audio_suppr.suppression(audio_suppr)

			elif choix == 3:
				if playlist != None:
					aff_encad(playlist)

			elif choix == 4:
				if playlist != None:
					playlist.sauvegarder()

			elif choix == 123:
				break

			else:
				aff_encad("Saisie incorrecte")

		except Exception as e:
			print("Erreur :")
			print(e)
		sleep(1)
"""----------------------Credit------------------------"""
def credit_SonKa():
	global version
	clear()
	print(memory.trait)
	aff_encad("Inventé et developé par KARIM aka K-A-R-I-M \nSonKa V"+version)
	print(memory.trait)
	sleep(2)
"""----------------------presentation demarrage------------------------"""
def presentation_demarrage():
	global version
	sleep(1)
	clear()
	messageBvn = "\nBienvenue dans SonKa V"+version
	print(messageBvn)
	sleep(1)
	clear()

	nom_styler = "\n"

	with open("nom/nom.ka", "r") as f:
		for ligne in f.readlines():
			nom_styler += ligne
	print(nom_styler)
	sleep(2)
"""----------------------menu parametre------------------------"""
def parametre():
	while True:
		try:

			clear()
			aff_encad("		Parametre		")

			msgPresentationChoix = memory.trait_2 + "\n"
			msgPresentationChoix += " 1 - commande\n"
			msgPresentationChoix += memory.trait_2 + "\n"
			msgPresentationChoix += " 123 - quitter\n"
			msgPresentationChoix += memory.trait_2

			aff_encad(msgPresentationChoix)

			choix = int(input())

			if(choix == 1):
				commande()
			elif(choix == 123):
				break
			else:
				aff_encad("Saisie incorrecte")

		except Exception as e:
			print("Erreur :")
			print(e)
		sleep(1)
"""----------------------methode du menu parametre------------------------"""
#--------menu parametre commande--------
def commande():
	while True:
		try:

			clear()
			aff_encad("		Parametre Commande		")

			msgPresentationChoix = memory.trait_2 + "\n"
			msgPresentationChoix += " 1 - voir les commandes actuel\n"
			msgPresentationChoix += " 2 - changer la touche pause\n"
			msgPresentationChoix += " 3 - changer la touche next\n"
			msgPresentationChoix += memory.trait_2 + "\n"
			msgPresentationChoix += " 123 - quitter\n"
			msgPresentationChoix += memory.trait_2

			aff_encad(msgPresentationChoix)

			choix = int(input())

			if(choix == 1):
				aff_commande_touche()
			elif(choix == 2):
				change_touche_pause()
			elif (choix == 3):
				change_touche_next()
			elif(choix == 123):
				break
			else:
				aff_encad("Saisie incorrecte")

		except Exception as e:
			print("Erreur :")
			print(e)
		sleep(1)
"""----------------------methode du menu parametre commande------------------------"""
def aff_commande_touche():
	touches = memory.touches_commande
	str_aff = ""
	i = 0
	for nom, touche in touches.items():
		str_aff += str(i)+" - "+nom+" : "+touche+"\n"
		i += 1
	aff_encad(str_aff)
	input("Appuyer sur entree pour continuer !!")

def change_touche_pause():
	print("Taper sur la nouvelle touche !!")
	sleep(1)
	shortcut = keyboard.read_hotkey()
	print('Touche selectioner :', shortcut)
	memory.setDefaultPause(shortcut)

def change_touche_next():
	print("Taper sur la nouvelle touche !!")
	sleep(1)
	shortcut = keyboard.read_hotkey()
	print('\nTouche selectioner :', shortcut)
	memory.setDefaultNext(shortcut)


main()
#partie_graphique()


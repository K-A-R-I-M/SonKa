import youtube_dl
from recherche_youtube import RechercheLienYoutube
import os
import sys
from LecteurAudio import LecteurAudio
from time import sleep
from PlaylistKa import PlaylistKa
from ContPlaylistKa import ContPlaylistKa
from AudioKa import AudioKa
from pynput.keyboard import Listener
from threading import Thread
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon


prog_etat = True
chercheur = RechercheLienYoutube()
conteneur_playlist = None
lecteur = None
dossiers = [PlaylistKa.memoire, LecteurAudio.dos_telechargement]
detection_commande_th = None
app = QApplication(sys.argv)

"""--------fontions utiles-------------"""


def net_titre(txt: str):
	titre = " ".join(txt.split())
	return titre


def aff_encad(txt):
	print("-----------------------------------")
	print(txt)
	print("-----------------------------------")

def suppr_a_partir(txt, c):
	tmp = ""
	for caractere in txt:
		if caractere == c:
			return tmp
		tmp += caractere
	return tmp

def clear():
	print(chr(27) + "[2J")

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
	detection_commande_th = Thread(target=detection_clavier)
	detection_commande_th.start()

"""----------------detection et trad touche du clavier--------------------"""
def trad_commande(key):
	global lecteur
	keydata = str(key)
	if lecteur != None:
		if keydata == "Key.media_play_pause" and lecteur != None:
			lecteur.pause()
		elif keydata == "Key.media_next" and lecteur != None:
			lecteur.next()

def detection_clavier():
	global prog_etat
	with Listener(on_press=trad_commande) as l:
		while prog_etat == True:
			sleep(2)
			if prog_etat == False:
				l.stop()

		l.join()


"""----------------main--------------------"""
def main():

	global prog_etat, lecteur, detection_commande_th, app

	#initialisation
	memoire_init()
	conteneur_playlist_init()
	detection_commande_th_init()

	messageBvn = "\nBienvenue dans le lecteur youtube YlistKa(beta)"
	print(messageBvn)
	sleep(1)

	while prog_etat:
		try:

			clear()

			menuPrincipal = "----------------------------------------------\n"
			menuPrincipal += " 1 - jouer qqchose\n"
			menuPrincipal += " 2 - pause/reprendre qqchose\n"
			menuPrincipal += " 3 - next qqchose\n"
			menuPrincipal += " 4 - arreter qqchose\n"
			menuPrincipal += " 5 - menu playlist qqchose\n"
			menuPrincipal += " 6 - sortir\n"
			menuPrincipal += "----------------------------------------------\n"

			choix = int(input(menuPrincipal))

			if (choix == 1):
				titre_rech = input('titre : \n')
				if lecteur == None:
					lecteur = LecteurAudio()
					lecteur.ajt_queue(titre_rech)
					lecteur.start()
				else:
					lecteur.ajt_queue(titre_rech)

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
					lecteur.eteindre()
					lecteur = None
					print(" arret \n")
				else:
					print("arret impossible \n")

			elif (choix == 5):
				menu_playlist()

			elif (choix == 6):
				if lecteur != None:
					lecteur.eteindre()
					lecteur = None

				print("Au Revoir")
				prog_etat = False
				"""app.quit()
				sys.exit(app.exec_())"""

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
		print("--------------------------------")
		for playlist in conteneur_playlist.getListPlaylist():
			print(str(nb)+" - " + str(playlist.getTitre()))
			nb += 1
		print("--------------------------------")

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

			aff_encad("Menu Playlist")

			msgPresentationChoix = " 1 - crée une playliste\n"
			msgPresentationChoix += " 2 - afficher tout les playlists existantes\n"
			msgPresentationChoix += " 3 - affichage d'une playlist\n"
			msgPresentationChoix += " 4 - gerer une playlist\n"
			msgPresentationChoix += " 5 - jouer une playlist\n"
			msgPresentationChoix += " 6 - quitter"

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
					print(playlist_aff)

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

			else:
				break

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

			aff_encad("Menu Gestion d'une Playlist \n"+playlist.getTitre())

			msgPresentationChoix = " 1 - ajout d'audio dans la playlist\n"
			msgPresentationChoix += " 2 - suppression d'un audio dans la playlist\n"
			msgPresentationChoix += " 3 - affichage d'une playlist\n"
			msgPresentationChoix += " 4 - sauvegarder la playlist\n"
			msgPresentationChoix += " 5 - quitter"

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
					print(playlist)

			elif choix == 4:
				if playlist != None:
					playlist.sauvegarder()

			else:
				break

		except Exception as e:
			print("Erreur :")
			print(e)
		sleep(1)

main()
#partie_graphique()


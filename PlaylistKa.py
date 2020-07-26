from AudioKa import AudioKa
from time import sleep
import json
from json import dump
import os

class PlaylistKa():
    memoire = "memoire_playlist"

    def __init__(self, titre):
        self._titre = titre
        self._audios = []


    def ajout(self, audio:AudioKa):
        self._audios.append(audio)
        print("ajout réussi")

    def suppression(self, audio_suppr:AudioKa):

        succes = False

        for audio in self._audios:
            if audio == audio_suppr:
                self._audios.remove(audio)
                succes = True

        if succes:
            print("suppression réussi")
        else:
            print("ERREUR : suppression impossible audio inexistant dans la playlist")

    def estVide(self):
        if self._audios == []:
            return True
        else:
            return False

    def getTitre(self):
        return self._titre

    def getAudios(self):
        return self._audios

    def lancer(self, lecteur=None):
        if lecteur != None:
            if self.estVide() == False:
                nb = lecteur.getChercheur().getNbRecheche() + 1
                for audio in self._audios:

                    titre = audio.getTitre()
                    url = audio.getUrl()


                    lecteur._queue.append(titre)

                    lecteur._telecharge_musique(url, nb=nb)

                    print("ajout a la file de lecture")


                    lecteur.getChercheur().addNbRecheche()
                    nb += 1

                    if lecteur.getChercheur().getNbRecheche() == 1:
                        lecteur.start()

            else:
                print("playlist vide")

        else:
            print("lecteur inexistant")
        sleep(1)

    def sauvegarder(self):
        print("Lancement de la Sauvegarde...")
        sleep(1)
        playlist_actu = self
        memoire_playlist_actu = "./"+PlaylistKa.memoire+"/"+self._titre+".json"
        with open(memoire_playlist_actu, "w") as f:
            for audio in self._audios:
                dump(audio.toJson(), f)
                f.write("\n")

        print("Sauvegarde réussite !")
        sleep(1)


    @staticmethod
    def AudioKaFromJson(playlist):
        audios_traité = []
        audios = playlist.getAudios()
        for audio in audios:
            audio = AudioKa.fromJson(str(audio))
            audios_traité.append(audio)
        return audios_traité



    def __str__(self):
        if self.estVide() == False:
            aff = ""
            nb = 0
            for audio in self._audios:
                titre = audio.getTitre()
                aff += str(nb)+" - "+titre+"\n"
                nb += 1
            return aff
        else:
            return "playlist vide"

from AudioKa import AudioKa
from time import sleep
import json
from json import dump
import os
import vlc
from recherche_youtube import RechercheLienYoutube
from LecteurAudio import LecteurAudio
import Memory as memory


class PlaylistKa():
    memoire = memory.dir_sauvegarde_playlist

    def __init__(self, titre, momentaner=False):
        self._titre = titre
        self._audios = []
        self._momentaner = momentaner


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

    """--------fonction utile--------"""
    def _se_termine_par(self, txt, mot):
        succes = True
        if (len(txt) < len(mot)):
            succes = False
        else:
            i = len(mot) - 1
            j = len(txt) - 1
            while (i > 0):
                if txt[j] != mot[i]:
                    return False
                j -= 1
                i -= 1
        return succes

    def _net_titre(self, txt: str):
        titre = " ".join(txt.split())
        return titre
    """---------------------------"""

    def lancer(self, lecteur:LecteurAudio=None):
        if self._momentaner == False:
            if lecteur != None:
                if self.estVide() == False:

                    lecteur.add_launch(len(self._audios))

                    for audio in self._audios:

                        titre = audio.getTitre()
                        url = audio.getUrl()


                        lecteur.ajt_queue(titre)

                        #cas ou tout va bien
                        try:

                            lecteur._telecharge_musique(url)

                        #audio n'est plus dispo sur youtube
                        except Exception as e:

                            if self._se_termine_par(str(e), "YouTube said: Unable to extract video data"):
                                lecteur.pause()
                                # audio erreur
                                player = vlc.MediaPlayer("./SonKa_sound/erreur_audio_non_telecharger.mp3")
                                player.play()
                                sleep(3)

                                # recherche sur youtube de nv lien et telechargement
                                recherche_rafrai = RechercheLienYoutube()
                                titre_rafrai, url_rafrai = recherche_rafrai.recherche(titre)
                                lecteur.pause()

                                titre_rafrai = self._net_titre(titre_rafrai)

                                audio.setUrl(url_rafrai)
                                audio.setTitre(titre_rafrai)

                                print("rafrachissement de votre playlist")
                                lecteur._telecharge_musique(url_rafrai)

                                if self._est_sauvegarder():
                                    self.sauvegarder()


                        print("ajout a la file de lecture")


                        lecteur.getChercheur().addNbRecheche()

                        if lecteur.getChercheur().getNbRecheche() == 1:
                            lecteur.start()

                else:
                    print("playlist vide")

            else:
                print("lecteur inexistant")
            sleep(1)
        else:
            self.__lancer_moment(lecteur)

    def __lancer_moment(self, lecteur:LecteurAudio):
        if lecteur != None:
            try:
                lecteur.add_launch(1)

                chercheur = lecteur.getChercheur()

                result = chercheur.recherche(self._titre)

                url = result[1]
                titre = self._net_titre(result[0])
                print(url)
                print(titre)
                self._audios.append(AudioKa(titre, url))
                lecteur.ajt_queue(titre)

                lecteur._telecharge_musique(url)

                lecteur.getChercheur().addNbRecheche()

                if lecteur.getChercheur().getNbRecheche() == 1:
                    lecteur.start()

            except Exception as e:
                print("ERREUR : ")
                print(e)
        else:
            print("ERREUR : Lecteur indisponible")



    def _verif_dos(self):
        try:
            # verification du dossier et/ou changement de dossier
            if self._se_termine_par(os.getcwd(), LecteurAudio.dos_telechargement) == True:
                os.chdir("..")
        except Exception as e:
            print("ERREUR :")
            print(e)

    def _est_sauvegarder(self):
        # verification du dossier de localisation
        self._verif_dos()

        with os.scandir("./"+PlaylistKa.memoire+"/") as fichiers:
            for fichier  in fichiers:
                if fichier.name == str(self._titre)+".json":
                    return True
        return False

    def sauvegarder(self):
        #verification du dossier de localisation
        self._verif_dos()

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


    def _aff_audio(self, nb_audio:int, txt:str=""):
        titre = self._audios[nb_audio].getTitre()
        return str(nb_audio) + " - " + titre + txt

    def __str__(self):
        if self.estVide() == False:
            aff = "\n"
            for nb_audio in range(len(self._audios)):
                if nb_audio != len(self._audios):
                    aff += self._aff_audio(nb_audio, "\n")
                else:
                    aff += self._aff_audio(nb_audio)
            return aff
        else:
            return "playlist vide"

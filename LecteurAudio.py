import vlc
from threading import Thread
from recherche_youtube import RechercheLienYoutube
import os
import youtube_dl
from time import sleep
from win10toast import ToastNotifier
import Memory as memory


class LecteurAudio(Thread):
    dos_telechargement = memory.dir_audio

    def __init__(self):
        super().__init__()

        self._etat = True
        self._chercheur = RechercheLienYoutube()
        self._nb_courant_mus = 1
        self._queue = []
        self._play_obj = None
        #demarrage
        self._demarrage()
        self._notif = ToastNotifier()
        self._pause = False
        self._cour_playlist = []
        self._nb_cour_playlist_music = None

    def run(self):
        super().run()
        while self._etat :
            #verification d'existance d'un audio dans la queue
            if self._nb_courant_mus <= self._chercheur.getNbRecheche():
                self._play_obj = self.joue()

                #passage automatique au prohcain audio
                if self._play_obj != None:
                    sleep(3)
                    while self._play_obj != None:

                        try:
                            if self._play_obj.get_length() - self._play_obj.get_time() < 1000:
                                self._play_obj.stop()
                                self._play_obj = None
                                break
                        except Exception as e:
                            print("Ya eu un probleme mais tkt")

                        sleep(2)
                    self._nb_courant_mus += 1

            #en attante de nv audio
            else:
                sleep(2)
                #print("je dort y a plus de taff")

    '''---------------------Demmarrage----------------------'''
    def _demarrage(self):
        #verif le dossier de la localisation et dep si necessaire
        self._verif_dos()

        #nettoyage
        self._nettoyage_fichier_music()


    def _nettoyage_fichier_music(self):
        with os.scandir("./") as fichiers:
            for fichier in fichiers:
                if self._se_termine_par(fichier.name, ".wav") or self._se_termine_par(fichier.name, ".webm") or self._se_termine_par(fichier.name, ".mp3"):
                    os.remove(fichier.name)
                    print("ancien music supprimer")
        print("fin du nettoyage des fichiers audios")

    '''---------------------modif de chaine de caractère----------------------'''

    def _net_titre(self, txt: str):
        titre = " ".join(txt.split())
        return titre

    def _commence_par(self, txt, mot):
        succes = True
        if (len(txt) < len(mot)):
            succes = False
        else:
            for i in range(len(mot)):
                if txt[i] != mot[i]:
                    succes = False
        return succes

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

    '''---------------------outil d'affichage----------------------'''
    def _aff_encad(self, txt):
        print(memory.trait)
        print(txt)
        print(memory.trait)


    '''---------------------Telechargement----------------------'''

    # fonction qui telecharge
    def _telecharge_musique(self, url, nb):


        self._verif_dos()

        # telecharge musique
        ydl_opts = {
            'audioformat': "mp3",
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])


        with os.scandir("./") as fichiers:
            for fichier in fichiers:

                if self._se_termine_par(fichier.name, ".mp3") and self._commence_par(fichier.name, "song_") == False:
                    print("trouver")
                    os.rename(fichier, 'song_' + str(nb) + '_nb.mp3')
                    break



    # fonction s'occupe de tout ce qui est en rapport avec le telechargement
    def _telechargeur_automatique(self, txt: str):

        result = self._chercheur.recherche(txt)

        nb = self._chercheur.getNbRecheche()

        url = result[1]
        titre = self._net_titre(result[0])
        print(url)
        print(titre)
        self._queue.append(titre)

        self._telecharge_musique(url, nb=nb)

    '''---------------------Gestion des fichiers audio----------------------'''
    def _verif_dos(self):
        try:
            # verification du dossier et/ou changement de dossier
            if self._se_termine_par(os.getcwd(), LecteurAudio.dos_telechargement) == False:
                os.chdir("./" + LecteurAudio.dos_telechargement)
        except Exception as e:
            print("ERREUR :")
            print(e)


    def _supppr_ancien_audio(self):
        self._verif_dos()
        nb = self._nb_courant_mus - 1

        filename = 'song_' + str(nb) + '_nb.mp3'
        os.remove("./"+filename)

    '''---------------------Gestion audio----------------------'''

    def joue(self):

        nb = self._nb_courant_mus



        if nb != 1:
            self._supppr_ancien_audio()
            self.suppr_queue()



        filename = 'song_' + str(nb) + '_nb.mp3'
        player = vlc.MediaPlayer(filename)
        player.play()

        self._aff_encad("Lancement de : " + self._queue[0])

        self._notif.show_toast("SonKa", self._queue[0], duration=3)


        return player

    def pause(self):
        if self._pause == True:


            player = vlc.MediaPlayer("./SonKa_sound/play.wav")
            player.play()

            sleep(0.2)


        if self._play_obj != None:
            self._play_obj.pause()


        if  self._pause == False:

            player = vlc.MediaPlayer("./SonKa_sound/pause.wav")
            player.play()


        if self._pause == False:
            self._pause = True
        else:
            self._pause = False




    def next(self):
        if self._play_obj != None and self._nb_courant_mus < self._chercheur.getNbRecheche():
            self._play_obj.stop()
            self._play_obj = None
            print("next")
        else:
            if self._play_obj != None:
                self._play_obj.pause()

                player = vlc.MediaPlayer("./SonKa_sound/error_next.wav")
                player.play()

                sleep(0.5)
                self._play_obj.pause()
            print("next impossible")

    def next_playlist(self):
        print("pas encore dispo car refonte total necessaire")
        """if self._nb_cour_playlist_music == None:
            self._nb_cour_playlist_music = self._cour_playlist[0]
        nb = self._nb_cour_playlist_music
        if nb == 1:
            self.next()
        else:
            for i in range(nb):
                if i != 0:
                    self._verif_dos()
                    with os.scandir("./") as fichiers:
                        for fichier in fichiers:
                            if fichier.name == 'song_' + str(i+self._nb_courant_mus) + '_nb.mp3':
                                print(fichier.name)
                                sleep(3)                     
        self._nb_courant_mus += nb
        next()
        
        self._cour_playlist.pop(0)
        self._nb_cour_playlist_music = self._cour_playlist[0]"""

    '''---------------------Gestion Queue----------------------'''

    def ajt_queue(self, txt: str):
        self._telechargeur_automatique(txt)
        print("ajout a la file de lecture")

    def suppr_queue(self):
        self._queue.pop(0)

    '''---------------------Arret----------------------'''
    def eteindre(self):
        if self._play_obj != None:
            self._play_obj.stop()
            self._play_obj = None
        self._etat = False

        #nettoyage
        self._nettoyage_fichier_music()

    """---------------------Getters------------------------"""

    def getChercheur(self):
        return self._chercheur

    def add_launch(self, nb=1):
        self._cour_playlist.append(nb)

    def __str__(self):
        txt = ""
        if len(self._queue) == 0:
            txt = " la file de lecture est vide ! "
        else:
            for nb_audio_titre in range(len(self._queue)):
                if nb_audio_titre != len(self._queue) - 1:
                    txt += str(nb_audio_titre) +" - "+self._queue[nb_audio_titre]+"\n"
                else:
                    txt += str(nb_audio_titre) +" - "+self._queue[nb_audio_titre]
        return txt


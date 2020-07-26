from PlaylistKa import PlaylistKa

class ContPlaylistKa():

    def __init__(self):
        self._liste_PlayListKa = []

    def ajout(self, playlistka:PlaylistKa):
        self._liste_PlayListKa.append(playlistka)
        print("ajout réussi")

    def suppression(self, titre="", nb=-1):

        titre_playlist = []

        for playlist in self._liste_PlayListKa:
            titre_playlist.append(playlist.getTitre())

        if titre in titre_playlist:
            if (nb < len(titre_playlist) and nb != -1 and self._liste_PlayListKa[nb].getTitre == titre):
                self._liste_PlayListKa.pop(nb)
                print("suppression réussi")

            else:
                nb = self._liste_PlayListKa.index(titre)
                self._liste_PlayListKa.pop(nb)
                print("suppression réussi")

        elif (nb < len(self._liste_PlayListKa) and nb != -1):
            self._liste_PlayListKa.pop(nb)
            print("suppression réussi")

        else:
            print("ERREUR : suppression impossible playlist inexistant dans la playlist")

    def getPlaylist(self, i):
        return self._liste_PlayListKa[i]

    def getListPlaylist(self):
        return self._liste_PlayListKa

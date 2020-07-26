import json

class AudioKa():
    def __init__(self, _titre, _url):
        self._titre = _titre
        self._url = _url

    def getTitre(self):
        return self._titre

    def getUrl(self):
        return self._url

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


    @staticmethod
    def fromJson(json_string):
        json_dict = json.loads(json_string)
        json_dict = json.loads(json_dict)
        return AudioKa(**json_dict)
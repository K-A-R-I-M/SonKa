import asyncio
from pyppeteer import launch
from time import sleep

class RechercheLienYoutube():

    def __init__(self):
        self.nb_recherche = 0

    async def recherche_lien(self, url):
        browser = await launch()
        page = await browser.newPage()

        await page.goto(url)

        tag = 'h3 > a'

        element = await page.querySelector(tag)
        title = await page.evaluate('(element) => element.textContent', element)


        sleep(1)
        await page.click(tag)
        url_page = page.url

        await browser.close()


        return title, url_page



    def _formatClair(self, txt):
        #rendre compatible le texte avec le lien youtube de recherche
        xtx = ""
        cSpe = " "
        for c in range(len(txt)):
            if cSpe == txt[c]:
                xtx += "+"
            else:
                xtx += txt[c]
        return xtx

    def recherche(self, txt):
        txt = self._formatClair(txt)
        url = "https://www.youtube.com/results?search_query="+txt
        print('Ouverture de', url)

        titre, url_trouv = asyncio.get_event_loop().run_until_complete(self.recherche_lien(url))

        self.nb_recherche += 1

        return titre, url_trouv


    def getNbRecheche(self):
        return self.nb_recherche

    def addNbRecheche(self):
        self.nb_recherche += 1


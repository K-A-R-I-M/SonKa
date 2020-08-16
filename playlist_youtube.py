import asyncio
from pyppeteer import launch
from AudioKa import AudioKa
from PlaylistKa import PlaylistKa

def suppr_a_partir(txt, c):
    tmp = ""
    for caractere in txt:
        if caractere == c:
            return tmp
        tmp += caractere
    return tmp

async def playlist_youtube_translate(titre_playlist: str, url: str):
    browser = await launch()
    page = await browser.newPage()

    await page.goto(url)

    tag_div = 'div.playlist-items'
    tag_a = 'a.yt-simple-endpoint'
    tag_span = 'span'

    div_principal = await page.querySelectorAll(tag_div)

    nb = 1

    playlist = PlaylistKa(titre_playlist)

    for element in div_principal:
        liens = await element.querySelectorAll(tag_a)

        for lien in liens:
            url = await page.evaluate('(element) => element.href', lien)
            spans = await lien.querySelectorAll(tag_span)
            for span in spans:
                titre = await page.evaluate('(element) => element.title', span)

                if titre != "":
                    audio = AudioKa(_titre=titre, _url=suppr_a_partir(url, "&"))
                    playlist.ajout(audio)

    await browser.close()

    print(playlist)
    return playlist


def playliste_youtube(titre_playlist: str, url: str):
    try:
        playlist_traduite = asyncio.get_event_loop().run_until_complete(playlist_youtube_translate(titre_playlist=titre_playlist, url=url))
        if playlist_traduite.estVide():
            url_playlist_traduite = asyncio.get_event_loop().run_until_complete(playlist_youtube_translate_p2(url=url))
            if url_playlist_traduite != None:
                playlist_traduite = asyncio.get_event_loop().run_until_complete(playlist_youtube_translate(titre_playlist=titre_playlist, url=url_playlist_traduite))
            else:
                playlist_traduite = None

        return playlist_traduite

    except Exception as e:
        print("Erreur : ")
        print(e)
        return None

async def playlist_youtube_translate_p2(url: str):
    browser = await launch()
    page = await browser.newPage()

    await page.goto(url)

    tag_ytd = 'ytd-playlist-video-renderer'
    tag_div = '#content'
    tag_a = 'a'
    url = None

    div_principal = await page.querySelector(tag_ytd)


    div = await div_principal.querySelector(tag_div)
    link = await div.querySelector(tag_a)
    url = await page.evaluate('(element) => element.href', link)
    print(url)

    await browser.close()

    if url != None:
        return url
    else:
        return None
import discord as ds
from PIL import Image, ImageDraw
import os
import requests
import shutil
import discord as ds
from PIL import Image, ImageDraw
import os
import requests
import shutil
from bs4 import BeautifulSoup
from random import randint
from pixabay import Image as Imgg
import imageio

'''
Just a space to configure informations about the files
'''
TrollFacePath = "TrollFace.jpeg"
debug = True
AvatarPNGPath = "pers.png"

BLACK = (0, 0, 0, 0)

client = ds.Client()

# key for the pixbay api
API_KEY = ''
image = Imgg(API_KEY)


def rond(imgg):
    bigsize = (imgg.size[0] * 3, imgg.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(imgg.size, Image.ANTIALIAS)
    imgg.putalpha(mask)


@client.event
async def on_ready():
    activity = ds.Game(name="Help sur %help", type=3)
    await client.change_presence(status=ds.Status.idle, activity=activity)
    print('Le bot {0.user} a été connecté'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == "%help":
        await message.channel.send("**%compliment** (vous pouvez mentionner quelqu'un)\n"
                                   "**%titanic%** (mention obligatoire)\n"
                                   "**%troll** (vous pouvez mentionner quelqu'un)\n"
                                   "**%vdm** (vdm aléatoire)"
                                   "**%pileouface** ou **%pof** (pile ou face)"
                                   "**%cherche [quelque chose]** (cherche l'image que vous voulez)")

    if message.content.lower().startswith("%compliment"):
        if len(message.mentions) == 0:
            desti = str(message.author)
        elif len(message.mentions) == 1:
            desti = str(message.mentions[0])
        else:
            await message.channel.send("Vous ne pouvez pas mentionner plusieurs personnes")
            desti = str(message.author)
        img = Image.open('meme.jpg')
        draw = ImageDraw.Draw(img)
        draw.text((130, 10), "Manger des cookies", fill=BLACK)
        if len(desti) > 20:
            desti = str(desti)[0:19] + "\n" + str(desti)[19:len(str(desti))]
        else:
            desti = str(desti)
        draw.text((130, 135), 'Manger des\ncookies avec\n@' + desti, fill=BLACK)
        img.save('ima.jpg', 'jpeg')
        with open('ima.jpg', 'rb') as f:
            picture = ds.File(f)
            await message.channel.send(file=picture)
        os.remove('ima.jpg')

    if "saucisson" in message.content.lower():
        await message.channel.send("Quelqu'un a parlé de saucisson?")

    if message.content.lower().endswith("quoi"):
        await message.channel.send("feur")

    if message.content.lower().startswith("%titanic"):
        if len(message.mentions) == 1:
            aut = requests.get(
                "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(message.author),
                stream=True)
            dest = requests.get(
                "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(message.mentions[0]),
                stream=True)
            dl = [aut, dest]
            for pers in dl:
                nom = "icone" + str(dl.index(pers)) + ".png"
                if pers.status_code == 200:
                    pers.raw.decode_content = True
                    with open(nom, 'wb') as f:
                        shutil.copyfileobj(pers.raw, f)
                    print('Image sucessfully Downloaded: ', nom)
                else:
                    print('Image Couldn\'t be retreived')
            titanic = Image.open("titanic.jpg")
            img0 = Image.open("icone0.png").resize((150, 150))
            img1 = Image.open("icone1.png").resize((150, 150))
            rond(img0)
            rond(img1)
            titanic.paste(img0, (280, 10), img0)
            titanic.paste(img1, (400, 20), img1)
            titanic.save('titan.jpg', 'jpeg')
            with open('titan.jpg', 'rb') as f:
                picture = ds.File(f)
                await message.channel.send(file=picture)
            os.remove("icone0.png")
            os.remove("icone1.png")
            os.remove("titan.jpg")
        else:
            await message.channel.send("Vous devez identifier une personne !")

    if message.content.lower().startswith("%thinking"):
        pers = ""
        if len(message.mentions) > 1:
            await message.channel.send("Vous ne pouvez identifier qu'une personne !")
        elif len(message.mentions) == 1:
            pers = requests.get(
                "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(message.mentions[0]),
                stream=True)
        else:
            pers = requests.get(
                "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(message.author),
                stream=True)
        nom = "pers.png"
        if pers.status_code == 200:
            pers.raw.decode_content = True
            with open(nom, 'wb') as f:
                shutil.copyfileobj(pers.raw, f)
            print('Image sucessfully Downloaded: ', nom)
        else:
            print('Image Couldn\'t be retreived')
        png = Image.open("pers.png")
        rond(png)
        rapport = png.size[0] / 225
        main = Image.open("thinkingmain.png").resize((round(rapport * 162), round(rapport * 115)))
        png.paste(main, (0, png.size[1] - main.size[1]), main)
        png.save('thinking.png', 'png')
        with open('thinking.png', 'rb') as f:
            picture = ds.File(f)
            await message.channel.send(file=picture)
        os.remove("pers.png")
        os.remove("thinking.png")

    if message.content.lower().startswith("%troll"):
        debug("Création de l'image troll")
        debug("\t- détection de la personne à mettre sur l'image ...")
        if not len(message.mentions):
            debug("\t\t- pas de mentions, utilisation du nom de l'auteur")
            playtotroll = message.author
        elif len(message.mentions) == 1:
            debug("\t\t- une mention, on prend donc celle-ci")
            playtotroll = message.mentions[0]
        elif len(message.mentions) > 1:
            debug("\t\t- trop de mentions, on prend juste la première")
            playtotroll = message.mentions[0]
        else:
            debug("\t\t- erreur avec les mentions, on prend l'auteur")
            playtotroll = message.author
        debug("\t- récupération de la photo de profil ...")
        pers = requests.get("https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(playtotroll),
                            stream=True)
        if pers.status_code == 200:
            pers.raw.decode_content = True
            with open(AvatarPNGPath, 'wb') as f:
                shutil.copyfileobj(pers.raw, f)
            f.close()
            debug("\t\t- photo téléchargée !")
            debug("Création du montage ...")
            trollimg = Image.open(TrollFacePath)
            avatarimg = Image.open(AvatarPNGPath)
            new = Image.new("RGBA", (1000, 1000))
            img = Image.open(TrollFacePath)
            img = img.resize((1000, 1000))
            new.paste(img, (0, 0))
            img = Image.open(AvatarPNGPath)
            img = img.resize((250, 250))
            rond(img)
            new.paste(img, (275, 200), img)
            new.paste(img, (550, 200), img)
            new.save("TrollResult.png")
            trollimg.close()
            avatarimg.close()
            img = Image.open("TrollResult.png")
            for x in range(0, 1000):
                for y in range(0, 1000):
                    r = img.getpixel((x, y))[0]
                    g = img.getpixel((x, y))[1]  # Quelle optimisation ... x)
                    b = img.getpixel((x, y))[2]
                    newr = 255 - r
                    newg = 255 - g
                    newb = 255 - b
                    img.putpixel((x, y), (newr, newg, newb, 255))
            img.save("ReverseTrollResult.png")
            debug("Création du gif ...")
            images = [imageio.imread("TrollResult.png"), imageio.imread("ReverseTrollResult.png")]
            imageio.mimsave('Troll.gif', images)
            with open('Troll.gif', 'rb') as f:
                picture = ds.File(f)
                await message.channel.send(file=picture)
                os.remove("TrollResult.png")
                os.remove("ReverseTrollResult.png")
                os.remove('Troll.gif')
        else:
            debug("\t\t- erreur durant le téléchargement de la photo :/")

    if message.content.lower() == "%vdm":
        vdm_url = "https://www.viedemerde.fr/aleatoire"
        vdm_html = requests.get(vdm_url).text
        soup = BeautifulSoup(vdm_html, 'html.parser')
        site = soup.find("a", {"class": "article-link"}).getText()
        await message.channel.send(site)

    if message.content.lower().startswith("%pileouface") or message.content.lower().startswith("%pof"):
        msg = message.content.lower().split()
        debug(msg)
        if "pile" not in msg and "face" not in msg:
            await message.channel.send("Vous devez choisir entre pile ou face !")
        else:
            nmbr = randint(0, 1)
            if nmbr == 0:
                rep = "pile"
            else:
                rep = "face"
            if rep in msg:
                resu = "Vous avez gagné !"
            else:
                resu = "Vous avez perdu... :/"
            await message.channel.send("La pièce a fait " + rep + " ! " + resu)

    if message.content.lower().startswith("%cherche"):
        msg = message.content.lower().split()
        del msg[0]
        recherche = " ".join(msg)
        ims = image.search(q=recherche,
                           lang='fr')
        if len(ims.get('hits')) == 0:
            await message.channel.send("Aucun résultat trouvé !")
        else:
            img = requests.get(ims.get('hits')[0].get('largeImageURL'), stream=True)
            nom = "image.jpg"
            if img.status_code == 200:
                img.raw.decode_content = True
                with open(nom, 'wb') as f:
                    shutil.copyfileobj(img.raw, f)
                print('Image sucessfully Downloaded: ', nom)
            else:
                print('Image Couldn\'t be retreived')
            with open('image.jpg', 'rb') as f:
                picture = ds.File(f)
                await message.channel.send(message.author.mention, file=picture)
            os.remove("image.jpg")


def debug(text):
    if debug:
        print("[DEBUG] " + str(text))
    else:
        pass
   
client.run("")

#!/usr/bin/env python
# coding: utf-8

import os
import discord
import wikipedia
import datetime
import discord
import random
import requests
import glob
import fitz
import pytesseract
from PIL import Image
from tools import load_phrases
from twitter_tools import load_twitter_image
from spellchecker import SpellChecker

client = discord.Client()

def build_pupo_response():

    now = datetime.datetime.now()
    hour = now.hour
    day_of_week = now.weekday()

    nickname = load_phrases('nicknames.txt')

    if day_of_week == 0:
        response = """Segunda-feira, {}? Tá de sacanagem""".format(nickname)
        img='stern.png'

    elif day_of_week in [1,2,3]:
        if hour >=6 and hour < 18:
            response = """Você **não pode** tomar uma gelada.\nNão são nem 6 horas, {}. Vai trabalhar.""".format(nickname)
            img = 'boring.jpg'
        else:
            response = """Você **ainda não pode** tomar uma gelada.\nNão é dia disso. Que tal uma aguinha com gás?""".format(nickname)
            img = 'water.jpg'

    elif day_of_week == 4:
        if hour < 18:
            response = """Você **precisa** tomar uma gelada hoje, {}, mas ainda está muito cedo.""".format(nickname)
            img = 'friday.png'
        else:
            response = """É sexta-feira.\nJá passou das 18.\nABRA UMA GELADA IMEDIATAMENTE, {}""".format(nickname.upper())
            img = 'beer.jpg'

    elif day_of_week == 5:
        response = """É sábado, {}.\nFoda-se, abre uma ae.""".format(nickname)
        img = 'beer.jpg'

    elif day_of_week == 6:
        response = """Você **não pode** tomar uma gelada hoje.\nÉ domingo, {}.\nDia de descansar. Que tal um cafezinho?""".format(nickname)
        img = 'coffee.jpg'
            
    return (response, img)



def build_salario_response(wage):

    wage = wage.lower()

    factor = 1

    ks = [x for x in wage if x=='k']

    for k in ks:
        factor = factor*1000

    wage = wage.replace(',','.').replace('k','')

    wage = ''.join([x for x in wage if x.isdigit() or x == '.'])
    
    try:
        wage = int(round(float(wage)*factor))
    except:
        msg = 'Isso não é um número!'
        return msg, 'confused.jpg'

    if wage<=3000:
        msg = 'Um salário de R$ {} é considerado **MISERÁVEL** na cidade de São Paulo. Lamento!'.format(wage)
        return msg, 'miseria.jpg'

    if wage<=7000:
        msg = 'Um salário de R$ {} é considerado **POBRE** na cidade de São Paulo. Sinto muito!'.format(wage)
        return msg, 'pobre.jpg'

    if wage<=15000:
        msg = 'Um salário de R$ {} é considerado **CLASSE MÉDIA** na cidade de São Paulo. Muito bem!'.format(wage)
        return msg, 'classemedia.jpg'

    if wage<=30000:
        msg = 'Um salário de R$ {} é considerado **BEM DE VIDA** na cidade de São Paulo. Quase lá!'.format(wage)
        return msg, 'bemdevida.jpg'

    msg = 'Um salário de R$ {} é considerado **RICO** na cidade de São Paulo. Parabéns!'.format(wage)
    return msg, 'rico.jpg'


def build_cilia_response():
    
    article_found = False
    while not article_found:
        try:
            response= ' <:cilia:767213853435232287>' * 10
            game = load_phrases('cilia.txt')
            if '(' in game:
                game = game.split('(')[0] + ' (video game)'
            article = wikipedia.search(game)
            article = article[0]
            page = wikipedia.page(article)
            response += '\n{}'.format(game)
            response += '\n\n{}'.format(page.url)
            response += '\n\n{} (...)\n'.format(page.summary[0:1000])
            response += ' <:cilia:767213853435232287>' * 10
            article_found = True
        except Exception as e:
            print(e)
    return (response, None)

def build_idelber_response():
    games = load_phrases('cilia.txt',4)
    response = """<:idelber:771875461437325332> Sim, gosto de sexo.

<:idelber:771875461437325332> Sim, falo muito de e faço muito sexo.

<:idelber:771875461437325332> Com quatro regrinhas claras: 

<:idelber:771875461437325332> {},

<:idelber:771875461437325332> {},

<:idelber:771875461437325332> {}

<:idelber:771875461437325332> e {}."""
    response = response.format(games[0],games[1],games[2],games[3])

    return (response, None)

def build_boulas_response():
    return load_phrases('boulas.txt'), None

def build_lucyborn_response():
    img = 'lucyborn.jpg'
    load_twitter_image(id=1216390489605332993,path=img)
    return (None, img)

def build_braut_response():
    img = 'braut.jpg'
    load_twitter_image(id=1317010382301573120,path=img)
    return (None, img)

def build_bagno_response(word, corrected_word):

    response = """Olá!

Aqui quem fala é o Marcos Bagno, professor do Departamento de Línguas Estrangeiras e Tradução da Universidade de Brasília, doutor em filologia e língua portuguesa pela Universidade de São Paulo, tradutor, escritor com diversos prêmios e mais de 30 títulos publicados entre literatura e obras técnico-didáticas.

Estou vendo aqui que você usou a grafia "{}" em vez da grafia "{}", como manda a doutrina gramatical
normativa.

Estou aqui para te falar que tudo bem! Não se pode confundir o uso real, autêntico,
empiricamente coletável da língua por parte dos falantes privilegiados (a norma culta), do
modelo idealizado de língua "boa", arbitrariamente definido pelos gramáticos
normativistas.

A linguagem é um importantíssimo elemento de dominação sociocultural e
política, talvez o mais importante instrumento de dominação e opressão. Quem está no
poder quer continuar nele e, para isso, a maneira de falar dos poderosos, dos privilegiados,
se transforma numa arma de defesa do poder contra a eventual insurreição dos oprimidos.

Chega de preconceito lingüístico!""".format(word, corrected_word)

    return response, 'bagno.jpg'

def build_pasquale_response(word):

    spell = SpellChecker(language='pt')

    misspelled = spell.unknown([word])

    if len(misspelled) == 0:    
        response = """Parabéns, amigo!

Seu português é perfeito.

A palavra "{}" está correta.

Continue assim!""".format(word)

        img = 'pasquale_right.jpg'

    else:

        for w in misspelled:

            corrected_word = spell.correction(w)

            if corrected_word != word:

                lottery = random.randint(1,10)

                if lottery==1:
                    return build_bagno_response(word, corrected_word)

                response = """Opa, amigo!

Parece que você cometeu um erro de português.

A palavra "{}" está errada.

Você quis dizer "{}"?""".format(word, corrected_word)

                img = 'pasquale_wrong.jpg'

            else:

                response = '"{}"'.format(word)
                img = 'pasquale_wtf.jpg'

    return response, img

def build_fazzi_response():

    politico = load_phrases('politicos.txt')
    base_text = load_phrases('fazzi.txt')
    name = politico.split(',')[0]
    article = politico.split(',')[1]
    party_1 = politico.split(',')[2]
    party_2 = 'PT'
    if party_1 == 'PT':
        party_2 = 'PCdoB'
    base_text = base_text.replace('[NAME]',name)
    base_text = base_text.replace('[PARTY1]',party_1)
    base_text = base_text.replace('[PARTY2]',party_2)
    if article=='a':
        base_text = base_text.replace('[X]','a')
        base_text = base_text.replace('[ELX]','ela')
        base_text = base_text.replace('[ABRAÇADX]','abraçada')
    elif article=='o':
        base_text = base_text.replace('[X]','o')
        base_text = base_text.replace('[ELX]','ele')
        base_text = base_text.replace('[ABRAÇADX]','abraçado')

    return (base_text, None)

def build_nazi_response():

    return (load_phrases('nazi.txt'), None)

def build_assis_response():

    img = 'bar_tab.jpg'
    money = random.randint(25,90) + random.randint(0,99)/100
    phrase = 'Opa! G. Assis foi embora do bar enquanto você estava no banheiro mijando, deixando uma conta de R${}.'.format(money)

    return (phrase, img)

def build_random_response():

    lottery = random.randint(1,1000)
    if lottery==1:
        return build_assedio_response()
    return None, None

def build_assedio_response():

    return (load_phrases('assedio.txt'), None)

def build_gamers_response():
    path = 'resources/scans/gamers/*'
    files = glob.glob(path)
    chosen_file = random.sample(files,1)[0]
    doc = fitz.open(chosen_file)
    chosen_page = random.randint(0,doc.page_count-1)
    page = doc.loadPage(chosen_page)
    pix = page.getPixmap()
    img_path = 'resources/images/gamers'
    pix.writePNG(img_path + '.png')
    im = Image.open(img_path + '.png')
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    rgb_im = im.convert('RGB')
    img_width, img_height = rgb_im.size
    cutoff_size = 250
    max_sample_y = img_height - cutoff_size
    max_sample_x = img_width - cutoff_size
    sample_y = random.randint(0,max_sample_y)
    sample_x = random.randint(0,max_sample_x)
    rgb_im = rgb_im.crop((sample_x,sample_y,
                  sample_x+cutoff_size,sample_y+cutoff_size))
    response = pytesseract.image_to_string(rgb_im,lang='por')
    response = response.replace('\n',' ').replace('\t',' ')[0:500]
    rgb_im.save(img_path + '.jpg')
    return (response, 'gamers.jpg')
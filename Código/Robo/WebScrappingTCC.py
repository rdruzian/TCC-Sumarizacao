#!/usr/bin/env python
# coding: utf-8

# ## Implementação de um robô para webscrapping
# ### Autor: Renato Druzian
# 
# #### Este robô será utilizado para buscar notícias no site do G1 e com isso montaremos um dataset que iremos utilizar no TCC para sumarizar notícias
# 1160 paginas 11025 noticias
# 1161 - 1327 paginas ~1660 noticias
# 1328 - 1532 paginas 1740 noticias
# 1533 - 1594 paginas 585 noticias
# 1595 - 2998 páginas 13380
# 2999 - 3000 paginas 20
# Total = 3000 páginas ~28000 noticias
# ## Importação das libs utilizadas para implementação do webscrapping
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import time
import re
import json


# Inicialização de variáveis
data = {}
data['noticias'] = []
d = {}
d['noticia'] = []

count = 0
c = 1
p = 1

verMais = []
noticia = ""
categoria = ""


# Função para abrir uma URL e retornar o html caso não haja erro
def urls(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
    except URLError:
        print("Server down or incorrect domain")
    else:
        return html


# Função que recebe um slice contento as URLs das notícias e a variável para montar o json.
# Aqui é separado o título da notícia, a categoria e o texto. São feitas alguma verificações 
# para não ir dados nulos e por fim guardado na variável que será criado o json
def pegaInfos(titulos, count, categoria, noticia):
    data['noticias'] = []
    for tag in titulos:
        manchete = ""
        noticia = ""
        noti = ""
        ##Pega a url da noticia na pagina prinicpal
        manchete = tag.getText()
        url = tag.get("href")
        if url != "" and type(url) is str:
            resp = urls(url)
            if resp != "" and type(resp) is not None:
                noticias = BeautifulSoup(resp.read(), "html.parser")
                #Busca a categoria da notícia
                cate = noticias.findAll("div", {"class": "header-title-content"})
                #Monta um slice com todos os paragrafos da noticia
                news = noticias.findAll("p", {"class": "content-text__container"})
                #Monta uma string com a noticia, já removendo os paragrafos em branco
                noticia = ""
                for n in news:
                    noti= n.getText()
                    if noti != "":
                        noticia = noticia + noti
                #Pega apenas o título da categoria
                for c in cate:
                    categoria = c.getText()
                
                if noticia != "":
                    data['noticias'].append([{'título': manchete, 'categoria': categoria, 'texto': noticia}])
                    count = count + 1
            else:
                break
        else:
            break
    return data, count


# #### Loop para criar as URLs e realizar a busca das notícias, será necessário no minímo 15000 notícias
while(c <= 30):
    verMais.append("https://g1.globo.com/index/feed/pagina-" + str(c) + ".ghtml")
    c += 1

def salvaJson(data, count):
    print("Salvando...")
    # #### Por fim é criado o json utlizando o encoder UTF-8 para reconhecer a gramática PT-BR 
    with open('C:\\Users\\renat\\TCC\\Código\\robo\\tcc1.json', 'a+', encoding='utf8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=2)
    
    with open('C:\\Users\\renat\\TCC\\Código\\robo\\log1.json', 'w', encoding='utf8') as file:
        file.write("Total noticias: " + str(count) + "\n")

# #### Com as URLs da célula anterior será feito busca das notícias, página a página
for n in verMais:
    print("Processando: " + str(n) + "...")
    res = BeautifulSoup(urls(n).read(),"html.parser")
    ## Alterar essa linha para encontrar a tag principal e mais um atributo html para identificar o titulo da noticia
    titulos = res.findAll("a", {"class": "feed-post-link gui-color-primary gui-color-hover"})
    data, count = pegaInfos(titulos, count, categoria, noticia)
    print(n + ": terminado")
    # if p == 10:
    #     salvaJson(data, count)
    #     p = 1
    # else:
    #     p += 1
    salvaJson(data, count)
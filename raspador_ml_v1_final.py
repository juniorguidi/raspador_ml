import requests, time, telegram_send
from bs4 import BeautifulSoup

def pesquisa_ml(dados_pesquisa):
    resposta = requests.get(dados_pesquisa)
    dados_resposta = BeautifulSoup(resposta.text, "html.parser")
    
    if (dados_resposta.findAll("div", attrs={"class": "andes-card andes-card--flat andes-card--default ui-search-result ui-search-result--core andes-card--padding-default"})):
        produtos = dados_resposta.findAll("div", attrs={"class": "andes-card andes-card--flat andes-card--default ui-search-result ui-search-result--core andes-card--padding-default"})
        lista = 1
    else:
        produtos = dados_resposta.findAll("div", attrs={"class": "andes-card andes-card--flat andes-card--default ui-search-result ui-search-result--core andes-card--padding-default andes-card--animated"})
        lista = 0

    return produtos, lista

def envia_mensagem_telegram(menor_preco, menor_titulo, menor_link, menor_estado):
    menor_preco = "{:,.2f}".format(menor_preco)

    mensagem = ("MENOR PREÇO: \nPreço: R$" + menor_preco + "\nTitulo: " + menor_titulo + "\nEstado: " + menor_estado + "\nLink: " + menor_link)

    print("\n\n")
    print (mensagem)
    print("\n\n")

    telegram_send.send(messages=[mensagem])


menor_preco = 10000.00
url = "https://lista.mercadolivre.com.br/novo/"
#pesquisa = url + input("Produto: ")
pesquisa = "ssd 512"

link_pesquisa = url+pesquisa

produtos, lista = pesquisa_ml(link_pesquisa)

if (int(lista)==1):
    if (produtos):
        for produto in produtos:
            estado = produto.find("span", attrs={"class": "ui-search-item__group__element ui-search-item__details"})
            titulo = produto.find("h2", attrs={"class": "ui-search-item__title"})
            link = produto.find("a", attrs={"class": "ui-search-item__group__element ui-search-link"})
            preco_real = produto.find("span", attrs={"class": "price-tag-fraction"})
            preco_centavos = produto.find("span", attrs={"class": "price-tag-cents"})

            if (estado):
                estado = estado.text
            else:
                estado = "Novo"

            if (preco_centavos):
                preco_produto = preco_real.text + "," + preco_centavos.text
            else:
                preco_produto = preco_real.text + ",00" 

            preco_produto = preco_produto.replace(".","")
            preco_produto = float(preco_produto.replace(",", "."))

            if (preco_produto < menor_preco):
                menor_preco = preco_produto
                if (titulo.text):
                    menor_titulo = titulo.text
                else:
                    menor_titulo = "VAZIO!"               
                menor_link = link["href"]
                menor_estado = estado
    else:
        menor_titulo = "Não encontrado."
        menor_link = "Não encontrado."
        menor_preco = 0
        menor_estado = "Nulo"
else:
    if (produtos):
        for produto in produtos:
            estado = produto.find("span", attrs={"class": "ui-search-item__group__element ui-search-item__details"})
            titulo = produto.find("h2", attrs={"class": "ui-search-item__title ui-search-item__group__element"})
            link = produto.find("a", attrs={"class": "ui-search-link"})
            preco_real = produto.find("span", attrs={"class": "price-tag-fraction"})
            preco_centavos = produto.find("span", attrs={"class": "price-tag-cents"})

            if (estado):
                estado = estado.text
            else:
                estado = "Novo"

            if (preco_centavos):
                preco_produto = preco_real.text + "," + preco_centavos.text
            else:
                preco_produto = preco_real.text + ",00" 

            preco_produto = preco_produto.replace(".","")
            preco_produto = float(preco_produto.replace(",", "."))

            if (preco_produto < menor_preco):
                menor_preco = preco_produto
                if (titulo.text):
                    menor_titulo = titulo.text
                else:
                    menor_titulo = "VAZIO!"               
                menor_link = link["href"]
                menor_estado = estado
        

envia_mensagem_telegram(menor_preco, menor_titulo, menor_link, menor_estado)
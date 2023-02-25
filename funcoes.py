import random
import requests
import pandas as pd
import os

def gerar_jogos(mod, quantidade_dezenas, quantidade_jogos, conc, proximo):

    jogos = []
    dict_jogos = {}
    for i in range(0,quantidade_jogos):
        for a in range(1, quantidade_dezenas+1):
            while True:
                num = random.randrange(range_jogos(modal(mod))[0], range_jogos(modal(mod))[1])
                if num not in jogos:
                    jogos.append(num)
                    break
        dict_jogos[i+1] = jogos
        jogos = []
    dict_jogos["Valor_Jogo"] = valores(modal(mod),"valores",quantidade_dezenas)
    dict_jogos["Valor_Jogos"] = quantidade_jogos * valores(modal(mod),"valores",quantidade_dezenas)
    df_jogos = pd.DataFrame(dict_jogos)
    df_jogos.to_string(f"jogos/{modal(mod)}/"+"jogos_" + modal(mod) + "_" + str(int(conc)+proximo) + ".txt", index=False)

def range_jogos(modalidade):
    if modalidade == "megasena":
        return(1,60)
    elif modalidade == "lotofacil":
        return(1,25)

def valores(modalidade, info, valor):
        valores = {"megasena": {"valores":{6:4.5,7:31.50,8:126,9:378,10:945,11:2079,12:4158,13:7722,14:13513.50,15:22522.50,16:36036.00,17:55692.00,18:83538.00,19:122094.00,20:174420.00},"range_dezenas":{"minimo":6,"maximo":20}},"lotofacil":{"valores":{15:2.5,16:40,17:350,18:2040,19:9690,20:38760},"range_dezenas":{"minimo":15,"maximo":20}}}
        return valores[modalidade][info][valor]

def concurso(mod):
    with open("concursos_" + modal(mod) + ".txt", "r+") as concurso:
        conc = ""
        for i in concurso:
            if i != "\n":
                conc = i
        return conc.replace("\n","")

def proximo_concurso(mod, conc):
    with open("concursos_" + modal(mod) + ".txt", "r+") as concurso:
        for i in concurso:
            pass
        concurso.write(conc+"\n")

def resultado(mod, concurso):
    key = open("chave.txt", "r")
    url = f"http://apiloterias.mksoft.com.br/v1/?sorteio={modal(mod)}&key="+ key.readline() +f"&concurso={concurso}"
    response = requests.get(url, headers={"User-Agent": "XY"})
    dezenas = response.json()["dezenas"]
    return dezenas

def conferencia(jogo, mod):
    df_jogos = pd.read_fwf((f"jogos/{modal(mod)}/"+jogo))
    result = resultado(mod, jogo.split("_")[2])
    numbers_result = [int(number) for number in result]
    cont = 0
    resumo = {}
    jog = []
    for i in df_jogos:
        for a in df_jogos[i]:
            if i != "Valor_Jogo" and i != "Valor_Jogos":
                if a in numbers_result:
                    cont += 1
                    jog.append(a)
        if modal(mod) == "megasena":
            if cont > 3:
                resumo["Jogo " + str(i)] = (cont,(jog))
        else:
            if cont > 10:
                resumo["Jogo " + str(i)] = (cont,(jog))
        cont = 0
        jog = []
    return resumo

def ultimo_concurso(mod):
    key = open("chave.txt", "r")
    url = f"http://apiloterias.mksoft.com.br/v1/?sorteio={modal(mod)}&key="+ key.readline() +"&concurso=ultimo"
    response = requests.get(url, headers={"User-Agent": "XY"})
    conc = response.json()["numero_concurso"]
    return int(conc)

def modal(mod):
    modalidade = {1:"megasena",2:"lotofacil"}
    return modalidade[mod]

def texto_dash(variavel, minimo, maximo):
    while True:
        try:
            if variavel == "modalidade":
                retorno = int(input("Escolha uma das seguintes opções:\n1 - MEGASENA\n2 - LOTOFACIL\n3 - SAIR\nMODALIDADE: "))
                if retorno == 1 or retorno == 2 or retorno == 3:
                    return retorno
            elif variavel == "dezenas":
                retorno = int(input(f"\nMínimo {minimo} dezenas e Máximo {maximo} dezenas.\nQuantas dezenas por jogo?\nDEZENAS: "))
                if retorno >= minimo and retorno <= maximo:
                    return retorno
            elif variavel == "quant_jogos":
                retorno = int(input(f"\nQuantos jogos quer que eu gere?\nJOGOS: "))
                if retorno> 0:
                    return retorno
            elif variavel == "gerar_conferir":
                retorno = int(input("\nO que deseja fazer?:\n1 - GERAR JOGOS\n2 - CONFERIR JOGOS\nMODALIDADE: "))
                if retorno == 1 or retorno == 2:
                    return retorno
            elif variavel == "opcao":
                retorno = int(input(f"\nEscolha uma opçáo entre {minimo} e {maximo}.\nOPÇÃO: "))
                if retorno >= minimo and retorno <= maximo:
                    return retorno
        except:
            pass

def listar_arquivos(modalidade):
    pasta = f"./jogos/{modal(modalidade)}"
    arquiv = {}
    cont = 1
    for diretorio, subpastas, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            arquiv[cont] = arquivo
            cont +=1
    return arquiv
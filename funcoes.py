import random
import requests
import pandas as pd

def gerar_jogos(modalidade, quantidade_dezenas, quantidade_jogos, conc, proximo):

    jogos = []
    dict_jogos = {}
    for i in range(0,quantidade_jogos):
        for a in range(1, quantidade_dezenas+1):
            while True:
                num = random.randrange(range_jogos(modalidade)[0], range_jogos(modalidade)[1])
                if num not in jogos:
                    jogos.append(num)
                    break
        dict_jogos[i+1] = jogos
        jogos = []
    dict_jogos["Valor_Jogo"] = valores(modalidade,quantidade_dezenas)
    dict_jogos["Valor_Jogos"] = quantidade_jogos * valores(modalidade,quantidade_dezenas)
    df_jogos = pd.DataFrame(dict_jogos)
    df_jogos.to_string("jogos/"+"jogos_" + modalidade + "_" + str(int(conc)+proximo) + ".txt", index=False)
    proximo_concurso(modalidade,str(int(conc)+ proximo))

def range_jogos(modalidade):
    if modalidade == "megasena":
        return(1,60)
    elif modalidade == "lotofacil":
        return(1,25)

def valores(modalidade, dezenas):
        valores = {"megasena": {6:4.5,7:31.50,8:126,9:378,10:945,11:2079,12:4158,13:7722,14:13513.50,15:22522.50,16:36036.00,17:55692.00,18:83538.00,19:122094.00,20:174420.00},"lotofacil":{15:2.5,16:40,17:350,18:2040,19:9690,20:38760}}
        return valores[modalidade][dezenas]

def concurso(modalidade):
    with open("concursos_" + modalidade + ".txt", "r+") as concurso:
        conc = ""
        for i in concurso:
            if i != "\n":
                conc = i
        return conc.replace("\n","")

def proximo_concurso(modalidade, conc):
    with open("concursos_" + modalidade + ".txt", "r+") as concurso:
        for i in concurso:
            pass
        concurso.write(conc+"\n")

def resultado(modalidade, concurso):
    key = open("chave.txt", "r")
    url = f"http://apiloterias.mksoft.com.br/v1/?sorteio={modalidade}&key="+ key.readline() +"&concurso={concurso}"
    response = requests.get(url, headers={"User-Agent": "XY"})
    dezenas = response.json()["dezenas"]
    return dezenas

def conferencia(modalidade, concurso):
    df_jogos = pd.read_fwf(("jogos/"+"jogos_" + modalidade + "_" + concurso + ".txt"))
    result = resultado(modalidade, concurso)
    numbers_result = [int(number) for number in result]
    cont = 0
    resumo = {}
    for i in df_jogos:
        for a in df_jogos[i]:
            if i != "Valor_Jogo" and i != "Valor_Jogos":
                if a in numbers_result:
                    cont += 1
        if modalidade == "megasena":
            if cont > 3:
                resumo["Jogo " + str(i)] = cont
        else:
            if cont > 10:
                resumo["Jogo " + str(i)] = cont
        if modalidade == "megasena":
            if cont == 5 or cont == 6:
                print(f"Cuncurso {concurso} e jogo {i}, modalidade {modalidade}, acertou {cont} Dezenas!")
        else:
            if cont == 11 or cont == 12 or cont == 13 or cont == 14 or cont == 15:
                print(f"Cuncurso {concurso} e jogo {i}, modalidade {modalidade}, acertou {cont} Dezenas!")

        cont = 0
    return resumo
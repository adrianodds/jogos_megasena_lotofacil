import funcoes as func

while True:
    
    try:
        modalidade = "megasena"
        concurso = func.concurso(modalidade)
        if concurso == "": #Se não houver jogos salvos para conferencia, gerar novo.
            concurso = "2460" #concurso inicial
            func.gerar_jogos(modalidade,6,100, concurso, 0)
        resumo = func.conferencia(modalidade, concurso)

        if len(resumo) == 0:
            resumo["Acertos"] = 0
            print(resumo)
        if modalidade == "megasena":
            func.gerar_jogos(modalidade,6,100, concurso, 1)
        else:
            func.gerar_jogos(modalidade,15,10, concurso, 1)

    except Exception as er:
        print(er)
        break
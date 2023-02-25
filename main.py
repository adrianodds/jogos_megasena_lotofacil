import funcoes as func

print("BEM VINDO!\n")
while True:
    modalidade = func.texto_dash("modalidade",0,0)
    if modalidade == 3:
        break
    fluxo = func.texto_dash("gerar_conferir",0,0)
    concurso = func.concurso(modalidade)

    if fluxo == 2:
        print("\nEscolha um dos jogos a seguir para iniciar a conferência:\n")
        lista_jogos = func.listar_arquivos(modalidade)
        i = 0
        for i in lista_jogos:
            print(f"{i} : {lista_jogos[i]}")
        opcao = func.texto_dash("opcao", 1, i)
        resumo = func.conferencia(lista_jogos[opcao], modalidade) 
        if len(resumo) == 0:
            print("\nNão houveram acertos, desejo mais sorte da próximo vez.\n")
            input("Pressione enter para continuar\n")
        else:
            print("")
            for i in resumo:
                print(f"O {i} = {resumo[i][1]} acertou {resumo[i][0]} dezenas.")
            print("")
            input("Pressione ENTER para continuar. \n")

    else:
        minimo = func.valores(func.modal(modalidade),'range_dezenas', 'minimo')
        maximo = func.valores(func.modal(modalidade),'range_dezenas', 'maximo')
        dezenas = func.texto_dash("dezenas", minimo, maximo)
        quant_jogos = func.texto_dash("quant_jogos", minimo, maximo)
        func.gerar_jogos(modalidade,dezenas,quant_jogos, concurso, 0)
        print(f"\nForam gerados {quant_jogos} jogos na modalidade {func.modal(modalidade).upper()} para o próximo concurso {concurso}, BOA SORTE!\n")

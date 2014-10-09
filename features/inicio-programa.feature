# language: pt-br
Funcionalidade: Professor pode iniciar programa em turma

    Afim de iniciar a aplicação de exercícios para alunos
    Como professor cadastrado em um cliente
    Posso iniciar um programa pré-definido

    Cenário: Tela de escolha de programa mostra quantos dias ele tem
        Dado um cliente com uma turma, prestes a fechar negócio
        Dado que a turma se chama "2ºB"
        Dado um programa exemplo com 4 baterias
        Se o professor logar e selecionar uma turma
        Então estarei na página "2ºB"
        Se eu clicar no link "2. Programa"
        Então verei o programa exemplo com 4 dias

    Cenário: Programa tem link para conteúdo programático
        Dado um cliente com uma turma, prestes a fechar negócio
        Dado que a turma se chama "2ºB"
        Dado um programa exemplo com 4 baterias
        Se o professor logar e selecionar uma turma
        Então estarei na página "2ºB"
        Se eu clicar no link "2. Programa"
        Então verei o programa exemplo com 4 dias
        Se clicar no link "Detalhes"
        Então estarei na página "Conteúdo programático"
        E verei o conteúdo programático do programa exemplo

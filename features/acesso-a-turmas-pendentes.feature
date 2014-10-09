# language: pt-br
Funcionalidade: Acesso a turma pelo prof. e aluno depende de seu status de pgto

    Como um professor ou como aluno, e dadas determinadas condições
    Acessarei a tentarei abrir turmas
    Para verificar que ela estará ou não disponível dependendo destas condições

    Cenário: Professor não pode acessar turma de lead, com contrato recém-fechado
        Dado um cliente com uma turma, prestes a fechar negócio
        Dado que o contrato não tem pagamentos
        Dado que a turma se chama "2ºB"
        Dado que o prazo para pagamento estar atrasado é de 5 dias
        Se hoje for dia 30/04/2014
        Quando seguir os passos até finalizar a compra
        Então terei um boleto de 70,00 referente a 05/2014, vencendo em 01/05/2014
        Se hoje for dia 01/05/2014, ou seja, o dia seguinte
        Se o professor logar e selecionar uma turma
        Então estarei na página "entre em contato com a diretoria"

    Cenário: Professor não pode acessar turma de lead, mesmo após alguns dias
        Dado um cliente com uma turma, prestes a fechar negócio
        Dado que o contrato não tem pagamentos
        Dado que a turma se chama "2ºB"
        Dado que o prazo para pagamento estar atrasado é de 5 dias
        Se hoje for dia 30/04/2014
        Quando seguir os passos até finalizar a compra
        Então terei um boleto de 70,00 referente a 05/2014, vencendo em 01/05/2014
        Se hoje for dia 04/05/2014
        Se o professor logar e selecionar uma turma
        Então estarei na página "entre em contato com a diretoria"

    Cenário: Professor pode acessar turma de lead que pagou e tornou-se cliente
        Dado um cliente com uma turma, prestes a fechar negócio
        Dado que o contrato não tem pagamentos
        Dado que a turma se chama "2ºB"
        Dado que o prazo para pagamento estar atrasado é de 5 dias
        Se hoje for dia 30/04/2014
        Quando seguir os passos até finalizar a compra
        Então terei um boleto de 70,00 referente a 05/2014, vencendo em 01/05/2014
        Se hoje for dia 04/05/2014
        Se o pagamento de 01/05/2014 for quitado hoje
        Se o professor logar e selecionar uma turma
        Então estarei na página "2ºB"
        Então estarei na página "Iniciar turma"

    Cenário: Professor pode acessar turma no vencimento do últ. pagamento
        Dado um cliente com uma turma, prestes a fechar negócio
        Dado que o contrato tem pagamentos quitados em 02/2014 e 03/2014
        Dado que a turma se chama "2ºB"
        Dado que o prazo para pagamento estar atrasado é de 5 dias
        Se um novo pagamento é gerado para este contrato a vencer em 15/04/2014
        Se hoje for dia 15/04/2014
        Se o professor logar e selecionar uma turma
        Então estarei na página "2ºB"
        Então estarei na página "Iniciar turma"

    Cenário: Professor pode acessar turma antes do últ. pagamento atrasar
        Dado um cliente com uma turma, prestes a fechar negócio
        Dado que o contrato tem pagamentos quitados em 02/2014 e 03/2014
        Dado que a turma se chama "2ºB"
        Dado que o prazo para pagamento estar atrasado é de 5 dias
        Se um novo pagamento é gerado para este contrato a vencer em 15/04/2014
        Se hoje for dia 19/04/2014
        Se o professor logar e selecionar uma turma
        Então estarei na página "2ºB"
        Então estarei na página "Iniciar turma"

    Cenário: Professor não pode acessar turma após últ. pagamento atrasar
        Dado um cliente com uma turma, prestes a fechar negócio
        Dado que o contrato tem pagamentos quitados em 02/2014 e 03/2014
        Dado que a turma se chama "2ºB"
        Dado que o prazo para pagamento estar atrasado é de 5 dias
        Se um novo pagamento é gerado para este contrato a vencer em 15/04/2014
        Se hoje for dia 20/04/2014
        Se o professor logar e selecionar uma turma
        Então estarei na página "entre em contato com a diretoria"

    Cenário: Aluno vê tarefas disponíveis no vencimento do últ. pagamento
        Dado um cliente com uma turma, prestes a fechar negócio
        Dado que o contrato tem pagamentos quitados em 02/2014 e 03/2014
        Dado que o prazo para pagamento estar atrasado é de 5 dias
        Se um novo pagamento é gerado para este contrato a vencer em 15/04/2014
        Se a turma for iniciada dia 15/04/2014 num programa exemplo com um aluno
        Se hoje for dia 15/04/2014
        E houver tarefa para hoje
        Se o aluno logar
        Então estarei na página "Minhas tarefas"
        E verei uma tarefa para o dia

    Cenário: Aluno vê tarefas disponíveis antes do últ. pagamento atrasar
        Dado um cliente com uma turma, prestes a fechar negócio
        Dado que o contrato tem pagamentos quitados em 02/2014 e 03/2014
        Dado que o prazo para pagamento estar atrasado é de 5 dias
        Se um novo pagamento é gerado para este contrato a vencer em 15/04/2014
        Se a turma for iniciada dia 19/04/2014 num programa exemplo com um aluno
        Se hoje for dia 19/04/2014
        E houver tarefa para hoje
        Se o aluno logar
        Então estarei na página "Minhas tarefas"
        E verei uma tarefa para o dia

    Cenário: Aluno não vê tarefas disponíveis após vencimento do últ. pagamento
        Dado um cliente com uma turma, prestes a fechar negócio
        Dado que o contrato tem pagamentos quitados em 02/2014 e 03/2014
        Dado que o prazo para pagamento estar atrasado é de 5 dias
        Se um novo pagamento é gerado para este contrato a vencer em 15/04/2014
        Se a turma for iniciada dia 19/04/2014 num programa exemplo com um aluno
        Se hoje for dia 20/04/2014
        E houver tarefa para hoje
        Se o aluno logar
        Então estarei na página "Minhas tarefas"
        E não verei nenhuma tarefa para o dia

# language: pt-br
Funcionalidade: Cobrança de turmas em andamento

    Afim de manter as cobranças em dia
    Como administrador do sistema
    Verei que pagamentos periódicos são gerados e que recebo avisos de pendências

    Cenário: Comando gera pgtos de turmas pendentes do mês atual
        Dado que o custo por turma é 70,00
        Dado um cliente com uma turma, prestes a fechar negócio
        Dado que o contrato tem pagamentos quitados em 02/2014 e 03/2014
        Se o contrato tem data preferida de pagamento como dia 20 de cada mês
        Se hoje for dia 01/04/2014
        Se comando para geração de pagamentos é executado
        Então contrato terá pagamento em 20/04/2014 no valor de 70,00

    Cenário: Comando gera pgtos de turmas pendentes, mesmo executado atrasado
        Dado que o custo por turma é 70,00
        Dado um cliente com uma turma, prestes a fechar negócio
        Dado que o contrato tem pagamentos quitados em 07/2014 e 08/2014
        Se o contrato tem data preferida de pagamento como dia 25 de cada mês
        E hoje for dia 05/09/2014
        E comando para geração de pagamentos é executado
        Então contrato terá pagamento em 25/09/2014 no valor de 70,00

    Cenário: Comando não gera pgtos de turmas que já tem pgtos no mês em questão
        Dado que o custo por turma é 70,00
        Dado um cliente com uma turma, prestes a fechar negócio

        Se o contrato tem data preferida de pagamento como dia 15 de cada mês
        E o contrato tem pagamentos quitados em 07/2014 e 08/2014
        Então contrato terá pagamento em 15/08/2014 no valor de 70,00

        Se o contrato tem data preferida de pagamento como dia 25 de cada mês
        E hoje for dia 01/08/2014
        E comando para geração de pagamentos é executado
        Então contrato terá pagamento em 15/08/2014 no valor de 70,00

    Cenário: teste de comando que avisa sobre inadimplentes para managers
        Dado que o prazo para pagamento estar atrasado é de 5 dias
        Dado um cliente com uma turma, prestes a fechar negócio
        Dado que o nome do cliente é "Cliente exemplo"
        Dado que a turma se chama "Turma exemplo"
        Dado que o contrato tem pagamentos quitados em 02/2014 e 03/2014
        Se um novo pagamento é gerado para este contrato a vencer em 15/04/2014
        Se hoje for dia 25/04/2014
        Se comando para aviso de inadimplentes é executado
        Então os managers receberão um e-mail com os dados:
            | Cliente         | Turma         |
            | Cliente exemplo | Turma exemplo |

# language: pt-br
Funcionalidade: Cobrança de turmas de compras recém concluídas

    Afim de realizar um pagamento para iniciar o uso do sistema,
    como um cliente em processo de fechamento de compra,
    verei que o valor será proporcional ao número de dias e que,
    se perto do fim do mês e abaixo de limite mínimo, será ignorado,
    sendo cobrado apenas o próximo mês.

    Esquema do Cenário: Data de fechamento de compra influi valor a ser pago
        Dado que o custo por turma é 70,00
        Dado um cliente com uma turma, prestes a fechar negócio
        Se hoje for dia <Data>
        Quando seguir os passos até finalizar a compra
        Então terei um boleto de <Valor> referente a <Referência>, vencendo em <Vencimento>

    Exemplos:
        | Data       | Valor | Referência | Vencimento |
        | 01/04/2014 | 67,67 | 04/2014    | 02/04/2014 |
        | 15/04/2014 | 35,00 | 04/2014    | 16/04/2014 |
        | 30/04/2014 | 70,00 | 05/2014    | 01/05/2014 |
        | 14/02/2014 | 35,00 | 02/2014    | 15/02/2014 |


    Esquema do Cenário: No fim do mês, pagamento dependerá se passou ou não do limite mínimo
        Dado que o custo por turma é 70,00
        Dado que o limite de pagamento mínimo é <Limite>
        Dado um cliente com uma turma, prestes a fechar negócio
        Se hoje for dia <Data>
        Quando seguir os passos até finalizar a compra
        Então terei um boleto de <Valor> referente a <Referência>, vencendo em <Vencimento>

    Exemplos:
        | Limite | Data       | Valor | Referência | Vencimento |
        | 7,00   | 27/04/2014 | 7,00  | 04/2014    | 28/04/2014 |
        | 7,01   | 27/04/2014 | 70,00 | 05/2014    | 28/04/2014 |
        | 21,00  | 21/06/2014 | 21,00 | 06/2014    | 22/06/2014 |
        | 21,01  | 21/06/2014 | 70,00 | 07/2014    | 22/06/2014 |

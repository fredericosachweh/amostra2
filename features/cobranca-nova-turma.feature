# language: pt-br
Funcionalidade: Criação de nova turma leva à tela de financeiro

    Para clientes ativos e com turmas em andamento, quando boleto do mês atual
    já foi aberto, será gerado novo boleto a vencer na data configurada ou no
    dia seguinte se já tiver passado.

    Contexto: Cliente já tem turmas com pagamentos passados
        Dado que o custo por turma é 70,00
        E que o limite de pagamento mínimo é 20,00
        E que contrato tem data preferida de pagamento como dia 20 de cada mês
        Dado um cliente com uma turma, prestes a fechar negócio
        E que o contrato tem pagamentos quitados em 02/2014 e 03/2014

    Esquema do Cenário: Se existente já foi aberto, gera boleto para data preferida
        Dado que cliente tem pgto para turma A para mês atual
        E que pagamento foi aberto pelo cliente
        E que hoje é dia <Dia>/04/2014
        Quando acessar como cliente
        E adicionar turma B
        Então terei boleto de 70,00 para turma A, a vencer em 20/04/2014
        E terei boleto de <Valor> para turma B, a vencer em 20/04/2014
        E verei link para impressão deste boleto

    Exemplos:
        | Dia | Valor |
        | 01  | 67,67 |
        | 15  | 35,00 |
        | 20  | 23,33 |


    Esquema do Cenário: Se existente não foi aberto, atualiza o mesmo
        Dado que cliente tem pgto para turma A para mês atual
        E que pagamento ainda não foi aberto pelo cliente
        E que hoje é dia <Dia>/04/2014
        Quando acesso como cliente
        E adiciono turma B
        Então terei boleto de <Valor> para turmas A e B, a vencer em 20/04/2014
        E verei link para impressão deste boleto
        E verei aviso de que boleto foi anexado ao do mês atual

    Exemplos:
        | Dia | Valor         |
        | 01  | 67,67 + 70,00 |
        | 15  | 35,00 + 70,00 |
        | 20  | 23,33 + 70,00 |


    Esquema do Cenário: Se passou limite mínimo, anexa a boleto do próx. mês
        Dado que o limite de pagamento mínimo é 50,00
        E que cliente tem pgto para turma A para mês atual
        E que hoje é dia <Dia>/04/2014
        Quando acessar como cliente
        E adicionar turma B
        Então terei boleto de 70,00 para turma A, a vencer em 20/04/2014
        E terei boleto de <Valor> para turma A e B, a vencer em 20/05/2014
        E verei link para impressão deste boleto
        E verei aviso de que boleto foi anexado ao do mês seguinte

    Exemplos:
        | Dia | Valor                 |
        | 15  | 35,00 + 70,00 + 70,00 |
        | 20  | 23,33 + 70,00 + 70,00 |
        | 29  | 2,33 + 70,00 + 70,00  |
        | 30  | 70,00 + 70,00         |


    Esquema do Cenário: Se passou limite, mas boleto atual não foi aberto, anexa a ele
        Dado que o limite de pagamento mínimo é 50,00
        E que cliente tem pgto para turma A para mês atual
        E que pagamento ainda não foi aberto pelo cliente
        E que hoje é dia <Dia>/04/2014
        Quando acessar como cliente
        E adicionar turma B
        Então terei boleto de <Valor> para turma A e B, a vencer em 20/04/2014
        E verei link para impressão deste boleto
        E verei aviso de que boleto foi anexado ao do mês atual

    Exemplos:
        | Dia | Valor         |
        | 10  | 46,66 + 70,00 |
        | 15  | 35,00 + 70,00 |

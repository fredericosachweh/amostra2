# language: pt-br
Funcionalidade: Criação de nova turma mostra preço dependente do dia da compra

    Para conhecer o preço a ser pago por uma nova turma, como um clientes ativo
    e com turmas em andamento, ao abrir tela de adicionar turma, verei seu
    preço que será proporcional ao número de dias subsequentes no mês.

    Contexto:
        Dado que o custo por turma é 70,00
        E que o limite de pagamento mínimo é 20,00
        E que contrato tem data preferida de pagamento como dia 20 de cada mês
        Dado um cliente com uma turma, prestes a fechar negócio
        E que o contrato tem pagamentos quitados em 02/2014 e 03/2014

    Esquema do Cenário: Mostra preço parcial e preço total a partir do mês seguinte
        Dado que hoje é dia <Dia>/04/2014
        Quando acessar como cliente
        E abrir a tela de adicionar turma
        Então estarei na página "nova turma terá o custo de R$<Valor> neste mês"
        E estarei na página "R$70,00 a partir de então"

    Exemplos:
        | Dia | Valor |
        | 01  | 67,67 |
        | 15  | 35,00 |
        | 20  | 23,33 |
        | 29  | 2,33  |

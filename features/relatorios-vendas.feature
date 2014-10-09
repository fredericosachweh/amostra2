# language: pt-br
Funcionalidade: Relatórios de vendas

    Para que seja possível acompanhar as vendas realizadas por um vendedor em
    determinados períodos, como um usuário do painel administrativo, poderei
    ver relatórios de vendas mensais e anuais.

    Contexto:
        Dado um usuário administrativo "Francisco de Andrada"
        E o usuário administrativo "Inácio Alvarenga"
        E que o custo por turma é 70,00
        Dado os clientes convertidos em vendas abaixo:
            | Cliente   | Turmas | Fechamento | Valor  | Vendedor          |
            | Exemplo 1 | 2      | 10/03/2014 | 42,42  | Inácio Alvarenga  |
            | Exemplo 2 | 1      | 14/03/2014 | 38,39  | Francisco Andrada |
            | Exemplo 3 | 2      | 18/03/2014 | 29,35  | Inácio Alvarenga  |
            | Exemplo 4 | 1      | 03/04/2014 | 63,00  | Francisco Andrada |
            | Exemplo 5 | 2      | 10/05/2014 | 46,67  | Francisco Andrada |
            | Exemplo 6 | 1      | 14/05/2014 | 33,33  | Inácio Alvarenga  |

    Cenário: Relatório de leads convertidos
        Dado que hoje é dia 15/04/2014
        Quando acesso o painel administrativo
        E acesso relatório de leads convertidos
        Então verei relatório de leads convertidos como abaixo:
            | Cliente   | Turmas | Valor   | Vendedor          |
            | Exemplo 4 | 1      | 35,00   | Francisco Andrada |
            | Exemplo 5 | 2      | 70,00   | Francisco Andrada |
            | Exemplo 6 | 1      | 35,00   | Inácio Alvarenga  |

    Cenário: Relatório de leads consolidado
        Dado que hoje é dia 15/04/2014
        Quando acesso o painel administrativo
        E acesso relatório de leads consolidado
        Então verei relatório de leads consolidados como abaixo:
            | Cliente           | Clientes | Turmas | Valor   |
            | Francisco Andrada | 2        | 3      | 105,00  |
            | Inácio Alvarenga  | 1        | 1      | 35,00   |

    Cenário: Relatório anual de leads consolidado
        Dado que hoje é dia 15/04/2014
        Quando acesso o painel administrativo
        E acesso relatório anual de leads consolidado
        Então verei relatório anual de leads consolidados como abaixo:
            | Cliente           | Clientes | Turmas | Valor   |
            | Francisco Andrada | 3        | 4      | 280,00  |
            | Inácio Alvarenga  | 3        | 5      | 350,00  |

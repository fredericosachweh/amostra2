# language: pt-br
Funcionalidade: Compra bloqueada se há dados de cadastro incompletos

    Afim de manter consistência de dados para geração de nota fiscal
    Como um cliente em processo de fechamento de compra
    Serei convidado a atualizar meus dados obrigatórios até fazê-lo

    Cenário: É impossível fechar compra sem preencher dados obrigatórios
        Dado um cliente com uma turma, prestes a fechar negócio
        Dado que tal cliente não tem definido o CNPJ
        Se eu acessar a demonstração
        Então estarei na página "Inicie sua demonstração"
        Se clicar no link "Comprar agora"
        Então estarei na página "Atualize seus dados"
        E estarei na página "preencha todos os campos obrigatórios"

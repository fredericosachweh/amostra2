# language: pt-br
Funcionalidade: Acesso a demonstração será bloqueado quando esta expirar

    Afim de garantir limitação de acesso a dados sigilosos
    Como um usuário convidado para demonstração
    Terei meu acesso bloqueado após a data da demonstração expirar

    Cenário: Demonstração pode ser acessada antes de vencer
        Dada uma demonstração válida até 25/04/2014
        Se hoje for dia 24/04/2014
        Quando acesso tal demonstração
        Então estarei na página "Inicie sua demonstração"

    Cenário: Demonstração ainda pode ser acessada quando vencer
        Dada uma demonstração válida até 25/04/2014
        Se hoje for dia 25/04/2014
        Quando acesso tal demonstração
        Então estarei na página "Inicie sua demonstração"

    Cenário: Demonstração não pode ser acessada após vencer
        Dada uma demonstração válida até 25/04/2014
        Se hoje for dia 26/04/2014
        Quando acesso tal demonstração
        Então estarei na página "Demonstração expirada"

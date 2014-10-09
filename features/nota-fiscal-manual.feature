# language: pt-br
Funcionalidade: Pagamento pode ter nota fiscal manual

    Afim de manter-se em dia com o fisco e até integrar com sistema automático
    Como um cliente acessando um pagamento
    Verei nota fiscal caso ela tenha sido anexada manualmente

    Contexto:
        Dado um cliente com uma turma, prestes a fechar negócio
        E um pagamento para 15/02/2014
        E hoje for dia 01/04/2014

    Cenário: Pagamento sem nota não tem botão para imprimir nota
        Quando o gestor logar, acessar financeiro
        Então não verá botão para imprimir nota na lista ou nos detalhes

    Cenário: Pagamento com nota tem botão para imprimi-la
        Quando pagamento tem nota fiscal
        E o gestor logar, acessar financeiro
        Então verá botão para imprimir nota na lista e nos detalhes

    Cenário: Ao anexar nota, gerente de cliente recebe e-mail de aviso
        Quando pagamento tem nota fiscal
        Então gerente terá recebido email com link para tal nota

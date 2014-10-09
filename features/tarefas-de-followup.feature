# language: pt-br
Funcionalidade: envio de tarefas por e-mail
    Cenário: tarefa da semana é enviada por e-mail para responsáveis
        Dado um usuário qualquer com tarefa para 03/04/2014
        Se hoje for dia 01/04/2014
        E executar o comando para enviar tarefas por e-mail
        Então usuário qualquer irá receber um aviso por e-mail
        E corpo do email terá link para tarefa

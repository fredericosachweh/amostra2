Release notes
=============

Versão 0.9.8
------------

* Testes através de casos de uso diversos (ver :ref:`cases`);
* Correção de bug: tags não estavam sendo respeitadas no programa;
* Método para realizar auditoria de programas (simular execução dia a dia, veja :ref:`auditoria`);

Versão 0.9.7
------------

* Reordenação de módulos ao inicializar turma;
* Logotipo da home foi readequado para ter o balão em movimento previsto no
  início do projeto;
* Ao exaurir as tentativas sobre um exercício, ao invés de dizer "página não
  encontrada", redireciono para a página de resultado com uma mensagem de erro
  (para deixar mais claro o que acontece ao voltar e tentar responder de
  novamente);
* Fiz com que uma bateria de usuário não pudesse ser iniciada caso não existam
  exercícios suficientes em uma de suas categorias;
* Na tela do aluno aparece o nome da instituição e a turma à qual o aluno está
  relacionado;
* Cliente pode imprimir boleto de pagamento referente às suas turmas e com isso
  fechar uma compra;

Versão 0.9.6
------------

* Cliente tem e-mail institucional, além dos contatos de pessoas;
* Termos de uso e contrato são textuais e podem ser editados no painel
  administrativo (conforme tópico :ref:`conteudo-estatico`);
* Categorias de exercícios tem flag que indica se serão usadas em
  demonstrações;
* Finalizei demonstração para cliente reusando infraestrutura de baterias de
  alunos (conforme tópico :ref:`demonstracoes`);
* Demonstração encerrada leva a tela de erro por falta de permissão (garantindo
  segurança de dados);
* Demonstração encerrada gera tarefa para dono da conta do cliente;
* Finalizada a demonstração, cliente pode fazer a compra ele mesmo (conforme
  tópico :ref:`compras`);
* Exercícios de expressões de multiplicação identificam quais tem zero
  multiplicado ou dividido por algum valor e evitam divisões por zero
  (indeterminações);
* Responsáveis por cliente e responsável por tarefa limitado à membros da
  equipe;
* Ao errar um exercício, mostro a resposta certa e a resposta errada em duas
  abas;
* Modelagem de exercícios de fração imprópria para figura e vice-versa, fração
  imprópria para número misto e vice-versa;

Versão 0.9.5
------------

* Complementei dados cadastrais de clientes;
* Defini status de clientes (conforme tópico :ref:`clientes_status`);
* Permiti filtrar clientes por status, cidade, estado, vendedor;
* Permiti procurar clientes por telefone, nome do cliente, nome de pessoas
  ligadas ao cliente, email de pessoas ligadas ao cliente;
* Permiti importar clientes através de planilha CSV, o que cadastra os clientes gerados como suspect;
* Criei sistema de registro de histórico de contatos e agendamento de tarefas (follow up);
* Registrei no follow up alterações de status do cliente;
* Permiti relacionado cliente a usuário que representará o dono do cliente (vendedor responsável);
* Criei tela para cliente solicitar demonstração e com isso fazer parte do sistema como um prospect;
* Criei tela para vendedor enviar demonstração por e-mail para cliente;
* Criei tela em que cliente tem acesso à link para aceitar termos e iniciar demonstração;

Versão 0.9.4
------------

* Corrigi formatação por extenso de 93/100, que antes era "noventa e três, centésimos" e agora é "noventa e três centésimos", sem vírgula;
* Corrigi formatação do termo um vigésimo que antes ficava no plural;
* Removi informação de debug abaixo de erros no formulário quando digitado errado;
* Não mostro a data de login para usuários recém-cadastrados (antes o default era a data atual);
* Resultado de expressões de adição e subtração não mais incluem zeros após a vírgula;
* Vírgulas a serem escolhidas em operações decimais ficam mais claras se inativas;
* Correção de exercícios de fração decimal que, quando iguais, deve dizer apenas "São iguais";
* Correção de exercícios de unidades de medida que tem casos em que resultados são decimais, mas não era possível digitar números com vírgula;
* Correção de exercícios de unidades de medida em que resultados apareciam com muitos zeros após a vírgula;

Versão 0.9.3
------------

* Resultado de tabuada não mostra mais resposta decimal mas sim inteira (7 ao invés de 7,0);
* Validação para que não se adicione mais alunos do que o limite da classe, por padrão, 50;
* Validação para que não se adicione alunos com nomes repetidos (homônimos);
* Documentação passo-a-passo na tela de detalhes de uma turma;
* Na multiplicação, quando o suporte é opcional (quando é zero), pode ser deixado em branco;
* Tela de login tem botão continuar ao invés de enviar, para estar alinhado com instruções para aluno;
* Senhas são geradas sempre com letras minúsculas e números não ambiguos para evitar confusão;
* Soma decimal tem tags para definir número de casas decimais, não gera números terminados em zero e gera entre 0.01 e 99.99 (por exemplo);
* Tela de login em classe lista usuários em colunas e campo de senha em modal;
* Bug corrigido: ao responder um dia, todos os dias eram marcados como concluídos;
* Tempo agora mostra média do dia. Atualizei testes para garantir tal comportamento;

Versão 0.9.2
------------

* Gerador de exercícios de expressões numéricas de adição e subtração na ordem que aparecem;
* Layout do exercícios de expressões numéricas de adição e subtração na ordem que aparecem;

Versão 0.9.1
------------

* Atualizei a versão do framework de montagem Foundation;
* Corrigi bug no datepicker, agora é possível iniciá-lo com datas em branco;
* Corrigi bug em que exercícios com resposta com múltiplas opções estavam repetindo as opções;
* Impedi remoção do professor pelo gestor, caso este tenha turmas ativas;
* Passei a informar que professor é opcional na tela de cadastro da turma;
* Gerador de exercícios *romano para decimal*;
* Gerador de exercícios *decimal para romano*;
* Permiti exercícios com múltiplas opções terem mais opções do que o necessário, sortenando-as na hora da resolução do exercício e, com isso, garantindo que diferentes alunos não vejam exercícios repetidos. Apliquei isso ao tipo de exercícios *decimal para romano*;
* Ajustes no sistema de importação e refatoração da documentação;

Versão 0.9
----------

A versão 0.9 engloba todas as atividades antes do início do uso do release notes.
